# from django.contrib.auth.models import User
from .models import User
from rest_framework import generics
from .serializers import UserSerialiser
from rest_framework.permissions import AllowAny, IsAuthenticated


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerialiser
    permission_classes = [AllowAny]

class RetrieveUpdateDeleteUserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerialiser
    permission_classes = [IsAuthenticated]
