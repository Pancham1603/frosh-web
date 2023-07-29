from django.urls import path
from .views import VerificationView, EmailActivationLink

urlpatterns = [
    path('activate/', EmailActivationLink.as_view()),
    path('activate/<secure_id_b64>/<token>', VerificationView.as_view(), name='activate'),
]
