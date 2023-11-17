from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('create_class', views.create_class, name='create_class'),
    path('create_homework', views.create_homework, name='create_homework'),
]



