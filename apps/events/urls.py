from django.urls import path
from . import views
from ..users import views as user_views

urlpatterns = [
    path('', user_views.login_user),
    path('register/<str:event_id>', views.generate_pass),
    path('register/<str:event_id>/<str:slot_id>', views.generate_pass)
]
