from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

# Create your models here.
NOTETYPE = (
    ("T", "To-Do"),
    ("R", "Reminder"),
    ("L", "Vocab/Learning"),
    ("P", "Photocard"),
)

COLOR = (
    ("#EAEC40", "Dandelion"),
    ("#FF7EB9", "Pink"),
    ("#F275AD", "Cyclamen"),
    ("#79CBC5", "Pearl Aqua"),
    ("#FFFF97", "Canary"),
    ("#7AFCFF", "Blue"),
    ("#FBAE4A", "Pastel Orange"),
    ("#F3858E", "Tulip"),
    ("#B2EC5D", "Inchworm"),
    ("#8D9440", "Bright Green"),
    ("#FFFFFF", "White"),
    ("#BEBEBE", "Grey"),
)

HOMESCREEN = (
    ("Y", "Yes"),
    ("N", "No"),
)

YON = (
    ("Y", "Yes"),
    ("N", "No"),
)


class Note(models.Model):
    name = models.CharField(max_length=100)
    notetype = models.CharField(max_length=1, choices=NOTETYPE, default=NOTETYPE[1][0])
    to_do = ArrayField(
        models.CharField(max_length=100, blank=True), blank=True, null=True
    )
    content = models.TextField(max_length=400, blank=True)
    date = models.DateField("Due date", blank=True, null=True)
    color = models.CharField(max_length=7, choices=COLOR, default=COLOR[2][0])
    homescreen = models.CharField(
        max_length=1, choices=HOMESCREEN, default=HOMESCREEN[1][0]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vocab = models.JSONField(blank=True, null=True)  # For Vocab/Learning
    photocard_caption = models.CharField(max_length=255, blank=True)  # For Photocard

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("notes_detail", kwargs={"note_id": self.id})

    class Meta:
        ordering = ["-date"]


class Photo(models.Model):
    url = models.CharField(max_length=250)
    note = models.OneToOneField(Note, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for note_id: {self.note_id} @{self.url}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    calendar_view = models.CharField(max_length=1, choices=YON, default=YON[0][0])
    weather_view = models.CharField(max_length=1, choices=YON, default=YON[0][0])
    background = models.CharField(max_length=250, blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("profile")
