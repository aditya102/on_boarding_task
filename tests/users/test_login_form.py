from faker import Faker
from exam import fixture

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

ERROR_MSG = 'Please enter a correct username and password. Note that both fields may be case-sensitive.'

class LoginView (TestCase):

    def create_user_data(self):
        fake = Faker()
        password = fake.password()
        user_data = {
            'username': fake.user_name(),
            'first_name': fake.name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'password1': password,
            'password2': password,
        }
        return user_data

    @fixture
    def user(self):
        return self.create_user_data()

    def setUp(self):
        self.test_user = User.objects.create_user(username=self.user['username'], password=self.user['password1'])

    def change_password(self):
        """
        Helper method for changing password.
        """
        self.test_user.set_password(self.create_user_data()['password1'])
        self.test_user.save()

    def test_login_page_elements(self):
        """
        Test the login page elements like button, username field and password field is loded properly or not.
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertContains(response, ' <input type="text" name="username"')
        self.assertContains(response, '<input type="password" name="password"')
        self.assertContains(response, '<button class="btn btn-outline-info" type="submit">')

    def test_post_login_page(self):
        """
        Check login page is redirected to home page or not .
        """
        response = self.client.post(
            reverse('login'), {'username': self.user['username'], 'password': self.user['password1']}, follow=True
        )
        self.assertRedirects(response, reverse('home'))

    def test_invalid_username_invalid_password(self):
        """
        Check for invalid username and invalid password should not be able to login
        """
        response = self.client.post(
            reverse('login'), {
                'username': self.create_user_data()['username'],
                'password': self.create_user_data()['password1']
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', None, ERROR_MSG)

    def test_valid_username_invalid_password(self):
        """
        Check for valid username and invalid password should not be able to login
        """
        response = self.client.post(reverse('login'), {'username': self.user['username'], 'password': '1sfsdf'})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', None, ERROR_MSG)

    def test_invalid_username_valid_password(self):
        """
        Check for invalid username and valid password should not be able to login
        """
        response = self.client.post(reverse('login'), {'username': 'xyzabe', 'password': self.user['password1']})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', None, ERROR_MSG)

    def test_blank_username_blank_password(self):
        """
        Check for blank username and blank password should not be able to login
        """
        response = self.client.post(reverse('login'), {'username': '', 'password': ''})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'username', 'This field is required.')
        self.assertFormError(response, 'form', 'password', 'This field is required.')

    def test_login_after_password_change(self):
        """
        Check for After changing password users should be able to login
        """
        old_password = self.user['password1']
        self.change_password()
        response = self.client.post(
            reverse('login'), {'username': self.user['username'], 'password': old_password}
        )
        self.assertEqual(response.status_code, 200)

    def test_old_password_login_check(self):
        """
        Check for users should not be able to login from old password
        """
        old_password = self.user['password1']
        self.change_password()
        response = self.client.post(reverse('login'), {'username': self.user['username'], 'password': old_password})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', None, ERROR_MSG)
