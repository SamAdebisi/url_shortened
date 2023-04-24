from django.core.cache import cache
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ShortenedURL
from .serializers import ShortenedURLSerializer
from django.shortcuts import redirect, get_object_or_404

# from rest_framework.views import APIView


def redirect_to_original_url(request, shortened_url):
    shortened = get_object_or_404(ShortenedURL, shortened_url=shortened_url)
    original = shortened.original_url

    if shortened.clicks <= 5:
        shortened.clicked()
        return redirect(original)
    else:
        return


class ShortenedURLView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenedURLSerializer

    def post(self, request, *args, **kwargs):
        # Check if the original URL is already cached
        original_url = request.data.get('original_url')
        cached_shortened_url = cache.get(original_url)
        if cached_shortened_url:
            # If the shortened URL is already in the cache, return it
            return Response({'shortened_url': cached_shortened_url}, status=status.HTTP_200_OK)

        # Create a new ShortenedURL object with the original URL provided in the request
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shortened_url = serializer.save()

        # Add the original URL and shortened URL to the cache
        cache.set(original_url, shortened_url.shortened_url)

        # Return the shortened URL
        return Response({'shortened_url': shortened_url.shortened_url}, status=status.HTTP_201_CREATED)


class OriginalURLView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenedURLSerializer
    lookup_field = 'shortened_url'

    def retrieve(self, request, *args, **kwargs):
        # Check if the shortened URL is already cached
        shortened_url = self.kwargs['shortened_url']
        cached_original_url = cache.get(shortened_url)
        if cached_original_url:
            # ShortenedURL.clicked()
            # If the original URL is already in the cache, return it
            return Response({'original_url': cached_original_url}, status=status.HTTP_200_OK)

        # Retrieve the original URL from the database
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        original_url = serializer.data['original_url']

        # Add the shortened URL and original URL to the cache
        cache.set(shortened_url, original_url)
        # ShortenedURL.clicked()

        # Return the original URL
        return Response({'original_url': original_url}, status=status.HTTP_200_OK)


class DeleteShortenedURLView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenedURLSerializer
    lookup_field = 'shortened_url'
