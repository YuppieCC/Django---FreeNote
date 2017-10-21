# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import generic
from django.core.urlresolvers import reverse
from django.conf import settings

from forms import NoteForm
from models import Note

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

			# check title's length
			if len(title) > 128:
				# keep title and content
				note_initial = {
					'title': title, 
					'content': content,
				}
				note_form = NoteForm(initial=note_initial)
				context_dict = {'message': '标题字数过多，请不要超过 128 个字符', 'form': note_form}
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

	except User.DoesNotExist:
		raise Http404("Not exists.")

	except Note.DoesNotExist:
		raise Http404("Not exists.")

@login_required
def update_note(request, username, note_id):
	# commit update
	if request.method == 'POST':
		new_title = request.POST['title']
		new_content = request.POST['content']
		new_content_excerpts = new_content[:200]
		Note.objects.filter(id=note_id).update(
			title = new_title,
			content = new_content,
			content_excerpts = new_content_excerpts,
		)
		return redirect('note', username=username, note_id=note_id)

	author = User.objects.get(username=username)
	note = Note.objects.get(id=note_id)
	note_initial = {
		'title': note.title,
		'content': note.content,
	}
	
	form = NoteForm(initial=note_initial)
	content_dict = {'note_id': note_id, 'form': form}
	return render(request, 'site/edit_note.html', content_dict)

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



