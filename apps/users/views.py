from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.views import View
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from django.template import Context
from .utils import account_activation_token
import random, string
import openpyxl
from .models import User
from .manager import generate_qr, generate_user_secure_id, upload_to_ibb
from datetime import datetime
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import json

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
                # messages.success(request, 'Login Successful')
                return redirect('/events')
            else:
                messages.error(request, 'Invalid password or account not activated')
                return redirect('/login')
        else:
            return render(request=request, template_name='login.html')
    else:
     return redirect('/events')


def logout_user(request):
    logout(request)
    return redirect('/login')


class EmailActivationLink(View):
    def get(self, request):
            return render(request, 'activate.html')


    def post(self, request):
        # current_site = get_current_site(request)
        user = User.objects.get(registration_id=request.POST['registration_id'])
        # if not user.is_active:
        #     email_body = {
        #         'user': user,
        #         'domain': current_site.domain,
        #         'secure_id_b64': urlsafe_base64_encode(force_bytes(user.secure_id)),
        #         'token': account_activation_token.make_token(user),
        #     }

        #     link = reverse('activate', kwargs={
        #                     'secure_id_b64': email_body['secure_id_b64'], 'token': email_body['token']})
        user.is_active = True
        password = ''.join(random.choices(string.ascii_uppercase +
                        string.digits, k=8))
        user.set_password(password)
        user.secure_id = generate_user_secure_id()
        user.qr = upload_to_ibb(generate_qr(
            json.dumps({
                'registration_id':user.registration_id,
                'secure_id':user.secure_id
            })
        , user.registration_id))
        user.save()
        text_content =  'Hi '+ user.first_name + ', your account has been activated. Use ' + password+' as your password.'
        email = EmailMultiAlternatives('Your Password for Frosh 23', text_content,'frosh+noreply@thapar.edu',
        [user.email],
    )
        email.attach_alternative(render_to_string('email_password.html', {'user':user.first_name, 'password':password}), 'text/html')
        email.send(fail_silently=True)
        messages.info(self.request, 'Account activated, password sent on email!')
        return redirect('/logout')


class VerificationView(View):
    def get(self, request, secure_id_b64, token):
        # try:
        secure_id = force_str(urlsafe_base64_decode(secure_id_b64))
        user = User.objects.get(secure_id=secure_id)

        if not account_activation_token.check_token(user, token):
            messages.info(self.request, 'User already activated')
            return redirect('/login')

        if user.is_active:
            return redirect('/login')
        user.is_active = True
        password = ''.join(random.choices(string.ascii_uppercase +
                        string.digits, k=8))
        user.set_password(password)
        user.secure_id = generate_user_secure_id()
        user.qr = upload_to_ibb(generate_qr(
            json.dumps({
                'registration_id':user.registration_id,
                'secure_id':user.secure_id
            })
        , user.registration_id))
        user.save()
        text_content =  'Hi '+ user.first_name + ', your account has been activated. Use ' + password+' as your password.'
        email = EmailMultiAlternatives('Your Password for Frosh 23', text_content,'frosh+noreply@thapar.edu',
        [user.email],
    )
        email.attach_alternative(render_to_string('email_password.html', {'user':user.first_name, 'password':password}), 'text/html')
        email.send(fail_silently=True)
        messages.info(self.request, 'Account activated, password sent on email!')
        return redirect('/logout')

        # except Exception as ex:
        #     pass

        return redirect('/login')


def create_users_from_xlsx(file_path):
    count = 0
    wb_obj = openpyxl.load_workbook(file_path)
    sheet = wb_obj.active
    users = User.objects.all()
    start = int(input("Start: "))
    end = int(input('End: '))
    for row in range(start, end+1):
        data = []
        user = User()
        for column in range(1,7):
            cell = sheet.cell(row=row, column=column)
            data.append(cell.value)
        # print
        # if not data[5]:
        #     try: 
        #         URLValidator(data[5])
        #         if users.filter(email=data[4]).count() == 0:
        #             user = User.objects.create_user(registration_id=data[0][-6:],first_name = data[1], last_name = data[3],
        #             email = data[4], is_staff = False, is_superuser = False, is_active = False, image=data[5])
        #             count+=1
        #             print(f"[{count}] ",f"[ADDED TO DATABASE] {user.first_name}")
        #         else:
        #             count+=1
        #             print(f"[{count}] ",f"[FAILURE] {user.first_name}")
        #     except ValidationError:
                # if users.filter(email=data[4]).count() == 0:
        user = User.objects.create_user(registration_id=data[0][-6:],first_name = data[1], last_name = data[3],
        email = data[4], is_staff = False, is_superuser = False, is_active = False, image='https://img.freepik.com/premium-vector/man-avatar-profile-picture-vector-illustration_268834-538.jpg')
        count+=1
        print(f"[{count}] ",f"[ADDED TO DATABASE] {user.first_name}")
        #         else:
        #             count+=1
        #             print(f"[{count}] ",f"[FAILURE] {user.first_name}")
        # else:
        #     count+=1
        #     print(f"[{count}] ",f"[FAILURE] {user.first_name}")

# create_users_from_xlsx(r'C:\Users\ajay\Desktop\projects\frosh-web\Untitled spreadsheet (1).xlsx')

def add_secret_key_for_all():
    users = User.objects.all()
    count = 0
    for user in users:
        if not user.secure_id:
            user.secure_id = generate_user_secure_id()
            user.save()
            count+=1
            print(count, user.first_name)

# add_secret_key_for_all()