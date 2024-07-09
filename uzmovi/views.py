from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from users.serializers import ForgotPasswordSerializer
from .permissions import IsAdminOrReadOnly

from users.models import ADMIN
from uzmovi.models import Movie
from uzmovi.serializers import MovieSerializer


# Create your views here.

# class MoviListAPIView(ListAPIView):
# 	queryset = Movie.objects.all()
# 	serializer_class = MovieSerializer
#
# 	def get_queryset(self):
# 		pass


class MovieAPIView(APIView):
	throttle_classes = [UserRateThrottle]
	permission_classes = [IsAdminOrReadOnly, IsAuthenticated]
	pagination_class = LimitOffsetPagination

	def post(self, request):
		serializer = MovieSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response({'message': 'Movie successfully added', 'status': 200}, status=200)
		else:
			return Response({'message': 'Bad request', 'status': 400, 'errors': serializer.errors}, status=400)

	def get(self, request):
		search = request.GET.get("search")
		sort = request.GET.get("sort")

		paginator = self.pagination_class()
		movies = paginator.paginate_queryset(Movie.objects.all(), request)
		if sort:
			if sort == "asc":
				movies = movies.order_by('created_at')
			elif sort == "desc":
				movies = movies.order_by('-created_at')
		if search:
			movies = Movie.objects.filter(title__icontains=search)

		serializer = MovieSerializer(instance=movies, many=True).data
		return paginator.get_paginated_response(serializer)




# class MovieAddAPIView(APIView):
# 	permission_classes = [IsAdminOrReadOnly, IsAuthenticated]
#
# 	def post(self, request):
# 		serializer = MovieSerializer(data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response({'message': 'Movie successfully added', 'status': 200}, status=200)
# 		else:
# 			return Response({'message': 'Bad request', 'status': 400, 'errors': serializer.errors}, status=400)


class ForgotPasswordView(APIView):
	serializer_class = ForgotPasswordSerializer
	def post(self, request):
		serializer = ForgotPasswordSerializer(data=request.data)
		if serializer.is_valid():
			pass
		else:
			pass