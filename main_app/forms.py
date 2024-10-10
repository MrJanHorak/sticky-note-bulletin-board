from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Note

class ExtendedUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    location = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            profile = Profile.objects.create(user=user, location=self.cleaned_data['location'])
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('calendar_view', 'weather_view', 'background')

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['name', 'notetype', 'content', 'date', 'color', 'homescreen', 'vocab', 'photocard_caption', 'to_do']
        widgets = {
            'notetype': forms.Select(attrs={'id': 'id_notetype'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
        }