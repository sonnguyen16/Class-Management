from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('login/faceid', views.loginFaceId, name='login_faceid'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('capture', views.capture, name='capture'),
    path('attendance', views.attendance, name='attendance'),
    path('update_profile', views.update_profile, name='update_profile'),
    path('class', views.classes, name='class'),
    path('class/<int:class_id>', views.class_detail, name='class_detail'),
]



