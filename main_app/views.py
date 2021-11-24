from django.http import request
from django.shortcuts import render, redirect
from .models import Note, Photo
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
import uuid
import boto3

# Create your views here.
def about(request):
  return render(request, 'about.html')

@login_required
def notes_index(request):
  notes = Note.objects.filter(user=request.user)
  return render(request, 'notes/index.html', { 'notes': notes })

@login_required
def notes_detail(request, note_id):
  note = Note.objects.get(id=note_id)
  return render(request, 'notes/detail.html', { 'note': note })

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in
      login(request, user)
      return redirect('notes_index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)

class NoteCreate(LoginRequiredMixin, CreateView):
  model = Note
  fields = ['name','notetype','content','date', 'color']
  success_url = '/notes/'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
    
class NoteUpdate(LoginRequiredMixin, UpdateView):
  model = Note
  fields = ['name','content']

class NoteDelete(LoginRequiredMixin, DeleteView):
  model = Note
  success_url = '/notes/'

class Home(LoginView):
  template_name = 'home.html'
