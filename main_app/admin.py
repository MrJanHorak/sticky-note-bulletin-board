from django.contrib import admin

# import  your models here
from .models import Note, Photo

# Register your models here.
admin.site.register(Note)
admin.site.register(Photo)