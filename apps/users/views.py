from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages


def home(request):
    return render(request, 'index.html')

@csrf_exempt
def login_user(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            registration_id = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=registration_id, password=password)
            if user is not None:
                login(request, user=user)
                request.session['user'] = registration_id
                return redirect('/events')
            else:
                return redirect('/login')
        else:
            return render(request=request, template_name='login.html')
    else:
     return redirect('/events')


def logout_user(request):
    logout(request)
    return redirect('/login')