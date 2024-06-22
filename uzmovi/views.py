from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from uzmovi.models import Movie
from uzmovi.serializers import MovieSerializer


# Create your views here.


class MovieAPIView(APIView):
	throttle_classes = [UserRateThrottle]

	def get(self, request):
		movies = Movie.objects.all()
		serializer = MovieSerializer(instance=movies, many=True).data
		return Response(serializer)
