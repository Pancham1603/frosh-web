from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ..users.models import User
from .models import Hood
import random
import string
import json
from datetime import datetime


# @login_required
# def allotment_form(request):
#     if request.method == 'POST':
#         if HoodPreference.objects.filter(user=request.user).exists():
#             messages.error(request, 'You have already submitted your preferences!')
#             return redirect('/hoods/initiation')
#         preferences = request.POST.get('preferences').split(',')	
#         hood_preference = HoodPreference()
#         hood_preference.user = request.user
#         hood_preference.hood_1 = Hood.objects.get(id=preferences[0])
#         hood_preference.hood_2 = Hood.objects.get(id=preferences[1])
#         hood_preference.hood_3 = Hood.objects.get(id=preferences[2])
#         hood_preference.hood_4 = Hood.objects.get(id=preferences[3])
#         return HttpResponse({
#             'message':'Preferences saved successfully!',
#             'status':200	
#         })
#     return render(request, 'clans.html')


def random_allotments():
    active_users = User.objects.filter(is_active=True)
    hoods = [hood for hood in Hood.objects.all()]
    counters = {
        hoods[0]:0,
        hoods[1]:0,
        hoods[2]:0,
        hoods[3]:0
    }
    count = 0
    print(active_users.count())
    max_members = int(active_users.count()/4)
    for user in active_users:
        while True:
            user_hood = random.choice(hoods)
            if counters[user_hood] < max_members:
                counters[user_hood] += 1
                count +=1 
                user.hood = user_hood
                user.save()
                print(f"[{count}] [{user_hood.name}] {user}")
                break
    for hood in hoods:
        hood.member_count = counters[hood]
        hood.save()
    print(active_users.count())
        

# random_allotments()
