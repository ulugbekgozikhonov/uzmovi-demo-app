from django.urls import path

from uzmovi.views import MovieAPIView

urlpatterns = [
	path('', MovieAPIView.as_view())
]
