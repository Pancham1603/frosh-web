from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _
from ..users.models import User


#### VALIDATORS ####

def event_id_check(value):
    if not value.endswith('@Frosh23'):
        raise ValidationError(
            _("%(value)s is not a valid Frosh event ID. Frosh event IDs end with '@Frosh23'"),
             params={"value":value}
             )

#### MODELS ####

class Event(models.Model):
    event_id = models.CharField(max_length=50, unique=True, validators=[event_id_check], primary_key=True)
    name = models.CharField(max_length=256)
    description = models.TextField()
    venue = models.CharField(max_length=256)
    date = models.DateField()
    time = models.TimeField()
    max_capacity = models.IntegerField()
    passes_generated = models.IntegerField()
    image = models.URLField(default='https://www.freeiconspng.com/thumbs/no-image-icon/no-image-icon-6.png')

    def __str__(self):
        return self.name


class EventPass(models.Model):
    pass_id = models.CharField(max_length=16, unique=True, primary_key=True)
    event_id = models.ForeignKey(Event, on_delete=models.RESTRICT)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    qr = models.URLField(unique=True, validators=[URLValidator])
    entry_status = models.BooleanField(default=False)

    def __str__(self):
        return self.pass_id
