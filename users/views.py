from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework import permissions

from users.models import User
from users.serializers import SignUpSerializer


class SignUpView(CreateAPIView):
	queryset = User.objects.all()
	serializer_class = SignUpSerializer
	permission_classes = [permissions.AllowAny]
