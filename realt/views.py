from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from app.models import Class, Homework, User, User_Class, Notification


# Create your views here.
def create_homework(request):
    class_id = request.POST['class_id']
    name = request.POST['name']
    cls = Class.objects.get(id = class_id)
    user = User.objects.get(id = request.session['user']['id'])
    user_class = User_Class.objects.filter(user=user, class_id=cls).first()
    if not user_class:
        return JsonResponse({
            'status': '404',
            'message': 'User not in class'
        })
    
    notification = {
        "content" : name + ' created homework in ' + cls.name,
        "user" : user,
        "link" : '/class/' + str(cls.id) 
    }

    Notification.objects.create(**notification)

    return JsonResponse({
        'status': '200',
        'data': {
             "content" : name + ' created homework in ' + cls.name,
             "link" : '/class/' + str(cls.id) 
        }
    })

def submit_homework(request):
    homework_id = request.POST['homework_id']
    name = request.POST['name']
    homework = Homework.objects.get(id = homework_id)
    user = homework.created_by
    if user.id == request.session['user']['id']:
        notification = {
            "content" : name + ' submitted homework in ' + homework.title,
            "user" : user,
            "link" : '/homework/' + str(homework.id)
        }

        Notification.objects.create(**notification)

        return JsonResponse({
            'status': '200',
            'data': {
                "content" : name + ' submitted homework in ' + homework.title,
                "link" : '/homework/' + str(homework.id) 
            }
        })

        
    
