from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from ..users.models import User
import random
import string
import json
from datetime import datetime


@login_required
def allotment_form(request):
    if request.method == 'POST':
        preferences = request.POST.get('preferences').split(',')	
        print(preferences)	
        return HttpResponse('success')
    return render(request, 'clans.html')

