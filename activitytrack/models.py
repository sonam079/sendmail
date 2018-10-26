from django.contrib.auth.models import User
from django.db import models
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
from datetime import datetime
# Create your models here.

# Track login User activity
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from basic.models import EmailTemplates, SendEmail


class UserLoginActivity(models.Model):
    # Login Status
    SUCCESS = 'S'
    FAILED = 'F'

    LOGIN_STATUS = ((SUCCESS, 'Success'),
                    (FAILED, 'Failed'))

    login_IP = models.GenericIPAddressField(null=True, blank=True)
    login_datetime = models.DateTimeField(auto_now=True)
    login_username = models.CharField(max_length=40, null=True, blank=True)
    status = models.CharField(max_length=1, default=SUCCESS, choices=LOGIN_STATUS, null=True, blank=True)
    user_agent_info = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'user_login_activity'
        verbose_name_plural = 'user_login_activities'

    def __str__(self):
        return str(self.id)


class UserTemplatesUploadActivity(models.Model):
    request_track_user = models.ForeignKey(UserLoginActivity, on_delete=models.DO_NOTHING)
    request_user_name = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(default=datetime.now())
    templates_upload_status = models.BooleanField(default=False)
    number_of_templates_upload = models.IntegerField(default=0)
    send_mail_status = models.BooleanField(default=False)
    number_of_mail_send = models.IntegerField(default=0)
    templates = models.TextField(default='', null=True, blank=True)

    def __str__(self):
        return str(self.id)

    @receiver(post_save, sender=UserLoginActivity)
    @receiver(post_save, sender=EmailTemplates)
    @receiver(post_save, sender=SendEmail)
    def successful_login_log(sender, instance, created, **kwargs):
        if created:
            if sender.__name__ == 'UserLoginActivity':
                user = User.objects.get(id=get_current_authenticated_user().id)
                UserTemplatesUploadActivity.objects.create(request_user_name=user, request_track_user=instance)
            if sender.__name__ == 'EmailTemplates':
                profile = UserTemplatesUploadActivity.objects.filter(request_user_name=instance.templates_owner).last()
                profile.templates_upload_status = True
                profile.number_of_templates_upload = profile.number_of_templates_upload + 1
                profile.templates = profile.templates + str(instance.templates) + ' ,'
                profile.save()

            if sender.__name__ == 'SendEmail':
                profile = UserTemplatesUploadActivity.objects.filter(
                    request_user_name_id=instance.mail_send_user_id).last()
                profile.send_mail_status = True
                profile.number_of_mail_send = profile.number_of_mail_send + instance.number_of_mail
                profile.save()

    post_save.connect(successful_login_log, sender=UserLoginActivity)
    post_save.connect(successful_login_log, sender=EmailTemplates)
