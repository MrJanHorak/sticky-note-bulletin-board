from typing import cast
from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Note

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return (request, 'about.html')

class NoteCreate(LoginRequiredMixin, CreateView):
  model = Note
  fields = '__all__'

def form_valid(self, form):
  form.instance.user = self.request.user
  return super().form_valid(form)

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

class Note:  # Note that parens are optional if not inheriting from another class
  def __init__(self, name, notetype, content, color):
    self.name = name
    self.notetype = notetype
    self.content = content
    self.color = color

def notes_index(request):
  notes = Note.objects.all()
  return render(request, 'notes/index.html', { 'notes': notes })

def notes_detail(request, note_id):
  note = Note.objects.get(id=note_id)
  return render(request, 'notes/detail.html', { 'note': note })

class NoteCreate(CreateView):
  model = Note
  fields = '__all__'
  success_url = '/notes/'

class NoteUpdate(UpdateView):
  model = Note
  fields = ['__all__']

class NoteDelete(DeleteView):
  model = Note
  success_url = '/notes/'

