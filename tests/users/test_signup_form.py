from exam import fixture
from faker import Faker

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from users.forms import SignUpForm
from users.mixin import UserMixin


class SignupTest(UserMixin, TestCase):

    def test_for_the_both_password_field_match(self):
        """
        Test password and confirm password field have same password or not.
        """
        response = self.client.post(reverse('register'), {
            'username': self.user['username'],
            'first_name': self.user['first_name'],
            'last_name': self.user['last_name'],
            'email': self.user['email'],
            'password1': self.user['password1'],
            'password2': self.create_user_data()['password2'],
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2', "The two password fields didn't match.")

    def test_for_form_valid(self):
        """
        Test for whole form is valid or not . By checking each field have have valid data or not
        """
        form = SignUpForm(data=self.user)
        self.assertTrue(form.is_valid())

    def tests_for_account_already_exist(self):
        """
        Test that account with that username is already present or not.
        """
        user1 = User.objects.create_user(username=self.user['username'], password=self.user['password1']).save()
        self.assertEqual(True, User.objects.filter(username=self.user['username']).exists())

    def test_for_correct_username_format_or_not(self):
        """
        check that username contains anything other than lowercase alphabates or digit
        """
        form = SignUpForm(
            {
                'username': 't@#@ser124',
                'first_name': self.user['first_name'],
                'last_name': self.user['last_name'],
                'email': self.user['email'],
                'password': self.user['password1'],
            }
        )
        self.assertTrue(form.has_error('username'))

    def test_email_is_valid_or_not(self):
        """
        Checks that email is valid or not.It should not contains any special character or spaces.
        """
        form = SignUpForm(
            {
                'username': 't@#@ser124',
                'first_name': self.user['first_name'],
                'last_name': self.user['last_name'],
                'email': '_@#@$faf@gmail.com',
                'password': self.user['password1'],
            }
        )
        self.assertTrue(form.has_error('email'))
