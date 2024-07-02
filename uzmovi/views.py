from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from users.models import ADMIN
from uzmovi.models import Movie
from uzmovi.serializers import MovieSerializer


# Create your views here.


class MovieAPIView(APIView):
	throttle_classes = [UserRateThrottle]

	def get(self, request):
		movies = Movie.objects.all()
		serializer = MovieSerializer(instance=movies, many=True).data
		return Response(serializer)

class MovieAddAPIView(APIView):
	def post(self, request):
		if request.user.roles == ADMIN:
			serializer = MovieSerializer(data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response({'message': 'Movie successfully added', 'status': 200}, status=200)
			else:
				return Response({'message': 'Bad request', 'status': 400, 'errors': serializer.errors}, status=400)
		else:
			return Response({'message': "Page not found"}, status=404)

