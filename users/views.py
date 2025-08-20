from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from .serializers import RegisterSerializer, UserPublicSerializer, MeUpdateSerializer

# Create your views here.
User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = MeUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    lookup_field = "username"
    serializer_class = UserPublicSerializer
