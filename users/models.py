from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models

from base.models import BaseModel

ORDINARY, ADMIN, DIRECTOR = ('ordinary', 'admin', 'director')
VIA_EMAIL, VIA_PHONE = ('via_email', 'via_phone')


class User(AbstractUser, BaseModel):
	ROLES = (
		(ORDINARY, ORDINARY),
		(ADMIN, ADMIN),
		(DIRECTOR, DIRECTOR),
	)

	AUTH_TYPE = (
		(VIA_PHONE, VIA_PHONE),
		(VIA_EMAIL, VIA_EMAIL),

	)

	image = models.ImageField(upload_to="media/users_photo/", null=True, blank=True,
	                          default="media/users_photo/default.png", validators=[
			FileExtensionValidator(allowed_extensions=["jpeg", "jpg", "png", "heic", "heif"])])
	username = models.CharField(max_length=31, unique=True)
	password = models.CharField(max_length=255)
	roles = models.CharField(choices=ROLES, default=ORDINARY)
	email = models.EmailField(null=True, blank=True)
	phone_number = models.CharField(max_length=13, null=True, blank=True)
	auth_type = models.CharField(choices=AUTH_TYPE)

	def __str__(self):
		return self.username


class UserConfirmation(BaseModel):
	VERIFY_TYPES = (
		(VIA_PHONE, VIA_PHONE),
		(VIA_EMAIL, VIA_EMAIL)
	)

	code = models.CharField(max_length=8)
	verify_type = models.CharField(max_length=32, choices=VERIFY_TYPES)
	user = models.ForeignKey('users.User', models.CASCADE, related_name='verify_codes')
	expiration_time = models.DateTimeField(null=True)
	is_confirmed = models.BooleanField(default=False)

	def __str__(self):
		return str(self.user.__str__())
