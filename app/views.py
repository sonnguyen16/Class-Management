from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from opencv.fr import FR
from opencv.fr.compare.schemas import CompareRequest
from opencv.fr.persons.schemas import PersonBase
from opencv.fr.search.schemas import SearchMode, DetectionRequest, SearchOptions, SearchRequest
from django.conf import settings
from django.core.files.storage import default_storage
from unidecode  import unidecode 
import os
import time
import cv2
from datetime import datetime
from PIL import Image
from io import BytesIO
import asyncio
import concurrent.futures
from .serializers import UserSerializer, AttendanceSerializer
import json

# Define the region, and developer key
# SG: "https://sg.opencv.fr"
# US: "https://us.opencv.fr"
# EU: "https://eu.opencv.fr"

BACKEND_URL = "https://sg.opencv.fr"
DEVELOPER_KEY = "8z1Rw-fMTcxN2ZjZmEtMDFkMy00Y2JiLThkY2UtYjdiNDkzZDJiZGU2"

# Initialize the SDK
sdk = FR(BACKEND_URL, DEVELOPER_KEY)
data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'data')
cascade_path = os.path.join(data_folder, 'haarcascade_frontalface_default.xml')
clf = cv2.CascadeClassifier(str(cascade_path))

def index(request):
    if request.session['user']:
        return render(request, 'pages/index.html')
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
                    data_folder = os.path.join(settings.BASE_DIR, 'app/static/uploads/attendances')
                    new_path = os.path.join(data_folder, str(time.time()) + '.jpg')
                    cv2.imwrite(new_path, frame)
                    break
                if len(scans) > 0:
                    for scan in scans:
                        cv2.rectangle(frame, (scan.box.left, scan.box.top), (scan.box.right, scan.box.bottom), (0, 255, 0), 2)
                        if len(scan.persons) > 0:
                            detect = True
                            scan = scan
                            cv2.putText(frame, "Press 'F' to continue" , (10,30), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                            for person in scan.persons:
                                cv2.putText(frame, unidecode(person.person.name), (scan.box.left, scan.box.top - 10), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
                        else:
                            detect = False
                            cv2.putText(frame, "Unknown", (scan.box.left, scan.box.top - 10), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
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
        attendance = {
            'image': new_path.split('project\\')[1],
            'user': user_serializer.get_user(user['id']),
            'time': datetime.now()
        }
        attendance_serializer.create(attendance)
        return HttpResponseRedirect('/')

def login(request):
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
                    
        search_result = comparison(images[0])
        if search_result:
            return JsonResponse(
                {
                    'status': '422',
                    'message': 'Person are already registered'
                }
            )
       
        data_folder = os.path.join(settings.BASE_DIR, 'app/static/uploads/avatar')
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

        try:
            person = PersonBase(
                name=full_name,
                date_of_birth=date_of_birth,
                nationality=nationality,
                images=images
            )
            result = sdk.persons.create(person)
        except Exception as e:
            return JsonResponse(
                {
                    'status': '422',
                    'message': e
                }
            )
        
        try:
            user = {
                'full_name': full_name,
                'email': email,
                'password': password,
                'role': role,
                'date_of_birth': date_of_birth,
                'avatar': new_path,
                'opencv_id': result.id
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
        request.session['user'] = user_serializer.get_user_by_opencvid(result.id)
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
            data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'data')
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



    
