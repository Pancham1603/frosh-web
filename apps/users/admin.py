from django.contrib import admin
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('registration_id', 'first_name', 'email')
    search_fields = ('registration_id', 'first_name', 'email')

admin.site.register(User, UserAdmin)

admin.site.site_header = "Frosh Admin"
admin.site.site_title = "Frosh Admin"
admin.site.index_title = "Welcome to Frosh Admin"