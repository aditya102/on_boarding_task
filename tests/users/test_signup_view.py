from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from users.forms import SignUpForm


class AccountsTestCase(TestCase):

    def setUp(self):
        self.user_data = {
            'username': 'testuser124',
            'first_name': 'test',
            'last_name': 'demo',
            'email': 'testuser@gmail.com',
            'password1': '1234aditya_is_best',
            'password2': '1234aditya_is_best'
        }

    def test_signup_page_elements_render(self):
        """
        Test for all the elements in the signup page is loding properly or not.
        """
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertContains(response, '<input type="text" name="username" maxlength="150')
        self.assertContains(response, '<input type="text" name="first_name"')
        self.assertContains(response, '<input type="text" name="last_name"')
        self.assertContains(response, '<input type="email" name="email"')
        self.assertContains(response, '<input type="password" name="password1"')

    def test_for_the_both_password_field_match(self):
        """
        Test tha password and confirm password field have same data or not.
        """
        response = self.client.post(reverse('register'), {
            'username': 'testuser124',
            'first_name': 'test',
            'last_name': 'demo',
            'email': 'testuser@gmail.com',
            'password1': '1234adityaisbest11212',
            'password2': '1234adityaisbest'
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
        user = User.objects.create_user(
            username='testuser124',
            first_name='test',
            email="testuser@gmail.com",
            password="aditya"
        )
        form1 = SignUpForm(data=self.user_data)
        self.assertEqual(False, form1.is_valid())

    def test_for_correct_username_format_or_not(self):
        """
        check that username contains anything other than lowercase alphabates or digit
        """
        form = SignUpForm(
            {'username': 't@#@ser124',
             'first_name': 'test',
             'last_name': 'demo',
             'email': 'testuser@gmail.com',
             'password': '1234adityaisbest'}
        )
        self.assertTrue(form.has_error('username'))

    def test_email_is_valid_or_not(self):
        """
        Checks that email is valid or not.It should not contains any special character or spaces.
        """
        form = SignUpForm(
            {'username': 'testuser23',
             'first_name': 'test',
             'last_name': 'demo',
             'email': 'tes-!@$4tuser@gmail.com',
             'password': '1234adityaisbest'}
        )
        self.assertTrue(form.has_error('email'))

    def test_for_valid_email_address_reset(self):
        """
        Checks that password reset request accept only valid emails whose account is present on database.
        """
        temp_form = SignUpForm(data=self.user_data)
        temp_form.save()
        response = response = self.client.post(reverse('password_reset'), {'email': 'testuser1222@gmail.com'})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', "No Account with this email Address")
