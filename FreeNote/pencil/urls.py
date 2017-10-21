# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^about/(?P<username>[\w]+)$', views.about, name="about"),

	url(r'^note/(?P<username>[\w]+)/$', views.note_list, name='note_list'),
	url(r'^note/(?P<username>[\w]+)/(?P<note_id>[\d]+)/$', views.note, name='note'),
	url(r'^note/(?P<username>[\w]+)/add/$', views.CkEditorFormView.as_view(), name='add_note'),
	url(r'^note/(?P<username>[\w]+)/(?P<note_id>[\d]+)/edit/$', views.update_note, name='edit_note'),
	url(r'^note/(?P<username>[\w]+)/(?P<note_id>[\d]+)/delete/$', views.delete_note, name='delete_note'),

]