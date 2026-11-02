from django.contrib import admin
from .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'genre', 'release_year', 'rating')
    search_fields = ('title', 'genre')
    list_filter = ('genre', 'release_year')
    ordering = ('title',)
