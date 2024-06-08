from django.contrib.auth.models import AbstractUser
from django.db import models

from base.models import BaseModel


# Create your models here.

class User(AbstractUser, BaseModel):
	ROLES = (
		("ORDINARY", "ORDINARY"),
		("ADMIN", "ADMIN"),
		("DIRECTOR", "DIRECTOR"),
	)

	AUTH_TYPE = (
		("VIA_EMAIL", "VIA_EMAIL"),
		("VIA_PHONE", "VIA_PHONE"),
	)

	image = models.ImageField(upload_to="media/users_photo/", null=True, blank=True,
	                          default="media/users_photo/default.png")
	username = models.CharField(max_length=31, unique=True)
	password = models.CharField(max_length=60)
	roles = models.CharField(choices=ROLES, default="ORDINARY")
	auth_type = models.CharField(choices=AUTH_TYPE)


class UserConfirmation(BaseModel):
	pass
