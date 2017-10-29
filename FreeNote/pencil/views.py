# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, forms
from django.views import generic
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import OperationalError

from registration.forms import RegistrationForm

from send_email import Token, send_html_email
from forms import NoteForm
from models import Note


token_confirm = Token(settings.SECRET_KEY)

class CkEditorFormView(generic.FormView):
	form_class = NoteForm
	template_name = 'site/add_note.html'

	def get_success_url(self):
		return reverse('note')

def Home(request):
	return render(request, 'site/home.html')

@login_required
def index(request):
	return render(request, 'site/index.html')

@login_required
def about(request, username):
	return render(request, 'site/about.html')

def register(request):
	if request.method == 'POST':
		user_form = RegistrationForm(request.POST)
		if user_form.is_valid():
			username = user_form.cleaned_data.get('username')
			email = user_form.cleaned_data.get('email')
			password = user_form.cleaned_data.get('password1')
			user = User.objects.create_user(username=username, password=password, email=email)
			user.is_active = False
			user.save()
			token = token_confirm.generate_validate_token(username)

			subject = u'欢迎加入<FreeNote>'
			link = '/'.join([settings.DOMAIN, 'activate', token])
			html_content = u'<p>{0}, 欢迎加入 FreeNote ，请访问该链接，完成用户验证:</p>\
				<br><a href="{1}">点击链接完成验证</a>'.format(username, link)
			to_list = []
			to_list.append(email)
			send_html_email(subject, html_content, to_list)
			return render(request, 'site/message.html', {'message': u'请登录你的邮箱按提示进行操作'})
	else:
		user_form = RegistrationForm()
	context_dict = {'form': user_form}
	return render(request, 'registration/registration_form.html', context_dict)

def password_reset(request):
	try:
		if request.method == 'POST':
			email = request.POST['email']
			user = User.objects.get(email=email)
			token = token_confirm.generate_validate_token(user.username)
			# send email
			subject = u'<FreeNote>用户重设密码信息'
			link = '/'.join([settings.DOMAIN, 'passwordreset', user.username, token])
			html_content = u'<p>{0}, 欢迎使用 FreeNote ，请访问该链接，完成用户重设密码:</p>\
				<br><a href="{1}">点击链接完成验证</a>'.format(user.username, link)
			to_list = []
			to_list.append(email)
			send_html_email(subject, html_content, to_list)
			return render(request, 'site/message.html', {'message': u'请登录你的邮箱按提示进行操作'})

		else:
			return render(request, 'registration/password_reset.html')

	except User.DoesNotExist:
		message = 'User with this Email address does not exists'
		return render(request, 'registration/password_reset.html', {'message': message})

def password_reset_done(request, username, token):
	try:
		user = User.objects.get(username=username)
		user_confirm = token_confirm.confirm_validate_token(token)
		if request.method == 'POST':
			form = forms.SetPasswordForm(user, request.POST)
			if form.is_valid():
				user.set_password(form.cleaned_data.get('new_password1'))
				user.save()
				login(request, user)
				return redirect('index')
			else:
				return render(request, 'registration/password_reset_done.html', {'form': form})

		else:
			form = forms.SetPasswordForm(user)
			return render(request, 'registration/password_reset_done.html', {'form': form})

	except User.DoesNotExist:
		return render(request, 'site/message.html', {'message': u'这个账户不存在'})

	except:
		user_confirm = token_confirm.remove_validate_token(token)
		users = User.objects.filter(username=username)
		for user in users:
			user.delete()
		return render(request, 'site/message.html', {'message': u'你的验证链接已过期'})

def activate_user(request, token):
	try:
		username = token_confirm.confirm_validate_token(token)
	except:
		username = token_confirm.remove_validate_token(token)
		users = User.objects.filter(username=username)
		for user in users:
			user.delete()
		return render(request, 'site/message.html', {'message': u'你的验证链接已过期'})
	try:
		user = User.objects.get(username=username)
		user.is_active = True
		user.save()
		login(request, user)
		return render(request, 'site/note_list.html', {'message': u'恭喜，你的账户已成功激活。'})
	
	except User.DoesNotExist:
		return render(request, 'blah/message.html', {'message': u'这个账户不存在'})


@login_required
def note(request, username, note_id):
	author = User.objects.get(username=username)
	note = Note.objects.get(id=note_id)

	context_dict = {'note': note}
	return render(request, 'site/note.html', context_dict)

@login_required
def note_list(request, username=None):
	try:
		author = User.objects.get(username=username)
		notes = Note.objects.filter(author_id=author.id)
		# add a new note
		if request.method == 'POST':
			title = request.POST['title']
			content = request.POST['content']
			content_excerpts = content[:200]
			note_initial = {
				'title': title, 
				'content': content,
			}
			# check title's length
			if len(title) > 128:
				note_form = NoteForm(initial=note_initial)
				context_dict = {'message': u'标题字数过多，请不要超过 128 个字符', 'form': note_form}
				return render(request, 'site/add_note.html', context_dict)
			else:
				# add a note
				note = Note(
					author_id = author.id,
					title = title,
					content = content,
					content_excerpts = content_excerpts,
				)
				note.save()
				return redirect('note_list', username=username)
		
		context_dict = {'notes': notes, 'author': author}
		return render(request, 'site/note_list.html', context_dict)

	except OperationalError:
		note_form = NoteForm(initial=note_initial)
		context_dict = {'message': u'对不起，你所输入的符号（如表情符号）暂不支持', 'form': note_form}
		return render(request, 'site/add_note.html', context_dict)

	except User.DoesNotExist:
		raise Http404("Not exists.")

	except Note.DoesNotExist:
		raise Http404("Not exists.")

@login_required
def update_note(request, username, note_id):
	# commit update
	try:
		if request.method == 'POST':
			new_title = request.POST['title']
			new_content = request.POST['content']
			new_content_excerpts = new_content[:200]
			# check title's length
			new_note_initial = {
				'title': new_title,
				'content': new_content,
			}
			if len(new_title) > 128:
				note_form = NoteForm(initial=new_note_initial)
				context_dict = {'message': u'标题字数过多，请不要超过 128 个字符', 'form': note_form}
				return render(request, 'site/edit_note.html', context_dict)
			
			else:
				Note.objects.filter(id=note_id).update(
					title = new_title,
					content = new_content,
					content_excerpts = new_content_excerpts,
				)
				return redirect('note', username=username, note_id=note_id)

		else:
			author = User.objects.get(username=username)
			note = Note.objects.get(id=note_id)
			note_initial = {
				'title': note.title,
				'content': note.content,
			}
			form = NoteForm(initial=note_initial)
			content_dict = {'note_id': note_id, 'form': form}
			return render(request, 'site/edit_note.html', content_dict)

	except OperationalError:
		note_form = NoteForm(initial=new_note_initial)
		context_dict = {'message': u'对不起，你所输入的符号（如表情符号）暂不支持', 'form': note_form}
		return render(request, 'site/edit_note.html', context_dict)

@login_required
def delete_note(request, username, note_id):
	try:
		note = Note.objects.get(id=note_id) 
		if request.method == 'POST':
			note.delete()
			return redirect('note_list', username=username)
		
		content_dict = {'note': note, 'username': username}
		return render(request, 'site/note_delete_confirm.html', content_dict)

	except Note.DoesNotExist:
		raise Http404('This is note does not exist.')


def page_not_found(request):
	return render(request, 'site/message.html', {'message': '404 Page not found'})

def server_error(request):
	return render(request, 'site/message.html', {'message': '500 Server Error'})

def permission_denied(request):
	return render(request, 'site/message.html', {'message': '403 Permission denied'})

def bad_request(request):
	return redner(request, 'site/message.html', {'message': '400 Bad request'})


