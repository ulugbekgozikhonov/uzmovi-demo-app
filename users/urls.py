from django.urls import path

from users.views import RegisterView, VerifyAPIView, LoginAPIView

urlpatterns = [
	path('register/', RegisterView.as_view()),
	path('login/', LoginAPIView.as_view()),
	path('verify/', VerifyAPIView.as_view())
]
