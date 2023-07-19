from django.contrib import admin
from .models import Event, EventPass

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'venue', 'max_capacity', 'passes_generated')
    search_fields = ('name', 'date', 'venue')


class EventPassAdmin(admin.ModelAdmin):
    list_display = ('pass_id', 'user_id', 'event_id')
    search_fields = ('pass_id', 'user_id', 'event_id')


admin.site.register(Event, EventAdmin)
admin.site.register(EventPass, EventPassAdmin)