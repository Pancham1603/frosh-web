from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from .manager import UserManager

class User(AbstractUser):
    username = None
    registration_id = models.CharField(unique=True, max_length=20)
    gender = models.CharField(max_length=1)
    events = ArrayField(base_field=models.CharField(max_length=60), max_length=50, blank=True, default=list)

    USERNAME_FIELD = "registration_id"
    REQUIRED_FILEDS = ['gender']
    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

