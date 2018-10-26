from django.test import TestCase, RequestFactory
from django.core.urlresolvers import resolve
from basic.views import home, uploadTemplates, parse_template, append_template
from basic.models import SubscribedEmail, EmailTemplates, SendEmail
from django.http import HttpRequest
from basic.forms import EmailSubscriberAddForm, EmailTemplatesUploadForm
from xml.sax.saxutils import escape
from django.contrib.auth.models import User
from django.core.files import File
import mock
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
import os
import re
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib import auth
from mock import patch
import shutil
import tempfile
from django.conf import settings


# To test the views
# testing the 'home' view
class HomePageTest(TestCase):

    # To test if root url '/' maps to valid view i.e home view
    def test_root_url_resolves_to_home_view(self):
        # Resolve() is used find which view the url directs to
        found = resolve('/')
        # Checks whether directed url by found is same as home view
        self.assertEqual(found.func, home)

    # Tests whether the home view render the valid template
    def test_home_page_returns_correct_html(self):
        # Fetching the response from the root url
        response = self.client.get('/')

        # Testing if the response html page contains different html elements same as in index.html
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>vPhrase SendMail</title>', html)
        self.assertTrue(html.strip().endswith('</html>'))
        # Make sure that valid template is used
        self.assertTemplateUsed(response, 'basic/index.html')

    def test_home_page_can_save_a_POST_request_and_redirect_after_POST(self):
        # Creates request object, assigns the method
        request = HttpRequest()
        request.method = 'POST'
        # Gives email input
        request.POST['email_address'] = 'ankurranjan19972016@gmail.com'
        # Define the valid email format
        pattern = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

        # Checks whether the email is in valid format
        if re.match(pattern, request.POST['email_address']):
            response = home(request)

            # Checks if the SubscribeEmail object exists
            self.assertEqual(SubscribedEmail.objects.count(), 1)
            new_item = SubscribedEmail.objects.first()
            # print(new_item.text)
            # The object queried is same as the user input email
            self.assertEqual(new_item.email_address, 'ankurranjan19972016@gmail.com')
            # print(response.status_code)

            # If the view redirects when the email inout is valid
            self.assertEqual(response.status_code, 302)
            # If the redirect location is valid
            self.assertEqual(response['location'], '/')
        else:
            # If the test fails the automatically declares tet failure
            self.fail("test failed")

    def test_home_page_uses_correct_form(self):
        response = self.client.get('/')
        # Check if the home view uses valid form
        self.assertIsInstance(response.context['add_form'], EmailSubscriberAddForm)

    # If proper action is taken when error is encountered like blank input
    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/', data={'email_address': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basic/index.html')
        expected_error = escape("This field is required.")
        self.assertContains(response, expected_error)


TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class TestCalls(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    # To Test the if the parse_template method is called by mocking it using Mock library

    @mock.patch('basic.views.append_to_chart')
    @mock.patch('basic.views.parse_and_append_templates')
    @mock.patch('basic.views.append_template')
    @mock.patch('basic.views.parse_template')
    def test_view_direct_is_valid(self, mock_parse_temp, mock_append_temp, mock_parse_and_append_temp, mock):
        # def test_view_direct_is_valid(self):

        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        user = User.objects.create_user(**self.credentials)
        # send login data

        subscribed_user = SubscribedEmail.objects.create(email_address='ankurranjan19972016@gmail.com')

        # Testing the success login log with Email_Template as sender using mock library
        with mock.patch('activitytrack.models.UserTemplatesUploadActivity.successful_login_log',
                        autospec=True) as mocked_handler:
            post_save.connect(mocked_handler, sender=EmailTemplates,
                              dispatch_uid='test_view_direct_is_valid_mocked_handler')

        # Creating request with custom 'Http_User_Agent'
        request = self.factory.get(reverse('basic:upload_templates'), HTTP_USER_AGENT='Mozilla/5.0')
        self.client.post('/login/', self.credentials, follow=True)
        request.user = user

        test_image_path = os.path.join(TEST_DIR, 'email1.html')

        # Creating Test File version using Mock

        # file_mock = mock.MagicMock(spec=File)
        # file_mock.name = 'test.html'
        # request.method = 'POST'
        # Giving fie_mock as template input
        with open(test_image_path, 'rb') as f:
            # print(File(f))
            # print(type(File(f)))
            # print(type(f))
            request.method = 'POST'
            file_mock = File(f)
            file_mock.name = 'email1.html'
            request.FILES['templates'] = file_mock

            response = uploadTemplates(request)

        self.assertEqual(mock_parse_temp.call_count, 1)
        # print(mock_parse_temp.call_args)
        # self.assertEqual(mock_append_temp.call_count, 1)

        # Testing if the postrequest worked
        self.assertTrue(EmailTemplates.objects.filter(templates_owner=request.user).exists())

        self.assertEqual(mocked_handler.call_count, 1)  # Test if the signal was called
        # self.assert_equal(mocked_handler.call_count, 1)  # when using django-nose

        parse_template(EmailTemplates.objects.first().id)
        append_template(EmailTemplates.objects.first().id)

        self.assertEqual(mock_append_temp.call_count, 1)
        self.assertEqual(mock_parse_and_append_temp.call_count, 1)
        self.assertTrue(SendEmail.objects.filter(mail_send_user=user, number_of_mail=1).exists())
        self.assertTrue(mock.called)

        # Testing if the redirection takes place after valid request
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')
