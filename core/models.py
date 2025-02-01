from django.contrib.auth.models import AbstractUser
from django.db import models

# https://tvtropes.org/pmwiki/pmwiki.php/Administrivia/MediaCategories
mediaCategories = [
    ("Advertising", "Advertisement"),
    ("Animation", "Animation"),
    ("Anime", "Anime"),
    ("ARG", "ARG"), # added
    ("Art", "Art"), # added
    ("AudioPlay", "Audio play"), # added
    ("Blog", "Blog"),
    ("ComicBook", "Comic book"),
    ("ComicStrip", "Comic strip"),
    ("Fanfic", "Fanfic"), # added
    ("Film", "Film"),
    ("LetsPlay", "Let's play"), # added
    ("Literature", "Literature"),
    ("Magazine", "Magazine"),
    ("Manga", "Manga"),
    ("Manhua", "Manhua"),
    ("Manhwa", "Manhwa"),
    ("Music", "Music"),
    ("Myth", "Myth"), 
    ("Platform", "Platform"), # added
    ("Podcast", "Podcast"), # added
    ("Radio", "Radio"),
    ("Ride", "Ride"), # added
    ("Roleplay", "Roleplay"),
    ("Series", "TV Series"),
    ("TabletopGame", "Tabletop game"),
    ("Theatre", "Theater"), # lol
    ("Toys", "Toys"), # added
    ("VideoGame", "Video game"),
    ("VisualNovel", "Visual novel"),
    ("WebAnimation", "Web animation"),
    ("Webcomic", "Webcomic"),
    ("WebOriginal", "Web original"), # added
    ("Website", "Website"),
    ("WebVideo", "Web video"),
    ("WesternAnimation", "Western animation"),
    ("Wrestling", "Wrestling"), # added
]

# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
class User(AbstractUser):
    pass


class Trope(models.Model):
    urlSafeName = models.TextField(unique=True)
    displayName = models.TextField(unique=True)


class Media(models.Model):
    urlSafeTitle = models.TextField()
    urlMediaType = models.TextField()
    displayTitle = models.TextField(blank=True, null=True, db_index=True)

    tropes = models.ManyToManyField(Trope, related_name="medias")
