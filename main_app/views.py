from django.http import request
from django.shortcuts import render, redirect
from .models import Note, Photo, Profile
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from .forms import ExtenedUserCreationForm, ProfileForm
import uuid
import boto3

S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'sicky-note-board-image-bucket'

# Create your views here.
def about(request):
  return render(request, 'about.html')

class ProfileUpdate(LoginRequiredMixin, UpdateView):
  model = Profile
  fields = ['calendar_view', 'weather_view','background']

@login_required
def profile(request):
  return render(request, 'profile.html')

@login_required
def home(request):
  notes = Note.objects.all()
  return render(request, 'home.html', { 'notes': notes })

@login_required
def notes_index(request):
  notes = Note.objects.filter(user=request.user)
  return render(request, 'notes/index.html', { 'notes': notes })

@login_required
def notes_detail(request, note_id):
  note = Note.objects.get(id=note_id)
  return render(request, 'notes/detail.html', { 'note': note })


def signup(request):
  # error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = ExtenedUserCreationForm(request.POST)
    profile_form = ProfileForm(request.POST)

    if form.is_valid() and profile_form.is_valid():
      # This will add the user to the database
      user = form.save()

      profile = profile_form.save(commit=False)
      profile.user = user

      profile.save()

      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password1')
      user = authenticate(username=username, password=password)
      # This is how we log a user in
      login(request, user)
      return redirect('notes_index')
    else:
      # error_message = 'Invalid sign up - try again'
      form = ExtenedUserCreationForm()
      profile_form = ProfileForm()
  # A bad POST or a GET request, so render signup.html with an empty form
  form = ExtenedUserCreationForm()
  profile_form = ProfileForm()
  context = {'form': form, 'profile_form': profile_form}
  
  return render(request, 'signup.html', context)

def add_photo(request, note_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind('.'):]
    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = Photo(url=url, note_id=note_id)
      note_photo = Photo.objects.filter(note_id=note_id)
      if note_photo.first():
        note_photo.first().delete()
      photo.save()
    except Exception as err:
      print('An error occurred uploading file to S3: %s' % err)
  return redirect('notes_detail', note_id=note_id)

class NoteCreate(LoginRequiredMixin, CreateView):
  model = Note
  fields = ['name','notetype','content','date', 'color','homescreen']
  success_url = '/notes/'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
    
class NoteUpdate(LoginRequiredMixin, UpdateView):
  model = Note
  fields = ['name','notetype','content','date', 'color','homescreen']

class NoteDelete(LoginRequiredMixin, DeleteView):
  model = Note
  success_url = '/notes/'

class Login(LoginView):
  template_name = 'login.html'

