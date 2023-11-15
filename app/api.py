from rest_framework import viewsets, generics
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
