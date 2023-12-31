from django.shortcuts import render, HttpResponse
from ..events.models import EventPass, Event
from ..users.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

# Create your views here.

@csrf_exempt
def fetch_user_data(request):
    if request.method == 'POST':
        qr_data = request.POST.get('pass_id')
        if len(qr_data) == 16:
            generated_pass = EventPass.objects.get(pass_id=qr_data)
            event= generated_pass.event_id
            if event.event_id == request.POST.get('event_id'):
                user = generated_pass.user_id
                data = {
                    'user':f"{user}",
                    'registration_id':f"{user.registration_id}",
                    'event':f"{event}",
                    'image':user.image,
                    'valid':True if not generated_pass.entry_status else False,
                    'message':'Pass verified' if not generated_pass.entry_status else 'Pass has already been used'
                }
                return HttpResponse(json.dumps(data))
            else:
                return HttpResponse(json.dumps({
                'valid':False,
                'message': 'Invalid Pass'
            }))
        elif 'registration_id' in qr_data and 'secure_id' in qr_data:
            qr_data = json.loads(qr_data) 
            user = User.objects.get(registration_id=qr_data['registration_id'], secure_id=qr_data['secure_id'])
            event = Event.objects.get(event_id=request.POST.get('event_id'))
            generated_pass = EventPass.objects.filter(user_id=user, event_id=event).first()
            if generated_pass:
                data = {
                'user':f"{user}",
                'registration_id':f"{user.registration_id}",
                'event':f"{event}",
                'image':user.image,
                'time':generated_pass.time,
                'valid':True if not generated_pass.entry_status else False,
                'message': 'Pass verified' if not generated_pass.entry_status else 'Pass has already been used'
                }
                return HttpResponse(json.dumps(data))
            else: 
                return HttpResponse(json.dumps({
                'valid':False,
                'message': "Pass for this event doesn't exists"
            }))
        else:
            return HttpResponse(json.dumps({
                'valid':False,
                'message': 'Invalid Pass'
            }))
    else:
        return HttpResponse(json.dumps({
                'valid':False,
                'message': 'Method not allowed'
            }))


@csrf_exempt
def invalidate_pass(request):
    if request.method == 'POST':
        qr_data = request.POST.get('pass_id')
        if len(qr_data) == 16:
            pass_id = request.POST.get('pass_id')
            generated_pass = EventPass.objects.filter(pass_id=pass_id).update(entry_status=True)
            return HttpResponse('Pass Verified!')
        elif 'registration_id' in qr_data and 'secure_id' in qr_data:
            qr_data = json.loads(qr_data)
            user = User.objects.get(registration_id=qr_data['registration_id'], secure_id=qr_data['secure_id'])
            event = Event.objects.get(event_id=request.POST.get('event_id'))
            generated_pass = EventPass.objects.filter(user_id=user, event_id=event).update(entry_status=True)
            count = EventPass.objects.filter(event_id=event, entry_status=True).count()
            return HttpResponse(f"Pass verified! Live Count: {count}")


@login_required
def scanner(request):
    if request.user.is_staff:
        events = Event.objects.filter(booking_required=True).values('event_id', 'name')
        if request.iOS:
            return render(request, 'iphone.html', {'events':events})
        else:
            return render(request, 'scanner.html', {'events':events})
    else:
        return HttpResponse('Invalid Operation')
    


