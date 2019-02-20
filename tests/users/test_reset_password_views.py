from exam import fixture
from faker import Faker

from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from users.forms import SignUpForm

fake = Faker()
password = fake.password()


class PasswordReset(TestCase):
    def create_fake_data(self):
        base_password = fake.password()
        user_data = {
            'username': fake.user_name(),
            'first_name': fake.name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'password1': base_password,
            'password2': base_password,
        }
        return user_data

    @fixture
    def user(self):
        return self.create_fake_data()

    def test_for_valid_email_address_reset(self):
        """
        Checks that password reset request accepts only valid emails whose account is already present on database.
        """
        temp_form = SignUpForm(data=self.user)
        temp_form.save()
        response = response = self.client.post(reverse('password_reset'), {'email': fake.email()})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', "No Account with this email Address")

    def test_no_email_sent(self):
        """
        Check that no email should be sent without an email address
        """
        self.response = self.client.post(reverse('password_reset'))
        self.assertEqual(len(mail.outbox), 0)

    def test_email_sent_successfully(self):

        """
         Proper email reset msg should be sent to the email address with correct subject.
        """

        user = User.objects.create_user(
            username=self.user['username'], email=self.user['email'], password=self.user['password1']
        )
        user.save()
        self.response = self.client.post(reverse('password_reset'), {'email': user.email})
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(*mail.outbox[0].to, user.email)
        self.assertEqual(mail.outbox[0].subject, 'Password reset on testserver')
        self.assertEqual(mail.outbox[0].from_email, 'webmaster@localhost')

    def test_reset_password_using_verification_link(self):

        '''
        Test Case for checking user is able to reset the password or not if verification token is correct.
        '''

        user1 = User.objects.create_user(
            username=self.user['username'], email=self.user['email'], password=self.user['password1']
        )
        user1.save()
        response = self.client.post(reverse("password_reset"), {'email': self.user['email']})
        forgot_page = self.client.get(reverse(
            'password_reset_confirm',
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
        self.assertRedirects(forgot, reverse('password_reset_complete'))

    def test_invalid_verification_link(self):

        '''
        Test Case to make sure that user should not be able to use link more than once.
        '''
        user1 = User.objects.create_user(
            username=self.user['username'], email=self.user['email'], password=self.user['password1']
        )
        user1.save()
        response = self.client.post(reverse("password_reset"), {'email': self.user['email']})
        forgot_page = self.client.get(reverse(
            'password_reset_confirm',
            kwargs={
                'uidb64': response.context['uid'],
                'token': response.context['token']
            }), follow=True
        )
        forgot = self.client.post(
            forgot_page.redirect_chain[0][0],
            {'new_password1': 'Demo@123', 'new_password2': 'Demo@123'}
        )
        self.assertRedirects(forgot, reverse('password_reset_complete'))
        # Password changed successfully.
        reset_password_again = self.client.get(reverse(
            'password_reset_confirm',
            kwargs={
                'uidb64': response.context['uid'],
                'token': response.context['token']
            }), follow=True
        )
        forgot_again = self.client.post(
            forgot_page.redirect_chain[0][0],
            {
                'new_password1': 'Demo@123',
                'new_password2': 'Demo@123'
            }
        )
        self.assertContains(forgot_again, ' The password reset link is invalid because it\'s already visited')
