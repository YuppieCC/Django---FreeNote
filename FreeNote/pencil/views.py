# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.conf import settings

def Home(request):
	return render(request, 'site/home.html')

def index(request):
	return render(request, 'site/index.html')