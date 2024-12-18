from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class NoteTests(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'password123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.login_url = reverse('login_page')
        self.homepage_url = reverse('homepage')

    def test_get_homepage(self):
        response = self.client.get(self.homepage_url, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')

    def test_get_create_note_page(self):
        response = self.client.get(reverse('create_note'), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_note.html')

    def test_login_get(self):
        response = self.client.get(self.login_url, secure=True)
        self.assertEqual(response.status_code, 200)

    def test_login_post_valid(self):
        logged_in = self.client.login(username=self.username, password=self.password)
        self.assertTrue(logged_in)
        response = self.client.get(self.homepage_url)
        self.assertEqual(response.status_code, 301)