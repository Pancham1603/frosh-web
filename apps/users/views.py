from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import openpyxl
from .models import User
from datetime import datetime

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


def create_users_from_xlsx(file_path):
    wb_obj = openpyxl.load_workbook(file_path)
    sheet = wb_obj.active

    for row in range(2, sheet.max_row+1):
        data = []
        user = User()
        for column in range(1,7):
            cell = sheet.cell(row=row, column=column)
            data.append(cell.value)
        user.registration_id = f"{data[1].strftime('%d%m%y')}"
        user.first_name = data[2]
        user.last_name = data[3]
        user.email = data[4]
        user.gender = data[5]
        user.set_password('12345678')
        user.is_staff = False
        user.is_superuser = False
        user.is_active = True
        user.save()
        print(user)
        
       
        # if not user.registration_id in User.objects.filter(registration_id=user.registration_id):
            
       
        


# create_users_from_xlsx(r'E:\frosh-web\apps\users\testing_phase_1.xlsx')

        