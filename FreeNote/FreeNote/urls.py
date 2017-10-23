# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin

import registration
from pencil import views, urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.Home, name="Home"),
    url(r'^index/', include('pencil.urls')),
    url(r'^accounts/register/$', views.register, name='registration_register'),
    url(r'^activate/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$', views.activate_user, name='activate_user'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
]
