from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountsTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username='demo_user', password='demo@123')

    @staticmethod
    def change_password():
        new_user = User.objects.get(username='demo_user')
        new_user.set_password('@new_demo_passowrd')
        new_user.save()

    def test_login_page(self):
        """
        Test for the login page is loding or not
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertContains(response, ' <input type="text" name="username"')
        self.assertContains(response, '<input type="password" name="password"')
        self.assertContains(response, '<button class="btn btn-outline-info" type="submit">')

    def test_post_login_page(self):
        response = self.client.post(reverse('login'), {'username': 'demo_user', 'password': 'demo@123'}, follow=True)
        self.assertRedirects(response, reverse('home'))

    def test_invalid_username_invalid_password(self):
        response = self.client.post(reverse('login'), {'username': 'adafafaf', 'password': 'wrong@passowrd'})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', None, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')

    def test_validusername_invalid_password(self):
        response = self.client.post(reverse('login'), {'username': 'demo_user', 'password': '1sfsdf'})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', None, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')

    def test_invalidusername_validpassword(self):
        response = self.client.post(reverse('login'), {'username': 'xyzabe', 'password': 'demo@123'})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', None, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')

    def test_blankusername_blankpassword(self):
        response = self.client.post(reverse('login'), {'username': '', 'password': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['form'].errors, {'username': 
            ['This field is required.'], 'password': ['This field is required.']})

    def test_newpassword_login(self):
        AccountsTestCase.change_password()
        response = self.client.post(reverse('login'), {'username': 'demo_user', 'password': '@new_demo_password'})
        self.assertEqual(response.status_code, 200)

    def test_oldpassword_login_check(self):
        AccountsTestCase.change_password()
        response = self.client.post(reverse('login'), {'username': 'demo_user', 'password': 'demo@123'})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response, 
            'form', None, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')
