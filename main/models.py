from django.db import models
# import hashlib
# import random
from django.utils.crypto import get_random_string
from django.urls import reverse


class ShortenedURL(models.Model):
    original_url = models.URLField(max_length=200, unique=True)
    shortened_url = models.CharField(max_length=10, unique=True)
    clicks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def clicked(self):
        self.clicks += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.shortened_url:
            self.shortened_url = get_random_string(length=10)
            # self.shortened_url = self.generate_shortened_url()
        return super().save(*args, **kwargs)

    # def generate_shortened_url(self):
    #     # Generate a shortened URL using a hashing algorithm or a random string generator
    #     random.seed(self.original_url)
    #     short_url = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()[:8]
    #     # Ensure that the generated URL is unique
    #     while ShortenedURL.objects.filter(shortened_url=short_url).exists():
    #         random.seed(self.original_url)
    #         short_url = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()[:8]
    #     return short_url

    def __str__(self):
        return self.original_url

    def get_absolute_url(self):
        return reverse('original_url', args=[str(self.shortened_url)])
