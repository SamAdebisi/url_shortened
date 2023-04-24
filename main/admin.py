from django.contrib import admin
from .models import ShortenedURL


# @admin.register(ShortenedURL)
class ShortenedURLAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_url', 'shortened_url', 'clicks', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('original_url', 'shortened_url')


admin.site.register(ShortenedURL, ShortenedURLAdmin)
