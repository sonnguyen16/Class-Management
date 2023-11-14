from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    role_choices = [
        (0, 'Giáo viên'),
        (1, 'Sinh viên'),
    ]
    role = models.IntegerField(choices=role_choices)

    # Đặt related_name để tránh xung đột với auth.User
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')

    class Meta:
        permissions = [
            ("co_the_lam_gi_do", "Có thể làm gì đó"),
        ]

class Class(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.CharField(max_length=150)

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField()

class Homework(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='uploads/homeworks/')

class DoHomework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/do_homeworks/')
    score = models.IntegerField()
    comment = models.TextField()
