from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('join_class', views.join, name='join'),
    path('submit_homework', views.submit_homework, name='submit_homework'),
]



