from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Event, EventPass, EventSlot
from ..users.models import User
import random
import png
import pyqrcode
import base64
import requests
import string
import os
import json
from datetime import date, time, datetime
from decouple import config

global counters
counters = {} 
for event in Event.objects.all():
    counters[event.name]=event.passes_generated
for slot in EventSlot.objects.all():
    counters[slot.slot_id] = slot.passes_generated

# Create your views here.
@login_required
def events_home(request):
    events = Event.objects.all()
    events_sorted = sorted(events, key=lambda x: [x.date, convert_time_to_start_time(x.time)])
    user_passes = EventPass.objects.filter(user_id=request.user)
    live_event = events_sorted[0]
    try:
        live_event_pass = user_passes.filter(event_id=live_event, user_id=request.user)[0]
    except:
        live_event_pass = None
    scheduled_events = events.exclude(event_id=live_event.event_id)
    for Pass in user_passes:
        if Pass.event_id in events:
          scheduled_events = scheduled_events.exclude(event_id=Pass.event_id.event_id)
    event_slots = EventSlot.objects.all()
    user_passes_all = user_passes
    user_passes = user_passes.exclude(event_id=live_event.event_id)
    scheduled_events = sorted(scheduled_events, key=lambda x: [x.date, convert_time_to_start_time(x.time)])
    return render(request, 'events.html', {'live_event':live_event,'live_event_pass':live_event_pass, 'scheduled_events':scheduled_events ,'user_passes':user_passes, 'event_slots':event_slots, 'user_passes_all':user_passes_all})


@csrf_exempt
@login_required
def generate_pass(request, event_id, slot_id=None):
    user = User.objects.get(registration_id=request.user.registration_id)
    event = Event.objects.get(event_id=event_id)
    if not event.is_booking and not event.booking_required:
        data = {
                'status':False,
                'message':'Booking is not available for this event'
                }
        return HttpResponse(json.dumps(data))
    if not EventPass.objects.filter(user_id=user, event_id=event).count():
        if slot_id and event.slot_id==slot_id:
            event_slot = EventSlot.objects.get(slot_id=slot_id)
            counters[slot_id] += 1
            event_slot.refresh_from_db()
            if counters[slot_id]<=event_slot.max_capacity:
                while True:
                    pass_id = ''.join(random.choices(string.ascii_uppercase +
                                        string.digits, k=16))

                    if not EventPass.objects.filter(pass_id=pass_id).count():
                        break
                generated_pass = EventPass(event_id=event_slot.event,slot_id=event_slot ,pass_id=pass_id, user_id=user)
                generated_pass.qr = upload_to_ibb(generate_qr(pass_id))
                generated_pass.time = event_slot.time
                generated_pass.save()
                confirmation_email(generated_pass=generated_pass)

                event_slot.passes_generated = counters[slot_id]
                user.events.append(str(event))
                user.save()
                event_slot.save()
                data = {
                'pass_qr':generated_pass.qr,
                'status':True
                }
                return HttpResponse(json.dumps(data))
            else:
                data={
                    'status':False,
                    'message':"There was an error!"
                }
                counters[slot_id]-=1
                return HttpResponse(json.dumps(data))
        elif slot_id and event.slot_id!=slot_id:
            data={
                    'status':False,
                    'message':"There was an error!"
                }
            return HttpResponse(json.dumps(data))
        else:
            counters[event.name]+=1
            event.refresh_from_db()
            if counters[event.name]<=event.max_capacity:
                while True:
                    pass_id = ''.join(random.choices(string.ascii_uppercase +
                                        string.digits, k=16))

                    if not EventPass.objects.filter(pass_id=pass_id).count():
                        break

                generated_pass = EventPass(event_id=event, pass_id=pass_id, user_id=user)
                generated_pass.qr = upload_to_ibb(generate_qr(pass_id))
                generated_pass.time = event.time
                generated_pass.save()
                
                confirmation_email(generated_pass=generated_pass)
                event.passes_generated = counters[event.name]
                user.events.append(str(event))
                user.save()
                event.save()
                data = {
                    'pass_qr':generated_pass.qr,
                    'status':True
                }
                return HttpResponse(json.dumps(data))
            else:
                data={
                    'status':False,
                    'message':"There was an error!"
                }
                counters[event.name]-=1
                return HttpResponse(json.dumps(data))
    else:
        data={
                    'status':False,
                    'message':"You have already booked a pass for this event!"
                }
        return HttpResponse(json.dumps(data))

def generate_qr(value):
    qr = pyqrcode.create(value)
    qr.png(f'{value}.png', scale=8)
    return f'{value}.png'


def upload_to_ibb(file_path):
    with open(file_path, "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": config("IBB_API_KEY"),
            "image": base64.b64encode(file.read()),
        }
        res = requests.post(url, payload)
        print(res.json()['data']['url'])
    os.remove(file_path)
    return res.json()['data']['url']


def confirmation_email(generated_pass:EventPass):
    subject= subject = f'Registration successful for {generated_pass.event_id}'
    from_email = settings.EMAIL_HOST_USER
    to = generated_pass.user_id.email
    if generated_pass.slot_id:
        text_content = f'Hi {generated_pass.user_id}, thank you for registering in {generated_pass.event_id}. Your slot is {generated_pass.slot_id.time}'
        html_content = f'Hi <b>{generated_pass.user_id}</b>, thank you for registering in <b>{generated_pass.event_id}</b>. Your slot is {generated_pass.slot_id.time}  <br> Use this code for check-in at the event venue<br><img src="{generated_pass.qr}"><br> Pass ID: {generated_pass.pass_id}<br>Frosh TIET<br>Blazing through infinite realms.'
    else: 
        text_content = f'Hi {generated_pass.user_id}, thank you for registering in {generated_pass.event_id}.'
        html_content = f'Hi <b>{generated_pass.user_id}</b>, thank you for registering in <b>{generated_pass.event_id}</b>. <br> Use this code for check-in at the event venue<br><img src="{generated_pass.qr}"><br> Pass ID: {generated_pass.pass_id}<br>Frosh TIET<br>Blazing through infinite realms.'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)


def convert_time_to_start_time(time_string):
    split = time_string.split('-')
    start_time = datetime.strptime(split[0].strip(), "%H:%M:%S")
    # start_date = datetime.strptime(date, )
    # datetime.combine(start_date, start_time)
    end_time =  datetime.strptime(''.join(char for char in split[1] if char!=' '), "%H:%M:%S") 
    return start_time