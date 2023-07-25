from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Event, EventPass
from ..users.models import User
import random
import png
import pyqrcode
import base64
import requests
import string
import os
import json

# Create your views here.
@login_required
def events_home(request):
    events = Event.objects.all()
    user_passes = EventPass.objects.filter(user_id=request.user)
    for Pass in user_passes:
        if Pass.event_id in events:
          events = events.exclude(event_id=Pass.event_id.event_id)


    return render(request, 'events.html', {'events':events, 'user_passes':user_passes})

@csrf_exempt
@login_required
def generate_pass(request, event_id):
    event = Event.objects.get(event_id=event_id)
    user = User.objects.get(registration_id=request.session.get('user'))
    event.refresh_from_db()
    if event.max_capacity > EventPass.objects.filter(event_id=event).count() and EventPass.objects.filter(event_id=event, user_id=user).count()==0:
        while True:
            pass_id = ''.join(random.choices(string.ascii_uppercase +
                                string.digits, k=16))

            if not EventPass.objects.filter(pass_id=pass_id).count():
                break

        generated_pass = EventPass(event_id=event, pass_id=pass_id, user_id=user)
        generated_pass.qr = upload_to_ibb(generate_qr(pass_id))
        generated_pass.save()
        event.passes_generated +=1
        user.events.append(str(event))
        event.save()
        confirmation_email(generated_pass=generated_pass)
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
        return HttpResponse(json.dumps(data))


def generate_qr(value):
    qr = pyqrcode.create(value)
    qr.png(f'{value}.png', scale=8)
    return f'{value}.png'


def upload_to_ibb(file_path):
    with open(file_path, "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": '09dbe019b8cb056535f85d334cbb3aef',
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
    text_content = f'Hi {generated_pass.user_id}, thank you for registering in {generated_pass.event_id}.'
    html_content = f'Hi <b>{generated_pass.user_id}</b>, thank you for registering in <b>{generated_pass.event_id}</b>. <br> Use this code for check-in at the event venue<br><img src="{generated_pass.qr}"><br> Pass ID: {generated_pass.pass_id}<br>Frosh TIET<br>Blazing through infinite realms.'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)

