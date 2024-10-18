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
    ("#C0C0C0", "Silver"),        # 1920s Art Deco
    ("#8B5A2B", "Sienna"),        # 1920s
    ("#3B444B", "Payne's Grey"),  # 1920s
    ("#FFDAB9", "Peach Puff"),    # 1950s
    ("#FF6347", "Tomato"),        # 1950s
    ("#FF69B4", "Hot Pink"),      # 1950s
    ("#FF4500", "Orange Red"),    # 1960s
    ("#FFFF66", "Light Yellow"),  # 1960s
    ("#FFB6C1", "Light Pink"),    # 1960s
    ("#8B4513", "Saddle Brown"),  # 1970s
    ("#D2B48C", "Tan"),           # 1970s
    ("#DEB887", "Burly Wood"),    # 1970s
    ("#FF00FF", "Magenta"),       # 1980s
    ("#00FFFF", "Cyan"),          # 1980s
    ("#FFD700", "Neon Gold"),     # 1980s
    ("#808080", "Cool Grey"),     # 1990s
    ("#CD5C5C", "Indian Red"),    # 1990s
    ("#4682B4", "Steel Blue"),    # 1990s
    ("#000000", "Black"),         
    ("#FF0000", "Red"),           
    ("#0000FF", "Royal Blue"),    
    ("#228B22", "Forest Green"),  
    ("#FFA500", "Orange"),        
    ("#FF4500", "Red Orange"),    
    ("#9932CC", "Dark Orchid"),   
    ("#8B4513", "Saddle Brown"),  
    ("#FFD700", "Gold"),          
    ("#708090", "Slate Grey"), 
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

class VocabularyEntry(models.Model):
    word = models.CharField(max_length=100)
    meaning = models.TextField()
    note = models.ForeignKey('Note', on_delete=models.CASCADE, related_name='vocab_entries')

    def __str__(self):
        return self.word

class Note(models.Model):
    name = models.CharField(max_length=100)
    notetype = models.CharField(max_length=1, choices=NOTETYPE, default=NOTETYPE[1][0])
    to_do = ArrayField(
        models.CharField(max_length=100, blank=True), blank=True, null=True
    )
    content = models.TextField(max_length=400, blank=True)
    date = models.DateField("Due date", blank=True, null=True)
    color = models.CharField(max_length=7, choices=COLOR, default=COLOR[0][0])
    font_color = models.CharField("Ink Color", max_length=7, choices=COLOR, default=COLOR[2][0])
    homescreen = models.CharField(
        max_length=1, choices=HOMESCREEN, default=HOMESCREEN[1][0]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photocard_caption = models.CharField(max_length=255, blank=True)

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
