from django.shortcuts import render, redirect
from .models import Note, Photo, Profile, VocabularyEntry
from django.views.generic import ListView, DetailView
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy, reverse
from .forms import ExtendedUserCreationForm, ProfileForm, NoteForm, VocabularyEntryForm
import uuid
import boto3

S3_BASE_URL = "https://s3.us-east-1.amazonaws.com/"
BUCKET = "sicky-note-board-image-bucket"

VocabularyEntryFormSet = inlineformset_factory(Note, VocabularyEntry, form=VocabularyEntryForm, extra=1, can_delete=True)


# Create your views here.
def about(request):
    return render(request, "about.html")


@login_required
@login_required
def profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        logger.error(f"Profile does not exist for user: {request.user}")
        return render(request, "profile.html", {"error": "Profile does not exist."})

    profile_form = ProfileForm(request.POST or None, instance=profile)

    if request.method == "POST" and profile_form.is_valid():
        profile_form.save()
        return redirect("profile")  # Redirect to the profile page after saving

    return render(
        request, "profile.html", {"profile": profile, "profile_form": profile_form}
    )


@login_required
def home(request):
    notes = Note.objects.all()
    background = Profile.objects.get(user=request.user).background
    return render(request, "home.html", {"notes": notes, "background": background})


@login_required
def notes_index(request):
    try:
        notes = Note.objects.filter(user=request.user)
        profile = Profile.objects.get(user=request.user)
        location = profile.location
    except Profile.DoesNotExist:
        location = "New York"
    return render(
        request,
        "notes/index.html",
        {
            "notes": notes,
            "calendar": profile.calendar_view,
            "weather": profile.weather_view,
            "background": profile.background,
            "location": location,
        },
    )


@login_required
def notes_detail(request, note_id):
    background = Profile.objects.get(user=request.user).background
    note = Note.objects.get(id=note_id)
    return render(
        request, "notes/detail.html", {"note": note, "background": background}
    )


def signup(request):
    if request.method == "POST":
        form = ExtendedUserCreationForm(request.POST)
        # profile_form = ProfileForm(request.POST)
        if form.is_valid():
            user = form.save()
            # profile = profile_form.save(commit=False)
            # profile.user = user
            # profile.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("notes_index")
    else:
        form = ExtendedUserCreationForm()
        # profile_form = ProfileForm()
    context = {"form": form}
    return render(request, "signup.html", context)


def add_photo(request, note_id):
    photo_file = request.FILES.get("photo-file", None)
    if photo_file:
        s3 = boto3.client("s3")
        key = uuid.uuid4().hex + photo_file.name[photo_file.name.rfind(".") :]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, note_id=note_id)
            note_photo = Photo.objects.filter(note_id=note_id)
            if note_photo.first():
                note_photo.first().delete()
            photo.save()
        except Exception as err:
            print("An error occurred uploading file to S3: %s" % err)
    return redirect("notes_detail", note_id=note_id)


def note_type_selection(request):
    if request.method == "POST":
        note_type = request.POST.get("note_type")
        if note_type:
            return redirect(reverse("notes_create") + f"?type={note_type}")
    return render(request, "main_app/note_type_selection.html")


class NoteCreate(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = "main_app/note_form.html"
    success_url = "/notes/"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['vocab_entries'] = VocabularyEntryFormSet(self.request.POST)
        else:
            data['vocab_entries'] = VocabularyEntryFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        vocab_entries = context['vocab_entries']
        self.object = form.save()
        if vocab_entries.is_valid():
            vocab_entries.instance = self.object
            vocab_entries.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse("notes_detail", kwargs={"note_id": self.object.id})


class NoteUpdate(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = "main_app/note_form.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['vocab_entries'] = VocabularyEntryFormSet(self.request.POST, instance=self.object)
        else:
            data['vocab_entries'] = VocabularyEntryFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        vocab_entries = context['vocab_entries']
        self.object = form.save()
        if vocab_entries.is_valid():
            vocab_entries.instance = self.object
            vocab_entries.save()
        return super().form_valid(form)


class NoteDelete(LoginRequiredMixin, DeleteView):
    model = Note
    success_url = reverse_lazy("notes_index")

    def delete(self, request, *args, **kwargs):
        note = get_object_or_404(Note, pk=kwargs["pk"])
        if note.user != request.user:
            return HttpResponseForbidden("You are not allowed to delete this note.")
        return super().delete(request, *args, **kwargs)


class Login(LoginView):
    template_name = "login.html"


class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ("calendar_view", "weather_view", "background", "location")
