# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from uuslug import slugify
from ckeditor.fields import RichTextField
#from awesome_avatar.fields import AvatarField

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	#avatar = AvatarField(blank=True, upload_to='avatars', width=100, height=100)

	def __unicode__(self):		# __str__ on Python 3
		return self.user.username

class Note(models.Model):
	author = models.ForeignKey(User)
	title = models.CharField(max_length=128)
	content = RichTextField(blank=True, null=True)
	content_excerpts = RichTextField(blank=True, null=True)		# 文章摘记
	#category = models.CharField(max_length=50, blank=True)		# 类别
	pub_time = models.DateTimeField(auto_now_add=True)
	url_slug = models.SlugField(max_length=168, default="", allow_unicode=True)		# 如有需要可作为有效 URL 的一部分

	class Meta:
		ordering = ['-pub_time']	# 文章排序

	def save(self, *args, **kwargs):
		self.url_slug = slugify(self.title)
		super(Note, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.title

