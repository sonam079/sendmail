from django.test import TestCase
from basic.forms import EmailSubscriberAddForm, EmailTemplatesUploadForm
from django.core.files import File
import mock


class EmailSubscriber_Form_Test(TestCase):
    # Tests if the form renders email input by checking the placeholder text
    def test_form_renders_email_input(self):
        form = EmailSubscriberAddForm()
        self.assertIn('placeholder="spam.free@yourmail.com"', form.as_p())
        # self.assertIn('class="col-md-12"', form.as_p())
        # self.fail(form.as_p())

    # If the Form not accepts the blank error
    def test_form_validation_for_blank_items(self):
        form = EmailSubscriberAddForm(data={'email_address': ''})
        self.assertFalse(form.is_valid())
        # Tests if the error message renders displayed is correct
        self.assertEqual(form['email_address'].errors, ['This field is required.'])

    # If the form denies repeated email ids
    def test_if_form_doesnot_accepts_existing_email(self):
        form = EmailSubscriberAddForm(data={'email_address': 'abc@gmail.com'})
        self.assertTrue(form.is_valid())
        form.save()
        # Giving already existing Email-Id as input
        form = EmailSubscriberAddForm(data={'email_address': 'abc@gmail.com'})
        self.assertFalse(form.is_valid())
        # Tests if the error message renders displayed is correct
        self.assertEqual(form['email_address'].errors, ['User with this email already exists.'])

    # If the Form rejects invalid Email formats by giving an invalid format
    def test_if_form_accepts_invalid_email(self):
        form = EmailSubscriberAddForm(data={'email_address': 'abc7483'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form['email_address'].errors, ['Enter a valid email address.'])


class Template_upload_form_Test(TestCase):
    # To Test if the form saves file with .html extension
    def test_upload_form(self):
        file_mock = mock.MagicMock(spec=File)  # Creating a file for testing using Mock
        file_mock.name = 'test.html'
        form = EmailTemplatesUploadForm(files={'templates': file_mock})
        self.assertTrue(form.is_valid())

    # Tests if Form does not saves file with other extensions than .html
    def test_form_accepting_blank_or_invalid_input(self):
        file_mock = mock.MagicMock(spec=File)  # Creating a file for testing using Mock
        file_mock.name = 'test.pdf'
        form = EmailTemplatesUploadForm(files={'templates': file_mock})
        self.assertFalse(form.is_valid())

        # Forms does not saves empty input
        form = EmailTemplatesUploadForm(files={'templates': ''})
        self.assertFalse(form.is_valid())
