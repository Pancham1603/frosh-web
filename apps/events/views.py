from django.shortcuts import render, HttpResponse
from .models import Event

# Create your views here.
def events_home(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events':events})

