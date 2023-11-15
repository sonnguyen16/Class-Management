from rest_framework.serializers import ModelSerializer
from .models import User, Attendance

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'role', 'avatar']

    def create(self, validated_data):
        user = User(**validated_data)
        user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
        
    def get_user_by_opencvid(self, opencvid):
        try:
            return User.objects.get(opencv_id=opencvid).to_dict()
        except User.DoesNotExist:
            return None
        
class AttendanceSerializer(ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'image', 'user', 'time']

    def create(self, validated_data):
        attendance = Attendance(**validated_data)
        attendance.save()
        return attendance
 

    def get_attendance(self):
        try:
            return Attendance.objects.all()
        except Attendance.DoesNotExist:
            return None