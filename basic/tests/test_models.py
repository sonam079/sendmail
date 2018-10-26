from django.test import TestCase
from basic.models import SubscribedEmail, EmailTemplates, SendEmail
import mock
from django.contrib.auth.models import User
from django.core.files import File


# To Test the models
class SubscribedEmailModelsTest(TestCase):
    # Tests the models by creating two instances of subscribe_email object and saving them
    def test_saving_and_retreiving_models(self):
        first_subsribed_email = SubscribedEmail()
        first_subsribed_email.email_address = 'abc@gmail.com'
        first_subsribed_email.save()

        second_subsribed_email = SubscribedEmail()
        second_subsribed_email.email_address = 'edf@gmail.com'
        second_subsribed_email.save()

        saved_items = SubscribedEmail.objects.all()
        # Checks whether the instances are saved
        self.assertEqual(saved_items.count(), 2)

        # Tests whether the instances in database are same as the ones created earlier
        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.email_address, 'abc@gmail.com')
        self.assertEqual(second_saved_item.email_address, 'edf@gmail.com')


class EmailTemplates_and_SendMail_ModelsTest(TestCase):
    # Tests the models by creating two instances of email_template object and saving them
    def test_saving_and_retreiving_models(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        user = User.objects.create_user(**self.credentials)

        self.client.post('/login/', self.credentials, follow=True)

        file_mock1 = mock.MagicMock(spec=File)
        file_mock1.name = 'test1.html'
        first_email_template = EmailTemplates()
        first_email_template.templates = file_mock1
        first_email_template.templates_owner = user
        first_email_template.save()

        file_mock2 = mock.MagicMock(spec=File)
        file_mock2.name = 'test2.html'
        second_email_template = EmailTemplates()
        second_email_template.templates = file_mock2
        second_email_template.templates_owner = user
        second_email_template.save()

        saved_items = EmailTemplates.objects.all()
        self.assertEqual(saved_items.count(), 2)  # Checks whether the instances are saved

        first_send_email = SendEmail()
        first_send_email.template = first_email_template
        first_send_email.mail_send_user = user
        first_send_email.number_of_mail = 1
        first_send_email.save()

        second_send_Email = SendEmail()
        second_send_Email.template = second_email_template
        second_send_Email.mail_send_user = user
        second_send_Email.number_of_mail = 1
        second_send_Email.save()

        saved_email_items = SendEmail.objects.all()
        self.assertEqual(saved_email_items.filter(mail_send_user=user).count(), 2)
