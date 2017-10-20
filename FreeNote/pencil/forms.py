# -*- coding: utf-8 -*-

from django import forms

from ckeditor.fields import RichTextFormField

class NoteForm(forms.Form):
	title = forms.CharField(max_length=128, required=True)
	content = RichTextFormField()
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)