from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator

class User(models.Model):
    # Thêm các trường vào đây
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(max_length=254, blank=True)
    role_choices = [
        (0, 'Giáo viên'),
        (1, 'Sinh viên'),
    ]
    role = models.IntegerField(choices=role_choices)
    def __str__(self):
        return self.username

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
    file = models.FileField(upload_to='uploads/homeworks/')

    def __str__(self):
        return self.title

class DoHomework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/do_homeworks/')
    score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, default=None, validators=[MinValueValidator(0), MaxValueValidator(10)])
    comment = models.TextField()
    def __str__(self):
        return self.title
