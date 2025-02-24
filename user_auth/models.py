from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=255)
    # profile_picture = models.ImageField(upload_to='static/img/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    USERNAME_FIELD = "email"  # Login with email instead of username
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.name
