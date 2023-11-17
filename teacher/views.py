from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.conf import settings
from app.models import User, Class, Homework, DoHomework
import time
import os
from PIL import Image
from datetime import datetime

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
    deadline = request.POST['deadline']
    new_path = ''
    file_path = ''
    deadline = datetime.strptime(str(deadline), '%Y-%m-%dT%H:%M')

    if deadline < datetime.now():
        return JsonResponse(
            {
                'status': '400',
                'message': 'Deadline must be greater than current time'
            }
        )

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
        'class_id': cls,
        'deadline': deadline
    }

    Homework.objects.create(**homework)
    return JsonResponse(
        {
            'status': '200',
            'message': 'Create successfully'
        }
    )

def get_homework(request):
    dohomework_id = request.POST['dohomework_id']
    do_homework = DoHomework.objects.get(id=dohomework_id)
    if do_homework:
        return JsonResponse(
            {
                'status': '200',
                'message': 'Get successfully',
                'data': {
                    'id': do_homework.id,
                    'file': do_homework.file.url,
                    'score': do_homework.score,
                    'comment': do_homework.comment,
                    'created_at': str(do_homework.created_at),
                }
            }
        )
    
    return JsonResponse(
        {
            'status': '400',
            'message': 'Do homework not found'
        }
    )

def score_homework(request):
    dohomework_id = request.POST['dohomework_id']
    score = request.POST['score']
    comment = request.POST['comment']
    dohomework = DoHomework.objects.get(id=dohomework_id)
    dohomework.score = score
    dohomework.comment = comment
    dohomework.save()
    return JsonResponse(
        {
            'status': '200',
            'message': 'Score successfully',
        }
    )

def update_homework(request):
    print("alo")
    homework_id = request.POST['homework_id']
    title = request.POST['title']
    description = request.POST['description']
    image = request.FILES.getlist('image')
    file = request.FILES.getlist('file')
    deadline = request.POST['deadline']
    homework = Homework.objects.get(id=homework_id)
    new_path = homework.image
    file_path = homework.file

    if deadline:
        deadline = datetime.strptime(str(deadline), '%Y-%m-%dT%H:%M')
        if deadline < datetime.now():
            return JsonResponse(
                {
                    'status': '400',
                    'message': 'Deadline must be greater than current time'
                }
            )
    else:
        deadline = homework.deadline

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

    homework.title = title
    homework.description = description
    homework.image = new_path
    homework.file = file_path
    homework.deadline = deadline
    homework.save()
    return JsonResponse(
        {
            'status': '200',
            'message': 'Update successfully',
        }
    )
