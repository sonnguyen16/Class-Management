from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('create_class', views.create_class, name='create_class'),
    path('create_homework', views.create_homework, name='create_homework'),
    path('get_homework', views.get_homework, name='get_homework'),
    path('score_homework', views.score_homework, name='score_homework'),
    path('update_homework', views.update_homework, name='update_homework'),
]



