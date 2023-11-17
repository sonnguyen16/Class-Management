from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings
from app.models import User, Class, Homework
import time
import os
from PIL import Image

def create_class(request):
    name = request.POST['name']
    user = User.objects.get(id=request.session.get('user')['id'])
    image = request.FILES.getlist('image')
    new_path = ''

    if image:
        data_folder = os.path.join(settings.BASE_DIR, 'static/uploads/class')
        image = name + str(time.time()) + '.jpg'
        new_path = os.path.join(data_folder, image)
        with open(new_path, 'wb') as f:
            for chunk in request.FILES['image'].chunks():
                f.write(chunk)

        im = Image.open(new_path)
        im = im.convert('RGB')
        im.save(new_path)
        new_path = new_path.split('project\\')[1]

    cls = {
        'name': name,
        'image': new_path,
        'created_by': user
    }

    Class.objects.create(**cls)
    return JsonResponse(
        {
            'status': '200',
            'message': 'Create successfully'
        }
    )

def create_homework(request):
    title = request.POST['title']
    class_id = request.POST['class_id']
    description = request.POST['description']
    image = request.FILES.getlist('image')
    file = request.FILES.getlist('file')
    user = User.objects.get(id=request.session.get('user')['id'])
    cls = Class.objects.get(id=class_id)
    new_path = ''
    file_path = ''

    if image:
        data_folder = os.path.join(settings.BASE_DIR, 'static/uploads/homework')
        image = title + str(time.time()) + '.jpg'
        new_path = os.path.join(data_folder, image)
        with open(new_path, 'wb') as f:
            for chunk in request.FILES['image'].chunks():
                f.write(chunk)

        im = Image.open(new_path)
        im = im.convert('RGB')
        im.save(new_path)
        new_path = new_path.split('project\\')[1]

    if file:
        data_folder = os.path.join(settings.BASE_DIR, 'static/uploads/homework')
        file = title + str(time.time()) + '.docx'
        file_path = os.path.join(data_folder, file)
        with open(file_path, 'wb') as f:
            for chunk in request.FILES['file'].chunks():
                f.write(chunk)

        file_path = file_path.split('project\\')[1]

    homework = {
        'title': title,
        'description': description,
        'image': new_path,
        'file': file_path,
        'created_by': user,
        'class_id': cls
    }

    Homework.objects.create(**homework)
    return JsonResponse(
        {
            'status': '200',
            'message': 'Create successfully'
        }
    )

