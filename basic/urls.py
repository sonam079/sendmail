from django.conf.urls import url, include
from basic import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^upload_templates/$', views.uploadTemplates, name='upload_templates'),
    url(r'^send_template/(?P<pk>.+)$', views.send_template, name='send_template')
]

