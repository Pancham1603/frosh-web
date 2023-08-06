from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from ..users.models import User
import random
import string


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
    time = models.CharField(max_length=256)
    max_capacity = models.IntegerField()
    passes_generated = models.IntegerField()
    image = models.URLField(default='https://www.freeiconspng.com/thumbs/no-image-icon/no-image-icon-6.png')
    calendar_url = models.URLField(default='#')
    booking_required = models.BooleanField(default=True)
    is_booking = models.BooleanField(default=False)
    is_display = models.BooleanField(default=False)
    slots_required = models.BooleanField(default=False)
    slot_id = models.CharField(max_length=16, default='lmao')

    def __str__(self):
        return self.name


class EventSlot(models.Model):
    slot_id = models.CharField(primary_key=True, unique=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    time = models.CharField(max_length=256)
    calendar_url = models.URLField(default='#')
    passes_generated = models.IntegerField()
    venue = models.CharField(max_length=256)
    date = models.DateField()
    max_capacity = models.IntegerField()


@receiver(post_save, sender=Event, dispatch_uid="create_new_event_and_slot")
def create_event_slot(sender, instance, **kwargs):
    if instance.slots_required and EventSlot.objects.filter(event=Event.objects.get(event_id=instance.event_id)).count()==0:
        while True:
            slot_id = ''.join(random.choices(string.ascii_uppercase +
                                string.digits, k=16))
            if not EventSlot.objects.filter(slot_id=slot_id).count():
                break
        slot = EventSlot(slot_id=slot_id,venue=instance.venue,date= instance.date, time=instance.time,max_capacity= instance.max_capacity,passes_generated= 0,calendar_url= instance.calendar_url)
        slot.event = instance
        slot.save()
        event = Event.objects.filter(event_id=instance.event_id).update(slot_id=slot_id)
        


class EventPass(models.Model):
    pass_id = models.CharField(max_length=16, unique=True, primary_key=True)
    event_id = models.ForeignKey(Event, on_delete=models.RESTRICT)
    slot_id = models.ForeignKey(EventSlot, on_delete=models.RESTRICT, default=None, null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    qr = models.URLField(validators=[URLValidator])
    entry_status = models.BooleanField(default=False)
    time = models.CharField(max_length=256)

    def __str__(self):
        return self.pass_id