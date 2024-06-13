from django.db import models

from base.models import BaseModel


# Create your models here.

class Genre(BaseModel):
	title = models.CharField(65)


class Movie(BaseModel):
	title = models.CharField(max_length=60)
	image = models.ImageField(upload_to="media/movies/images", null=True)
	genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
