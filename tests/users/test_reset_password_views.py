from django.test import TestCase
from django.urls import reverse
from faker import Faker
from django.contrib.auth.models import User
from django.core import mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from users.forms import SignUpForm

fake = Faker()
password = fake.password()


class PasswordReset(TestCase):
    
    def setUp(self):
        self.user_data = {
            'username': fake.user_name(),
            'first_name': fake.name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'password1': password,
            'password2': password,
        }

    def test_for_valid_email_address_reset(self):
        """
        Checks that password reset request accepts only valid emails whose account is already present on database.
        """
        temp_form = SignUpForm(data=self.user_data)
        temp_form.save()
        response = response = self.client.post(reverse('password_reset'), {'email': fake.email()})
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email', "No Account with this email Address")

class EmailReset(TestCase):

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
            username='emailtestuser', email='testuser123@testing.com', password='Testing@1234'
        )
        user.save()
        self.response = self.client.post(reverse('password_reset'), {'email': user.email})
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(*mail.outbox[0].to, user.email)
        self.assertEqual(mail.outbox[0].subject, 'Password reset on testserver')
        self.assertEqual(mail.outbox[0].from_email, 'webmaster@localhost')

# class VerificationTokenCheck(TestCase):

#     def test_reseting(self):
#         """
#         Checks that verification token should not be used more than once and User should get proper error while using 
#         invalid token.
#         """
#         email = fake.email()
#         User.objects.create_user(
#             first_name=fake.first_name(), last_name=fake.last_name(), username=fake.user_name(),
#             email=email, password="", is_active=True).save()
#         response = self.client.post(reverse('password_reset'), {email: email})
#         self.client.get(
#             reverse('reset_password/confirm/'), kwargs={'uidb64': response.context['uid'], 
#             'token': response.context['token']}, follow=True
#         )




