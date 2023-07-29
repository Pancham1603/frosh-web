from django.shortcuts import render, HttpResponse
from ..events.models import EventPass, Event
from ..users.models import User
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

@csrf_exempt
def fetch_user_data(request):
    if request.method == 'POST':
        pass_id = request.POST.get('pass_id')
        generated_pass = EventPass.objects.get(pass_id=pass_id)
        event = generated_pass.event_id
        user = generated_pass.user_id
        data = {
            'username':f"{user}",
            'registration_id':f"{user.registration_id}",
            'event':f"{event}",
        }
        return HttpResponse(json.dumps(data))

def scanner(request):
    return render(request, 'tempScanner.html')

