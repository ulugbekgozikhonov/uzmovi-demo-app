from django.contrib import admin

from uzmovi.models import Genre, Movie


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
	list_display = ['id', 'title']


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
	list_display = ['id', 'title','genre']
