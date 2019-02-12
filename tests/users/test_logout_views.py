from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase


class AccountsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='demo_user', password='demo@123')

    def test_logout(self):
        self.client.login(username=self.user.username, password='demo@123')
        response = self.client.get(reverse('logout'), follow=True)
        self.assertRedirects(response, '/users/login/')
