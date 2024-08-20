from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator
import shortuuid

class User(models.Model):
    full_name = models.CharField(max_length=200, blank=True)
    date_of_birth = models.DateField(blank=True, default='2000-01-01')
    email = models.EmailField(max_length=254, blank=True, unique=True)
    password = models.CharField(max_length=128)
    avatar = models.ImageField(upload_to='app/static/uploads/avatar', null=True, blank=True)
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
    invite_code = models.CharField(max_length=30, null=True, blank=True, default= shortuuid.uuid())
    image = models.ImageField(upload_to='static/uploads/class', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='classes')
    def __str__(self):
        return self.name
    

class Attendance(models.Model):
    image = models.ImageField(upload_to='static/uploads/attendance', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    time = models.DateTimeField()

    def __str__(self):
        return self.user.full_name

class Homework(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='homeworks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='static/uploads/homework', null=True, blank=True)
    file = models.FileField(upload_to='static/uploads/homework', null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='homeworks')
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

class DoHomework(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dohomeworks')
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name='dohomeworks')
    file = models.FileField(upload_to='static/uploads/homework')
    score = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, default=None, validators=[MinValueValidator(0), MaxValueValidator(10)])
    comment = models.TextField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return ''
    
class User_Class(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_classes')
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='user_classes')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.full_name + ' - ' + self.class_id.name
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    content = models.TextField()
    link = models.CharField(max_length=200, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.link
