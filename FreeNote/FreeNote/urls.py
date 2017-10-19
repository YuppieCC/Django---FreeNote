# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin

import registration
from pencil import views, urls


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.Home, name="Home"),
    url(r'^index/', include('pencil.urls')),

    url(r'^accounts/', include('registration.backends.simple.urls')),
]
