from django.urls import path
from .views import (
    ShortenedURLView, OriginalURLView, DeleteShortenedURLView,
)

urlpatterns = [
    path('', ShortenedURLView.as_view(), name='shorten'),
    path('<str:shortened_url>/', OriginalURLView.as_view(), name='original_url'),
    path('<str:shortened_url>/delete/', DeleteShortenedURLView.as_view(), name='delete_shortened_url')
]
