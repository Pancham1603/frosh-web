from django.db import models

class UserProfile(models.Model):
    registration_id = models.CharField(max_length=256)
    password = models.CharField(max_length=16)
    email = models.EmailField()

