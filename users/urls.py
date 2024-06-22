from django.urls import path

from users.views import SignUpView, VerifyAPIView

urlpatterns = [
	path('signup/', SignUpView.as_view()),
	path('verify/', VerifyAPIView.as_view())
]
