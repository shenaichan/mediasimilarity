from django.contrib.auth.models import AbstractUser
from django.db import models


# https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
class User(AbstractUser):
    pass


class Trope(models.Model):
    urlSafeName = models.TextField(unique=True)
    displayName = models.TextField(blank=True, null=True)


class Media(models.Model):
    urlSafeTitle = models.TextField(unique=True)
    urlMediaType = models.TextField()
    displayTitle = models.TextField(blank=True, null=True, db_index=True)

    tropes = models.ManyToManyField(Trope, related_name="medias")
