from django.shortcuts import render, HttpResponse
from .models import Event, EventPass

# Create your views here.
def events_home(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events':events})


#- /events/register/<event id>
#- event ID from 'django dynamic URL patterns'
#- user ID from request.session.get("user")
#- passId will be random alphanimeric, generated using Random module
#- QR code will be made from Pass ID using pyzbar and pypng
