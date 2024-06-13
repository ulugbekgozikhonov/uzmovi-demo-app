from rest_framework import serializers

from uzmovi.models import Movie, Genre


class GenreSerializer(serializers.ModelSerializer):
	id = serializers.UUIDField(read_only=True)

	class Meta:
		model = Genre
		fields = ["id", "title", ]


class MovieSerializer(serializers.ModelSerializer):
	id = serializers.UUIDField(read_only=True)
	genre = GenreSerializer()

	class Meta:
		model = Movie
		fields = ["id", "title", "genre"]
