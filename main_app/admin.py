from django.contrib import admin

# import  your models here
from .models import Note

# Register your models here.
admin.site.register(Note)