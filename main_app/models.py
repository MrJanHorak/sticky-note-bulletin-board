from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
NOTETYPE = (
  ('T', 'To-Do'),
  ('R', 'Reminder'),
  ('L', 'Vocab/Learning'),
  ('P', 'Photocard'),
)

COLOR = (
  ('#EAEC40', 'Dandelion'),
  ('#FF7EB9', 'pink'),
  ('#F275AD', 'Cyclamen'),
  ('#79CBC5', 'Pearl Aqua'),
  ('#FFFF97', 'Canary'),
  ('#7AFCFF', 'blue'),
  ('#FBAE4A', 'Pastel Orange'),
  ('#F3858E', 'Tulip'),
  ('#8D9440', 'Bright Green'),
)

HOMESCREEN = (
  ('Y', 'Yes'),
  ('N', 'No'),
)

class Note(models.Model):
  name = models.CharField(max_length=100)
  notetype = models.CharField(
    max_length=1,
    choices= NOTETYPE,
    default=NOTETYPE[1][0]
  )
  content=models.TextField(max_length=400)
  date=models.DateField('Due date')
  color=models.CharField(
    max_length=7,
    choices = COLOR,
    default=COLOR[2][0]
  )
  homescreen = models.CharField(
    max_length=1,
    choices= HOMESCREEN,
    default=HOMESCREEN[1][0]
  )
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('notes_detail', kwargs={'note_id': self.id})

  class Meta:
    ordering = ['-date']

class Photo(models.Model):
  url = models.CharField(max_length=250)
  note = models.OneToOneField(Note, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for note_id: {self.note_id} @{self.url}"