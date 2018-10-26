from django.conf.urls import url
from .views import UserProfile
from account.api.views import ObtainJWTView

urlpatterns = [
    url(r'^login/$', view=ObtainJWTView.as_view(), name="login"),
    url(r'^detail/$', UserProfile.as_view(), name="user-details"),
]
