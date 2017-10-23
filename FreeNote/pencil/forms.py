# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User

from ckeditor.fields import RichTextFormField

class UserForm(forms.ModelForm):
	username = forms.CharField(max_length=128)
	email = forms.EmailField()
	first_name = forms.CharField(max_length=50, required=False)
	last_name = forms.CharField(max_length=50, required=False)

	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name')


class NoteForm(forms.Form):
	title = forms.CharField(max_length=128, required=True)
	content = RichTextFormField()
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)