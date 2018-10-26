from django.contrib.auth.models import User
from django.db import models
from basic.validators import validate_file_extension
# Create your models here.

# Model Class for Email which subscribed to my site
class SubscribedEmail(models.Model):
    email_address = models.EmailField(unique=True)

    def __str__(self):
        return str(self.email_address)


# Model Class for Saving Uploaded Email
class EmailTemplates(models.Model):
    templates_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    templates = models.FileField(validators=[validate_file_extension])
    number_of_times_templates_send = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return str(self.templates)


# Model Class for Saving Uploaded Image
class SaveImageFromTemplates(models.Model):
    parentTemplates = models.ForeignKey(EmailTemplates, on_delete=models.CASCADE, default=None)
    imageSource = models.CharField(max_length=10000)

    def __str__(self):
        return str(self.imageSource)


# Model for Email Send
class SendEmail(models.Model):
    template = models.ForeignKey(EmailTemplates, on_delete=models.DO_NOTHING)
    mail_send_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    number_of_mail = models.IntegerField(default=0)

    def __str__(self):
        return str(self.template)
