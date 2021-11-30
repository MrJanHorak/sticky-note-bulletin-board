from django.contrib import admin

# import  your models here
from .models import Note, Photo, Profile

# Register your models here.
admin.site.register(Note)
admin.site.register(Photo)
admin.site.register(Profile)