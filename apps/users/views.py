from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def home(request):
    return render(request, 'index.html')


def login_user(request):
    if request.method == 'POST':
        registration_id = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=registration_id, password=password)
        if user is not None:
            login(request, user=user)
            request.session['user'] = registration_id
            return redirect('/')
        else:
            return redirect('/login')
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/')