from django.urls import path

from uzmovi.views import MovieAPIView, MovieAddAPIView

urlpatterns = [
	path('', MovieAPIView.as_view()),
	path('add/', MovieAddAPIView.as_view())
]
