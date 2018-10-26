from django.contrib import admin
from basic.models import SubscribedEmail, EmailTemplates, SaveImageFromTemplates, SendEmail

# Register your models here.
admin.site.register(SubscribedEmail)
admin.site.register(EmailTemplates)
admin.site.register(SaveImageFromTemplates)
admin.site.register(SendEmail)
