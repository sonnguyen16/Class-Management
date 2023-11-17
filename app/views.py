import os
import cv2
import time
import json
import asyncio
from PIL import Image
from io import BytesIO
import concurrent.futures
from datetime import datetime
from django.shortcuts import render
from .serializers import UserSerializer, AttendanceSerializer
from .models import User, Class
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from opencv.fr import FR
from opencv.fr.persons.schemas import PersonBase
from opencv.fr.compare.schemas import CompareRequest
from opencv.fr.search.schemas import SearchMode, DetectionRequest, SearchOptions, SearchRequest
from django.conf import settings
from unidecode import unidecode 


BACKEND_URL = "https://sg.opencv.fr"
DEVELOPER_KEY = "8z1Rw-fMTcxN2ZjZmEtMDFkMy00Y2JiLThkY2UtYjdiNDkzZDJiZGU2"

# Initialize the SDK
sdk = FR(BACKEND_URL, DEVELOPER_KEY)
data_folder = os.path.join(settings.BASE_DIR, 'static', 'data')
cascade_path = os.path.join(data_folder, 'haarcascade_frontalface_default.xml')
clf = cv2.CascadeClassifier(str(cascade_path))

def index(request):
    user = request.session.get('user')
    if user is not None:
        classes = User.objects.get(id=user['id']).classes.all()
        return render(request, 'pages/index.html', {'classes': classes})
    return HttpResponseRedirect('/login')


def comparison(frame):
    search_request = SearchRequest([frame],collection_id=None,search_mode= SearchMode.FAST, min_score=0.7)
    result = sdk.search.search(search_request)
    return result

def logout(request):
    request.session['user'] = None
    return HttpResponseRedirect('/login')

scans = []

async def detect(frame):
    global scans
    search_options = SearchOptions(collection_id=None, search_mode=SearchMode.FAST, min_score=0.7)
    detect_request_without_search = DetectionRequest(frame, search_options=search_options)
    scans = sdk.search.detect(detect_request_without_search)

def detect_in_executor(frame):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(detect(frame))

def loginFaceId(request):
    if request.method == 'POST':
        user_serializer = UserSerializer()
        attendance_serializer = AttendanceSerializer()
        global scans
        names = []
        capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        count = 0
        scan = []
        detect = False
        with concurrent.futures.ThreadPoolExecutor() as executor:
            while True:
                ret, frame = capture.read()
                key = cv2.waitKey(1)
                if key == ord('f'):
                    # Save frame as image
                    data_folder = os.path.join(settings.BASE_DIR, 'static/uploads/attendances')
                    new_path = os.path.join(data_folder, str(time.time()) + '.jpg')
                    cv2.imwrite(new_path, frame)
                    break
                if len(scans) > 0:
                    for sc in scans:
                        cv2.rectangle(frame, (sc.box.left, sc.box.top), (sc.box.right, sc.box.bottom), (0, 255, 0), 2)
                        if len(sc.persons) > 0:
                            detect = True
                            scan = sc
                            cv2.putText(frame, "Press 'F' to continue" , (10,30), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                            for person in scan.persons:
                                cv2.putText(frame, unidecode(person.person.name), (sc.box.left, sc.box.top - 10), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
                        else:
                            detect = False
                            cv2.putText(frame, "Unknown", (sc.box.left, sc.box.top - 10), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
                            if scan == []:
                                cv2.putText(frame, "Press 'F' to register" , (10,30), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                
                
                cv2.imshow('Login FaceID', frame)
                if count % 60 == 0:
                    executor.submit(detect_in_executor, frame)
                count += 1

        cv2.destroyAllWindows()
        capture.release()
        if detect == False:
            return HttpResponseRedirect('/register')
        user = user_serializer.get_user_by_opencvid(scan.persons[0].person.id)
        request.session['user'] = user
        try:
            attendance = {
                'image': new_path.split('project\\')[1],
                'user': user_serializer.get_user(user['id']),
                'time': datetime.now()
            }
            attendance_serializer.create(attendance)
        except:
            return HttpResponseRedirect('/register')
        return HttpResponseRedirect('/')

def login(request):
    if request.method == "POST":
        user_serializer = UserSerializer()
        email = request.POST['email']
        password = request.POST['password']
        user = user_serializer.get_user_by_email(email)
        print(user)
        if user is None:
            return JsonResponse(
                {
                    'status': '422',
                    'message': 'Email does not exist'
                }
            )
        if user.password != password:
            return JsonResponse(
                {
                    'status': '422',
                    'message': 'Password is incorrect'
                }
            )
        request.session['user'] = user.to_dict()
        return JsonResponse(
            {
                'status': '200',
                'message': 'Login successfully'
            }
        )
    return render(request, 'pages/login.html')

def register(request):
    if request.method == 'POST':
        user_serializer = UserSerializer()
        full_name = request.POST['full_name']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        date_of_birth = datetime.strptime(request.POST['date_of_birth'], "%Y-%m-%d")
        nationality = "Vietnamese"
        images = []
        avatar = request.FILES.getlist('avatar')
        capture_link = request.POST['capture_link']
        if avatar:
            for image in avatar:
                byte_io = BytesIO(image.read())
                image_pil = Image.open(byte_io)
                images.append(image_pil)
        if capture_link:
            images.append(capture_link)

        if(len(images) == 0):
            return JsonResponse(
                {
                    'status': '422',
                    'message': 'Please upload or capture at least 1 image'
                }
            )
        
        if len(images) > 1:
            for i in range(len(images) - 1):  
                for j in range(i + 1, len(images)):
                    compare_request = CompareRequest([images[i]], [images[j]], SearchMode.FAST)
                    score = sdk.compare.compare_image_sets(compare_request)
                    if score < 0.7:
                        return JsonResponse(
                            {
                                'status': '422',
                                'message': 'Images are not the same person'
                            }
                        )
       
        for i in range(len(images) - 1):
            try:
                detect_request = DetectionRequest(images[i])
                scan = sdk.search.detect(detect_request)
                if not scan:
                    return JsonResponse(
                        {
                            'status': '422',
                            'message': 'No face detected, please select other images or capture'
                        }
                    )
            except Exception as e:
                return JsonResponse(
                    {
                        'status': '422',
                        'message': 'No face detected, please select other images or capture'
                    }
                )
       
        data_folder = os.path.join(settings.BASE_DIR, 'static/uploads/avatar')
        avatar = full_name + str(time.time()) + '.jpg'
        new_path = os.path.join(data_folder, avatar)
        if capture_link:
            new_path = capture_link.split('project\\')[1]
        else:
            with open(new_path, 'wb') as f:
                for chunk in request.FILES['avatar'].chunks():
                    f.write(chunk)

            im = Image.open(new_path)
            im.save(new_path)
            new_path = new_path.split('project\\')[1]

        search_result = comparison(images[0])
        id = ''
        if not search_result:
            try:
                person = PersonBase(
                    name=full_name,
                    date_of_birth=date_of_birth,
                    nationality=nationality,
                    images=images
                )
                result = sdk.persons.create(person)
                id = result.id
            except Exception as e:
                return JsonResponse(
                    {
                        'status': '422',
                        'message': e
                    }
                )
        else:
            id = search_result[0].person.id
        
        try:
            user = {
                'full_name': full_name,
                'email': email,
                'password': password,
                'role': role,
                'date_of_birth': date_of_birth,
                'avatar': new_path,
                'opencv_id': id
            }
            user_serializer.create(user)
        except Exception as e:
            error = str(e)
            json_error = json.dumps(error)
            return JsonResponse(
                {
                    'status': '422',
                    'message': json_error.replace('"', '')
                }
            )
        user = user_serializer.get_user_by_opencvid(id)
        request.session['user'] = user
        return JsonResponse(
            {
                'status': '200',
                'message': 'Register successfully'
            }
        )
    return render(request, 'pages/register.html')

def capture(request):
    capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    detect = False

    while True:
        ret, frame = capture.read()

        key = cv2.waitKey(1)
        if key == ord('f') and len(faces) > 0:
            data_folder = os.path.join(settings.BASE_DIR, 'static', 'data')
            new_path = os.path.join(data_folder, str(time.time()) + '.jpg')
            cv2.imwrite(new_path, frame)
            break

        faces = clf.detectMultiScale(
            frame,
            scaleFactor=1.1,
            minNeighbors=7,
            minSize=(100, 100),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, "Press 'F' to capture" , (10,30), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, "Put your face in the webcam" , (10,30), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('Register FaceID', frame)

    cv2.destroyAllWindows()
    capture.release()
    return HttpResponse(new_path)

def attendance(request):
    attendance_serializer = AttendanceSerializer()
    attendances = attendance_serializer.get_attendance()
    return render(request, 'pages/attendance.html', {'attendances': attendances})

def update_profile(request):
    id = request.session.get('user')['id']
    full_name = request.POST['full_name']
    email = request.POST['email']
    password = request.POST['password']
    avatar = request.FILES.getlist('avatar')
    date_of_birth = datetime.strptime(request.POST['date_of_birth'], "%Y-%m-%d")
    user_serializer = UserSerializer()

    instance = user_serializer.get_user(id)
    new_path = instance.avatar
    if avatar:
        data_folder = os.path.join(settings.BASE_DIR, 'static/uploads/avatar')
        avatar = full_name + str(time.time()) + '.jpg'
        new_path = os.path.join(data_folder, avatar)
        with open(new_path, 'wb') as f:
            for chunk in request.FILES['avatar'].chunks():
                f.write(chunk)

        im = Image.open(new_path)
        im.save(new_path)
        new_path = new_path.split('project\\')[1]

    if password != '':
        if len(password) < 6:
            return JsonResponse(
                {
                    'status': '422',
                    'message': 'Password must be at least 8 characters'
                }
            )
        user = {
            'full_name': full_name,
            'email': email,
            'password': password,
            'date_of_birth': date_of_birth,
            'avatar': new_path
        }
    else:
        user = {
            'full_name': full_name,
            'email': email,
            'date_of_birth': date_of_birth,
            'avatar': new_path
        }
    print(user)
    user_serializer.update(instance, user)
    request.session['user'] = user_serializer.get_user(id).to_dict()
    return JsonResponse(
        {
            'status': '200',
            'message': 'Update successfully'
        }
    )

def classes(request):
    user = request.session.get('user')
    if user is not None:
        classes = User.objects.get(id=user['id']).classes.all()
        return render(request, 'pages/class.html', {'classes': classes})
    return HttpResponseRedirect('/login')

def class_detail(request, class_id):
    cls = Class.objects.get(id=class_id)
    homeworks = cls.homeworks.all()
    return render(request, 'pages/class_detail.html', {'class': cls, 'homeworks': homeworks})









    
