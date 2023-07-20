from django.urls import path
from . import views

urlpatterns = [
    path('', views.events_home),
    path('register/<str:event_id>', views.generate_pass)
]
