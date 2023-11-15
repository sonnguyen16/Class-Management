from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('login/faceid', views.loginFaceId, name='login_faceid'),
    path('register', views.register, name='register'),
    path('capture', views.capture, name='capture'),
]
