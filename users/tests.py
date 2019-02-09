from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class LogInTest(TestCase):

    def test_login_screen_elements(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)




