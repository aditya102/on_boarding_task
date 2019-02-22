from exam import fixture
from faker import Faker

from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.users.forms import SignUpForm
from apps.users.mixin import UserMixin

class PasswordReset(UserMixin, TestCase):

    def test_for_valid_email(self):
        """
        Checks that password reset request accepts only valid emails whose account is already present on database.
        """
        temp_form = SignUpForm(data=self.user)
        temp_form.save()
        response = response = self.client.post(reverse(
            'password_reset'),
            {
                'email': self.create_user_data().get('email')
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', "No Account with this email Address")

    def test_email_success(self):
        '''
        Proper email reset message should be sent to the email address with correct subject.
        '''

        user = User.objects.create_user(
            username=self.user['username'], email=self.user['email'], password=self.user['password1']
        )
        user.save()
        self.response = self.client.post(reverse('users:password_reset'), {'email': user.email})
        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(user.email in user.email in mail.outbox[0].to)
        self.assertEqual(mail.outbox[0].subject, 'Password reset on testserver')
        self.assertEqual(mail.outbox[0].from_email, 'webmaster@localhost')

    def test_reset_password_using_verification_link(self):
        '''
        Test Case for checking user is able to reset the password or not if verification token is correct.
        '''

        user = User.objects.create_user(
            username=self.user['username'], email=self.user['email'], password=self.user['password1']
        )
        user.save()
        response = self.client.post(reverse("users:password_reset"), {'email': self.user['email']})
        forgot_page = self.client.post(reverse(
            'users:password_reset_confirm',
            kwargs={
                'uidb64': response.context['uid'],
                'token': response.context['token']
            }),
            follow=True
        )
        forgot = self.client.post(
            forgot_page.redirect_chain[0][0],
            {
                'new_password1': 'Demo@123',
                'new_password2': 'Demo@123'
            }
        )
        self.assertRedirects(forgot, reverse('users:password_reset_complete'))

    def test_invalid_link(self):

        '''
        Test Case to make sure that user should not be able to use link more than once.
        '''
        user = User.objects.create_user(
            username=self.user['username'], email=self.user['email'], password=self.user['password1']
        )
        user.save()
        response = self.client.post(reverse("users:password_reset"), {'email': user.email})
        forgot_page_response = self.client.get(reverse(
            'users:password_reset_confirm',
            kwargs={
                'uidb64': response.context['uid'],
                'token': response.context['token']
            }), follow=True
        )
        forgot = self.client.post(
            forgot_page_response.redirect_chain[0][0],
            {'new_password1': 'Demo@123', 'new_password2': 'Demo@123'}
        )
        self.assertRedirects(forgot, reverse('users:password_reset_complete'))
        forgot_page_response = self.client.post(
            forgot_page_response.redirect_chain[0][0],
            {
                'new_password1': 'Demo@123',
                'new_password2': 'Demo@123'
            }
        )
        self.assertContains(forgot_page_response, ' The password reset link is invalid because it\'s already visited')
