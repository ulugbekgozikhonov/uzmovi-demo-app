from datetime import datetime

from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User, DONE
from users.serializers import SignUpSerializer, LoginSerializer


class RegisterView(CreateAPIView):
	queryset = User.objects.all()
	serializer_class = SignUpSerializer
	permission_classes = [permissions.AllowAny]


class VerifyAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request):
		user = request.user
		code = request.data.get('code')
		user_verify_code = user.verify_codes.filter(code=code, expiration_time__gte=datetime.now(), is_confirmed=False)
		if user_verify_code.exists():
			user_verify_code.update(is_confirmed=True)
			user.auth_status = DONE
			user.save()
			data = {
				'message': 'successfully registered'
			}
			return Response(data, status=200)

		raise ValidationError({
			'message': 'your code invalid or time expired'
		})


class LoginAPIView(TokenObtainPairView):
	serializer_class = LoginSerializer



