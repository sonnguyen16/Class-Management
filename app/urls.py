from django.contrib import admin
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from . import api
from django.conf.urls import include

router = DefaultRouter()
router.register('user', api.UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('login/faceid', views.loginFaceId, name='login_faceid'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('capture', views.capture, name='capture'),
    path('attendance', views.attendance, name='attendance'),
]



