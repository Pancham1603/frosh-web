from django.shortcuts import render, HttpResponse
from ..events.models import EventPass, Event
from ..users.models import User
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

@csrf_exempt
def fetch_user_data(request):
    if request.method == 'POST':
        qr_data = request.POST.get('pass_id')
        if 'pass_id' in qr_data:
            generated_pass = EventPass.objects.get(pass_id=pass_id)
            event= generated_pass.event_id
            user = generated_pass.user_id
            data = {
                'user':f"{user}",
                'registration_id':f"{user.registration_id}",
                'event':f"{event}",
                'image':user.image,
                'valid':True if not generated_pass.entry_status else False
            }
            return HttpResponse(json.dumps(data))

        elif 'registration_id' in qr_data and 'secure_id' in qr_data:
            user = User.objects.filter(registration_id=qr_data['registration_id'], secure_id=qr_data['secure_id'])
            event = Event.objects.get(event_id=qr_data['event_id'])
            generated_pass = EventPass.objects.filter(user_id=user, event_id=event)
            if generated_pass:
                data = {
                'user':f"{user}",
                'registration_id':f"{user.registration_id}",
                'event':f"{event}",
                'image':user.image,
                'valid':True if not generated_pass.entry_status else False
                }
                HttpResponse(json.dumps(data))
            else: 
                HttpResponse("User pass for this event doesn't exist")


@csrf_exempt
def invalidate_pass(request):
    if request.method == 'POST':
        pass_id = request.POST.get('pass_id')
        generated_pass = EventPass.objects.filter(pass_id=pass_id).update(entry_status=True)
        return HttpResponse("Pass verified!")


def scanner(request):
    events = Event.objects.filter(booking_required=True).values('event_id', 'name')
    return render(request, 'scanner.html', {'events':events})

