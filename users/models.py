from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    bio = models.CharField(max_length=160, blank=True)
    avatar_url = models.URLField(blank=True)

    class Meta:
        indexes = [models.Index(fields=["username"])]
