from django.urls import path

from users.views import RegisterView, VerifyAPIView, LoginAPIView, LoginRefreshView, UpdatePasswordView

urlpatterns = [
	path('register/', RegisterView.as_view()),
	path('login/', LoginAPIView.as_view()),
	path('verify/', VerifyAPIView.as_view()),
	path('login-refresh/',LoginRefreshView.as_view()),
	path('change-password/', UpdatePasswordView.as_view())
]
