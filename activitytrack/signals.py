from django.contrib.auth import user_logged_in, user_login_failed
from django.dispatch import receiver

from activitytrack.helper import get_client_ip

# Track login User activity
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from activitytrack.models import UserLoginActivity, UserTemplatesUploadActivity

from basic.models import EmailTemplates

import requests


# receiver for user_login_successfully signal
@receiver(user_logged_in)
def log_user_logged_in_success(sender, user, request, **kwargs):
    try:
        user_agent_info = request.META.get('HTTP_USER_AGENT', '<unknown>')[:255]
        user_login_activity_log = UserLoginActivity(login_IP=get_client_ip(request),
                                                    login_username=user.username,
                                                    user_agent_info=user_agent_info,
                                                    status=UserLoginActivity.SUCCESS)
        user_login_activity_log.save()
    except Exception as e:
        # log the error
        print("log_user_logged_in request: %s, error: %s" % (request, e))


# receiver for user_login_failed signal
@receiver(user_login_failed)
def log_user_logged_in_failed(sender, credentials, request, **kwargs):
    try:
        user_agent_info = request.META.get('HTTP_USER_AGENT', '<unknown>')[:255]
        user_login_activity_log = UserLoginActivity(login_IP=get_client_ip(request),
                                                    login_username=credentials['username'],
                                                    user_agent_info=user_agent_info,
                                                    status=UserLoginActivity.FAILED)
        user_login_activity_log.save()
    except Exception as e:
        # log the error
        print("log_user_logged_in request: %s, error: %s" % (request, e))

# @receiver(post_save, sender=UserLoginActivity)
# def create_user_after_login(sender, instance, **kwargs):
#     print("Instance status", instance.status)
#     if instance.status == 'S':
#         UserTemplatesUploadActivity.objects.create(request_track_user=instance, user_name=instance.login_username)
#
#
# post_save.connect(create_user_after_login, sender=UserLoginActivity)
#
#
# @receiver(post_save, sender=EmailTemplates)
# def track_user_templates_upload_activity(sender, instance, created, **kwargs):
#     if created:
#         print("Instance Template User", instance.templates_owner)
#         print("Templates", instance.templates)
#         abc= UserTemplatesUploadActivity.objects.filter(user_name = instance.templates_owner).order_by('-request_track_user_id')[:1]
#         print("ABC", abc)
#         templates = ''
#         try:
#             templates = abc['templates_upload']
#             print("templates", templates)
#         except:
#             print("No file present before")
#
#         UserTemplatesUploadActivity.objects.filter(pk__in=abc).update(templates_upload = str(instance.templates) + ', ' + templates, templates_upload_status = True, send_mail_status = True)
#         print("abc",abc)
# post_save.connect(track_user_templates_upload_activity, sender=EmailTemplates)
