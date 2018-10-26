from rest_framework import mixins, viewsets
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView
)
# Use for Permission
from rest_framework.permissions import (
    AllowAny, IsAuthenticated
)

from .serializers import TemplatesSerializer, EmailSerializer

from basic.models import EmailTemplates, SubscribedEmail

from basic.views import parse_template

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)


class TemplatesListView(ListAPIView):
    print("TemplatesListView")
    serializer_class = TemplatesSerializer
    queryset = EmailTemplates.objects.all()
    permission_classes = [IsAuthenticated]


class TemplatesUploadView(CreateAPIView):
    print("TemplatesUploadView")
    serializer_class = TemplatesSerializer
    permission_classes = [IsAuthenticated]

    # After uploading the templates via DRF, run the parse_template function
    def perform_create(self, serializer):
        instance = serializer.save()
        print("Instance id in DRF", instance.pk)
        parse_template(instance.pk)
        req = self.request
        print("Request", req)


class SubscribedEmailListView(ListAPIView):
    serializer_class = EmailSerializer
    queryset = SubscribedEmail.objects.all()
    permission_classes = [IsAuthenticated]


class SubscribedEmailCreateView(CreateAPIView):
    serializer_class = EmailSerializer
    permission_classes = [IsAuthenticated]

# class SendTemplate()
