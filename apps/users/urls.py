from django.urls import path
from .views import VerificationView, EmailActivationLink
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('activate/', csrf_exempt(EmailActivationLink.as_view())),
    path('activate/<secure_id_b64>/<token>', csrf_exempt(VerificationView.as_view()), name='activate'),
]
