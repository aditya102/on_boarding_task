from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from faker import Faker


class Signup(TestCase):

    def test_signup_page_elements_render(self):
        """
        Test whether all the elements in the signup view is loading properly or not loding.
        """
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertContains(response, '<input type="text" name="username" maxlength="150')
        self.assertContains(response, '<input type="text" name="first_name"')
        self.assertContains(response, '<input type="text" name="last_name"')
        self.assertContains(response, '<input type="email" name="email"')
        self.assertContains(response, '<input type="password" name="password1"')
