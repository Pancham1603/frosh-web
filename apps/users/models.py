from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .manager import UserManager
# import random, string
# import pyqrcode, png, os
# import requests, base64, json
# from decouple import config
from ..hoods.models import Hood

class User(AbstractUser):
    username = None
    image = models.URLField()
    registration_id = models.CharField(unique=True, max_length=20)
    secure_id = models.CharField(unique=True, max_length=8, null=True, blank=True)
    events = ArrayField(base_field=models.CharField(max_length=60), max_length=50, blank=True, default=list)
    qr = models.URLField(blank=True)
    hood = models.ForeignKey(Hood, on_delete=models.DO_NOTHING, blank=True, null=True)

    USERNAME_FIELD = "registration_id"
    REQUIRED_FILEDS = ['image', 'qr']
    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# @receiver(pre_save, sender=User, dispatch_uid="create_new_user")
# def create_user_credentials(sender, instance, **kwargs):
#     if User.objects.filter(registration_id=instance.registration_id).count()==0:
#         secure_id = generate_user_secure_id()
#         instance.secure_id = secure_id
#         instance.qr = upload_to_ibb(generate_qr(
#             json.dumps({
#                 'registration_id':instance.registration_id,
#                 'secure_id':secure_id
#             })
#         , f"{instance.registration_id}_{secure_id}"))