from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

from users.models import ADMIN


class IsAdminOrReadOnly(BasePermission):
	def has_permission(self, request, view):
		if request.method in SAFE_METHODS:
			return True
		return request.user.is_staff

# def has_object_permission(self, request, view, obj):
# 	return request.user.is_staff
