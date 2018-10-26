from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import auth
from activitytrack.models import UserLoginActivity
from django.db.models.signals import post_save
import mock

class LogInTest(TestCase):

    def test_login_returns_correct_html(self):  # Tests whether the home view render the valid template
        response = self.client.get('/login/')  # Fetching the response from the root url

        # Testing if the response html page contains different html elements same as in index.html
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>vPhrase SendMail</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))
        self.assertTemplateUsed(response, 'account/login.html')  # Make sure that valid template is used

        # Testing the successful_login_log signals by mocking it using Mock library
        with mock.patch('activitytrack.models.UserTemplatesUploadActivity.successful_login_log',
                        autospec=True) as mocked_handler:
            post_save.connect(mocked_handler, sender=UserLoginActivity,
                              dispatch_uid='test_login_returns_correct_html_mocked_handler')

        user = auth.get_user(self.client)# Check if the user is authenticated
        self.assertFalse(user.is_authenticated())# Returns False

        # Valid Cedentials of which the user object is made
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.credentials_wrong = {# Invalid credentials
            'username': 'testuser1',
            'password': 'secret1'}
        user = User.objects.create_user(**self.credentials)
        # send login data
        response = self.client.post('/login/', self.credentials, follow=True)
        # should be logged in now
        self.assertTrue(response.context['user'].is_active)
        # Checks the signal
        self.assertTrue(UserLoginActivity.objects.filter(login_username = user.username,status='S').exists())

        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated())# Retuns True

        self.client.post('/login/', self.credentials_wrong, follow=True)
        self.assertTrue(UserLoginActivity.objects.filter(login_username=self.credentials_wrong['username'], status='F').exists())
        self.assertEqual(mocked_handler.call_count, 2)  # Testing if the moked signal is called twice

