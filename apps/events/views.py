from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from .models import Event, EventPass
from ..users.models import User
import random
import png
import pyqrcode
import base64
import requests
import string
import os

# Create your views here.
def events_home(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events':events})

#- /events/register/<event id>
#- event ID from 'django dynamic URL patterns'
#- user ID from request.session.get("user")
#- passId will be random alphanimeric, generated using Random module
#- QR code will be made from Pass ID using pyzbar and pypng

def generate_pass(request, event_id):
    event = Event.objects.get(event_id=event_id)
    user = User.objects.get(registration_id=request.session.get('user'))
    
    if event.max_capacity != event.passes_generated and EventPass.objects.filter(event_id=event, user_id=user).count()==0:
        while True:
            pass_id = ''.join(random.choices(string.ascii_uppercase +
                                string.digits, k=16))

            if not EventPass.objects.filter(pass_id=pass_id).count():
                break

        generated_pass = EventPass(event_id=event, pass_id=pass_id, user_id=user)
        generated_pass.qr = upload_to_ibb(generate_qr(pass_id))
        generated_pass.save()
        event.passes_generated +=1
        event.save()
        confirmation_email(generated_pass=generated_pass)
        return redirect('/events')
    else:
        return redirect('/events')


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
    msg.send(fail_silently=True)
