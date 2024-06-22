from django.contrib import admin

from users.models import User, UserConfirmation


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ["id", "username", "email", "phone_number"]


@admin.register(UserConfirmation)
class UserConfirmationAdmin(admin.ModelAdmin):
	list_display = ['id', 'code', 'user']
