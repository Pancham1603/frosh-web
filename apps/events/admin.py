from django.contrib import admin
from .models import *

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date','time', 'venue', 'max_capacity', 'passes_generated', 'is_booking', 'is_display', 'booking_complete', 'slots_required')
    search_fields = ('name', 'date', 'venue')


class EventPassAdmin(admin.ModelAdmin):
    list_display = ('pass_id', 'user_id', 'event_id', 'slot_id')
    search_fields = ('pass_id', 'user_id__first_name','user_id__registration_id', 'event_id__name', 'event_id__slot_id')

class EventSlotAdmin(admin.ModelAdmin):
    list_display = ('event','date','time', 'venue', 'max_capacity', 'passes_generated')
    search_fields = ('name', 'date', 'venue')


admin.site.register(Event, EventAdmin)
admin.site.register(EventPass, EventPassAdmin)
admin.site.register(EventSlot, EventSlotAdmin)