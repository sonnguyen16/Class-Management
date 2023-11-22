from django.shortcuts import render
from app.models import User, Class, Homework, DoHomework, User_Class
from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings
import time
import os

# Create your views here.
def join(request):
    if request.session.get('user') is None:
        return HttpResponseRedirect('/login')
    
 
    user = User.objects.get(id=request.session.get('user')['id'])
    invite_code = request.POST['invite_code']
    try:
        cls = Class.objects.get(invite_code=invite_code)
    except:
        return JsonResponse(
            {
                'status': '400',
                'message': 'Class not found'
            }
        )
   
    user_class = User_Class.objects.filter(user=user, class_id=cls).first()
    if user_class:
        return JsonResponse(
            {
                'status': '400',
                'message': 'You already in this class'
            }
        )
    

    User_Class.objects.create(user=user, class_id=cls)
    
    return JsonResponse(
        {
            'status': '200',
            'message': 'Join class successfully'
        }
    )

def submit_homework(request):
    homework_id = request.POST['homework_id']
    file = request.FILES.getlist('file')
    user = User.objects.get(id=request.session.get('user')['id'])
    homework = Homework.objects.get(id=homework_id)
    file_path = ''

    if file:
        data_folder = os.path.join(settings.BASE_DIR, 'static/uploads/homework')
        file = homework.title + str(time.time()) + '.docx'
        file_path = os.path.join(data_folder, file)
        with open(file_path, 'wb') as f:
            for chunk in request.FILES['file'].chunks():
                f.write(chunk)

        file_path = file_path.split('project\\')[1]

    do_homework = {
        'user': user,
        'homework': homework,
        'file': file_path
    }

    DoHomework.objects.create(**do_homework)

    return JsonResponse(
        {
            'status': '200',
            'message': 'Submit homework successfully'
        }
    )
