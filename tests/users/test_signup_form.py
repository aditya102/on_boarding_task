from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from faker import Faker

from users.forms import SignUpForm

fake = Faker()
password = fake.password()


class Signup(TestCase):
    def setUp(self):
        self.user_data = {
            'username': fake.user_name(),
            'first_name': fake.name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'password1': password,
            'password2': password,
        }

    def test_for_the_both_password_field_match(self):
        """
        Test password and confirm password field have same password or not.
        """
        response = self.client.post(reverse('register'), {
            'username': fake.user_name(),
            'first_name': fake.name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'password1': password,
            'password2': fake.password(),
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'password2', "The two password fields didn't match.")

    def test_for_form_valid(self):
        """
        Test for whole form is valid or not . By checking each field have have valid data or not
        """
        form = SignUpForm(data=self.user_data)
        self.assertTrue(form.is_valid())

    def tests_for_account_already_exist(self):
        """
        Test that account with that username is already present or not.
        """
        user1 = User.objects.create_user(username='testuser124', password=fake.password()).save()
        self.assertEqual(True, User.objects.filter(username='testuser124').exists())

    def test_for_correct_username_format_or_not(self):
        """
        check that username contains anything other than lowercase alphabates or digit
        """
        form = SignUpForm(
            {'username': 't@#@ser124',
             'first_name': fake.first_name(),
             'last_name': fake.last_name(),
             'email': fake.email(),
             'password': fake.password()}
        )
        self.assertTrue(form.has_error('username'))

    def test_email_is_valid_or_not(self):
        """
        Checks that email is valid or not.It should not contains any special character or spaces.
        """
        form = SignUpForm(
            {'username': fake.user_name(),
             'first_name': fake.first_name(),
             'last_name': fake.last_name(),
             'email': 'tes-!@$4tuser@gmail.com',
             'password': fake.password()}
        )
        self.assertTrue(form.has_error('email'))
