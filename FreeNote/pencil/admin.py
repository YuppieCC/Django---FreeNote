# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from pencil.models import UserProfile, Note


admin.site.register(UserProfile)
admin.site.register(Note)