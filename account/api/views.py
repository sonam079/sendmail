from rest_framework.generics import ListAPIView
from account.api.serializers import UserDetailsSerilaizer
from django.contrib.auth.models import User

from rest_framework_jwt.views import ObtainJSONWebToken

from .serializers import JWTSerializer


# Create your views here.
class ObtainJWTView(ObtainJSONWebToken):
    serializer_class = JWTSerializer


class UserProfile(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailsSerilaizer
