from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.core.cache import cache
from .models import ShortenedURL
from datetime import datetime
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class ShortenerTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@gmail.com',
            password='testpass123',
        )

        self.shortened = ShortenedURL.objects.create(
            original_url="https://www.google.com",
            shortened_url='abc123',
            clicks=0,
        )

    def tearDown(self):
        cache.clear()

    def test_create_user(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@gmail.com')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_create_shortened_url(self):
        self.assertEqual(f'{self.shortened.original_url}',
                         'https://www.google.com')
        self.assertEqual(f'{self.shortened.shortened_url}',
                         'abc123')
        self.assertEqual(f'{self.shortened.clicks}', '0')

    def test_create_shortened_view_for_logged_in_user(self):
        url = reverse('shorten')
        self.client.login(username='testuser',
                          email='test@gmail.com',
                          password='testpass123')
        response = self.client.post(url, {'original_url': 'https://www.google.com/'})
        self.assertEqual(response.status_code, 201)
        # self.assertTrue('shortened_url' in response.data)
        # self.assertContains(response, "https://www.google.com")

    def test_create_shortened_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.post(reverse('shorten'))
        self.assertEqual(response.status_code, 403)

    # def test_retrieve_original_url(self):
    #     url = reverse('retrieve-url', args=[self.shortened_url.short_url])
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(response.url, self.original_url)
    #
    # def test_delete_shortened_url(self):
    #     url = reverse('delete-url', args=[self.shortened_url.short_url])
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, 204)
    #     self.assertFalse(ShortenedURL.objects.filter(id=self.shortened_url.id).exists())
    #
    # def test_shortened_url_created_at(self):
    #     now = datetime.now()
    #     self.assertLess(self.shortened_url.created_at, now)
    #
    # def test_shorten_url_caching(self):
    #     url = reverse('shorten-url')
    #     response1 = self.client.post(url, {'original_url': 'https://www.example.com/'})
    #     self.assertEqual(response1.status_code, 201)
    #     shortened_url = response1.data['shortened_url']
    #
    #     # Clear cache and send request again
    #     cache.clear()
    #     response2 = self.client.post(url, {'original_url': 'https://www.example.com/'})
    #     self.assertEqual(response2.status_code, 201)
    #     self.assertEqual(response2.data['shortened_url'], shortened_url)
    #
    # def test_authentication(self):
    #     url = reverse('shorten-url')
    #     response = self.client.post(url, {'original_url': 'https://www.example.com/'})
    #     self.assertEqual(response.status_code, 401)
    #
    #     self.api_client.logout()
    #     response = self.api_client.post(url, {'original_url': 'https://www.example.com/'})
    #     self.assertEqual(response.status_code, 401)
    #
    # def test_encryption(self):
    #     url = reverse('shorten-url')
    #     response = self.client.post(url, {'original_url': 'https://www.example.com/'})
    #     self.assertEqual(response.status_code, 201)
    #     self.assertTrue(response.data['shortened_url'].startswith('http'))
    #
    # def test_invalid_url(self):
    #     url = reverse('shorten-url')
    #     response = self.client.post(url, {'original_url': 'invalidurl'})
    #     self.assertEqual(response.status_code, 400)
    #
    # def test_delete_shortened_url_authentication(self):
    #     url = reverse('delete-url', args=[self.shortened_url.short_url])
    #
    #     # Try to delete without authentication
    #     response = self.client.delete(url)
    #     self.assertEqual(response.status_code, 200)
