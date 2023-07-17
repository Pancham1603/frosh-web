from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

class User(AbstractUser):
    username = None
    registration_id = models.CharField(unique=True, max_length=20)
    gender = models.CharField(max_length=1)

    USERNAME_FIELD = "registration_id"
    REQUIRED_FILEDS = ['gender']
    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

