from django.contrib import admin

from uzmovi.models import Genre

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
