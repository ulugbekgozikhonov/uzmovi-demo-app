from typing import Dict, Any

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from base.utility import check_passwords, check_email_or_phone_number, send_email, send_phone, check_login_type
from users.models import User, VIA_EMAIL, VIA_PHONE, DONE, NEW


class SignUpSerializer(serializers.ModelSerializer):
	id = serializers.UUIDField(read_only=True)
	auth_type = serializers.CharField(required=False)

	def __init__(self, *args, **kwargs):
		super(SignUpSerializer, self).__init__(*args, **kwargs)
		self.fields['email_or_phone_number'] = serializers.CharField(required=False)
		self.fields['reset_password'] = serializers.CharField(required=False)

	class Meta:
		model = User
		fields = ('id', 'username', 'password', 'auth_type')
		extra_kwargs = {
			'auth_type': {'required': False},
			'password': {'write_only': True}
		}

	def validate(self, attrs):
		super(SignUpSerializer, self).validate(attrs)
		attrs = self.auth_validate(attrs)
		return attrs

	def create(self, validated_data):
		user = super(SignUpSerializer, self).create(validated_data)

		if user.auth_type == VIA_EMAIL:
			code = user.creat_verify_code(VIA_EMAIL)
			print(code)
			send_email(user.email, code)
		elif user.auth_type == VIA_PHONE:
			code = user.creat_verify_code(VIA_PHONE)
			print("PHONE_CODE", code)
		# send_phone(user.phone_number, code)
		user.set_password(validated_data.get('password'))
		user.save()
		return user

	@staticmethod
	def auth_validate(attrs):
		password = attrs.get("password")
		reset_password = attrs.get("reset_password")
		if not check_passwords(password, reset_password):
			raise ValidationError("Passwords not match")

		email_or_phone_number = attrs.get("email_or_phone_number")
		verify_type = check_email_or_phone_number(email_or_phone_number)
		print("VT", verify_type)
		if verify_type == "email":
			attrs = {
				"username": attrs.get("username"),
				"password": attrs.get("password"),
				"email": email_or_phone_number,
				"auth_type": VIA_EMAIL
			}
		elif verify_type == "phone_number":
			attrs = {
				"username": attrs.get("username"),
				"password": attrs.get("password"),
				"phone_number": email_or_phone_number,
				"auth_type": VIA_PHONE
			}

		return attrs

	def validate_email_or_phone_number(self, value):
		if value and User.objects.filter(email=value).exists():
			data = {
				"success": False,
				"message": "This email already exists"
			}
			raise ValidationError(data)

		elif value and User.objects.filter(phone_number=value).exists():
			data = {
				"success": False,
				"message": "This phone number already exists"
			}
			raise ValidationError(data)
		return value

	def to_representation(self, instance):
		data = super(SignUpSerializer, self).to_representation(instance)
		data.update(token=instance.tokens())
		return data


class LoginSerializer(TokenObtainPairSerializer):

	def __init__(self, *args, **kwargs):
		super(LoginSerializer, self).__init__(*args, **kwargs)
		self.user = None
		self.fields['userinput'] = serializers.CharField(required=True)
		self.fields['username'] = serializers.CharField(required=False, read_only=True)

	def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
		self.login_validate(attrs)
		attrs = self.user.tokens()
		return attrs

	def login_validate(self, attrs):
		user_input = attrs.get("userinput")

		if check_login_type(user_input) == "username":
			username = user_input
		elif check_login_type(user_input) == "email":
			user = User.objects.filter(email__iexact=user_input).first()
			username = user.username
		elif check_login_type(user_input) == "phone_number":
			user = User.objects.filter(phone_number=user_input).first()
			username = user.username
		else:
			data = {
				"success": False,
				"message": "You don't send phone number or email or username"
			}
			return ValidationError(data)

		user = authenticate(username=username, password=attrs.get('password'))

		if user is not None:
			self.user = user
		else:
			raise ValidationError(
				{
					"success": False,
					"message": "Login or password you entered is incorrect. Please check and try again"
				}
			)
