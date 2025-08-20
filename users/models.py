# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)             # unique email
    bio = models.CharField(max_length=160, blank=True)
    avatar_url = models.URLField(blank=True)           

    class Meta:
        indexes = [models.Index(fields=["username"]), models.Index(fields=["email"])]
