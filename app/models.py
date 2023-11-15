from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator
import shortuuid

class User(models.Model):
    full_name = models.CharField(max_length=200, blank=True)
    date_of_birth = models.DateField(blank=True, default='2000-01-01')
    email = models.EmailField(max_length=254, blank=True, unique=True)
    password = models.CharField(max_length=128)
    avatar = models.ImageField(upload_to='app/static/uploads/avatar', null=True, blank=True, default="static/images/pic-1.jpg")
    opencv_id = models.CharField(max_length=100 ,null=True, blank=True)
    role_choices = [
        (0, 'Giáo viên'),
        (1, 'Sinh viên'),
    ]
    role = models.IntegerField(choices=role_choices)
    def __str__(self):
        return self.full_name
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'date_of_birth': str(self.date_of_birth),
            'avatar_url': self.avatar.url if self.avatar else None,
            'opencv_id': self.opencv_id,
            'role': self.role,
        }

class Class(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.CharField(max_length=150)
    invite_code = models.CharField(max_length=30, null=True, blank=True, default= shortuuid.uuid())
    def __str__(self):
        return self.name
    


class Attendance(models.Model):
    image = models.ImageField(upload_to='app/static/uploads/attendance', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField()

    def __str__(self):
        return self.user.full_name
    
    def to_dict(self):
        return {
            'id': self.id,
            'image_url': self.image.url if self.image else None,
            'user': self.user.to_dict(),
            'time': str(self.time),
        }

class Homework(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='homeworks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='app/static/uploads/homework', null=True, blank=True, default="static/images/thump-1.png")
    file = models.FileField(upload_to='app/static/uploads/homework', null=True, blank=True)

    def __str__(self):
        return self.title

class DoHomework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    file = models.FileField(upload_to='app/static/uploads/homework')
    score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, default=None, validators=[MinValueValidator(0), MaxValueValidator(10)])
    comment = models.TextField()
    def __str__(self):
        return self.title
    
