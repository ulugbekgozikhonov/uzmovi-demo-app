from django.urls import path

from uzmovi.views import MovieAPIView

urlpatterns = [
	path('', MovieAPIView.as_view()),
	path('add/', MovieAPIView.as_view())
]
