from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator

class User(models.Model):
    email = models.EmailField(max_length=254, blank=True)
    password = models.CharField(max_length=128)
    avatar = models.ImageField(upload_to='app/static/uploads/avatar', null=True, blank=True, default="app/static/images/pic-1.jpg")
    role_choices = [
        (0, 'Giáo viên'),
        (1, 'Sinh viên'),
    ]
    role = models.IntegerField(choices=role_choices)
    def __str__(self):
        return self.email

class Class(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField()

class Homework(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='homeworks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='app/static/uploads/homework', null=True, blank=True, default="app/static/images/thump-1.png")
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
    
