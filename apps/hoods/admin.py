from django.contrib import admin
from .models import Hood

# Register your models here.

class HoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'member_count')
    search_fields = ('name', 'description')

admin.site.register(Hood, HoodAdmin)
