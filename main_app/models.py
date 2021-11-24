from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
NOTETYPE = (
  ('T', 'To-Do'),
  ('R', 'Reminder'),
  ('L', 'Vocab/Learning')
)

COLOR = (
  ('PI', 'pink'),
  ('BP', 'bright pink'),
  ('BY', 'yellow'),
  ('DY', 'dark yellow'),
  ('BL', 'blue'),
  ('GR', 'green'),

)
class Note(models.Model):
  name = models.CharField(max_length=100)
  notetype = models.CharField(
    max_length=1,
    choices= NOTETYPE,
    default=NOTETYPE[1][0]
  )
  content=models.TextField(max_length=300)
  date=models.DateField('Due date')
  color=models.CharField(
    max_length=2,
    choices = COLOR,
    default=COLOR[2][0]
  )
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('notes_detail', kwargs={'note_id': self.id})

