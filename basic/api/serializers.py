from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField

from basic.models import EmailTemplates, SubscribedEmail


class TemplatesSerializer(ModelSerializer):
    # send_this_templates_url = HyperlinkedIdentityField(
    #     view_name="api-basic:"
    # )

    class Meta:
        model = EmailTemplates
        fields = '__all__'


class EmailSerializer(ModelSerializer):
    class Meta:
        model = SubscribedEmail
        fields = '__all__'
