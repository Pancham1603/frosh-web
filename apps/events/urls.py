from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.events_home),
    path('register/<str:event_id>', views.generate_pass),
    path('register/<str:event_id>/<str:slot_id>', views.generate_pass)
]
