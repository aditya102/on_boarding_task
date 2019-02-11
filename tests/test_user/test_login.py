from django.test import TestCase
from django.urls import reverse

from django.contrib.auth.models import User


class AccountsTestCase(TestCase):
    def setUp(self):
        user = {
            'username': 'demo_user'
        }
        User.objects.create_user(
            username=user['username'], password='demo@123')

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
        self.assertContains(response, '<div id="div_id_username" class="form-group"> <label for="id_username" class="col-form-label  requiredField">')
        self.assertContains(response, '<span class="asteriskField">*</span> </label> <div class=""> <input type="password" name="password" class="textinput textInput form-control" required id="id_password" /> </div> </div')
        self.assertContains(response, '<button class="btn btn-outline-info" type="submit">Login</button>')

    def test_post_login_page(self):
        response = self.client.post(reverse('login'), {'username': 'demo_user', 'password': 'demo@123'}, follow=True)
        self.assertRedirects(response, reverse('home'))

    def test_login_with_invalid_credentials(self):
        """
        Test for user is not able to login with invalid credentials
        """
        response = self.client.post(reverse('login'), {'username': 'adafafaf', 'password': 'wrong@passowrd'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors, {'__all__': ['Please enter a correct username and password. Note that both fields may be case-sensitive.']})
        response = self.client.post(reverse('login'), {'username': 'demo_user', 'password': '1sfsdf'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors, {'__all__': ['Please enter a correct username and password. Note that both fields may be case-sensitive.']})
        response = self.client.post(reverse('login'), {'username': 'xyzabe', 'password': 'demo@123'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors, {'__all__': ['Please enter a correct username and password. Note that both fields may be case-sensitive.']})
        response = self.client.post(reverse('login'), {'username': '', 'password': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors, {'username': ['This field is required.'], 'password': ['This field is required.']})
        AccountsTestCase.change_password()
        response = self.client.post(reverse('login'), {'username': 'demo_user', 'password': '@new_demo_password'})
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('login'), {'username': 'demo_user', 'password': 'demo@123'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].errors, {'__all__': ['Please enter a correct username and password. Note that both fields may be case-sensitive.']})
