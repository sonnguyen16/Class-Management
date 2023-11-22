from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('create_homework', views.create_homework, name='create_homework'),
    path('submit_homework', views.submit_homework, name='create_class'),
]



