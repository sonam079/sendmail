from django.conf.urls import url
from django.contrib import admin

from .views import (
    TemplatesListView,
    TemplatesUploadView,
    SubscribedEmailListView,
    SubscribedEmailCreateView,
    # SendTemplate

)

urlpatterns = [
    url(r'^subscribed_email_list/$', SubscribedEmailListView.as_view(), name='subscribed_email_list'),
    url(r'^subscribed_email/create/$', SubscribedEmailCreateView.as_view(), name='subscribed_email_create'),
    url(r'^templates_list/$', TemplatesListView.as_view(), name='templates_list'),
    url(r'^templates_list/upload/$', TemplatesUploadView.as_view(), name='templates_list_upload'),
    # url(r'^templates_list/parse/(?P<pk>\d+)', TemplatesParseView.as_view(), name='templates_parse')
    # url(r'^send_template/(?P<pk>.+)$', SendTemplate.as_view(), name='send_template')

]
