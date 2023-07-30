from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', scanner),
    path('userdata', fetch_user_data),
    path('userdata/validate', invalidate_pass)
]
