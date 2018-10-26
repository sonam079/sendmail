"""sendmail URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from basic import views as basic_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, {'template_name': 'account/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'', include('basic.urls', namespace='basic')),
    url(r'^api/basic/', include('basic.api.urls', namespace='api-basic')),
    url(r'^api/account/', include('account.api.urls', namespace='account-basic'))

]

handler400 = basic_views.error400  # noqa
handler403 = basic_views.error403  # noqa
handler404 = basic_views.error404  # noqa
handler500 = basic_views.error500  # noqa
handler200 = basic_views.error200  # noqa

# when debug is True

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
