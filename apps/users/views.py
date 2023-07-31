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
from .utils import account_activation_token
import random, string
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
                messages.success(request, 'Login Successful')
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
        current_site = get_current_site(request)
        user = User.objects.get(registration_id=request.POST['registration_id'])
        if not user.is_active:
            email_body = {
                'user': user,
                'domain': current_site.domain,
                'secure_id_b64': urlsafe_base64_encode(force_bytes(user.secure_id)),
                'token': account_activation_token.make_token(user),
            }

            link = reverse('activate', kwargs={
                            'secure_id_b64': email_body['secure_id_b64'], 'token': email_body['token']})

            email_subject = 'Activate your account'

            activate_url = 'http://'+current_site.domain+link

            email = EmailMessage(
                email_subject,
                'Hi '+ user.first_name + ', Please click the link below to activate your account \n'+activate_url,
                'noreply@events.froshtiet.com',
                [user.email],
            )
            email.send(fail_silently=False)
            messages.info(request, 'Activation link sent on email!')
            return redirect('/login')
        else:
            messages.info(self.request, 'User already activated')
            return redirect('/login')


class VerificationView(View):
    def get(self, request, secure_id_b64, token):
        try:
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
            user.save()
            email = EmailMultiAlternatives('Your Password for Frosh TIET', 'Hi '+ user.first_name + ', your account has been activated. Use<b> ' + password+' </b>as your password.','pancham1603@gmail.com',
            [user.email],
        )
            email.send(fail_silently=False)
            messages.info(self.request, 'Account activated, password sent on email!')
            return redirect('/logout')

        except Exception as ex:
            pass

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
        print(data)
        User.objects.create_user(registration_id=data[0][-6:],first_name = data[1], last_name = data[3],
         email = data[4], is_staff = False, is_superuser = False, is_active = False, image=data[5])


# create_users_from_xlsx(r'')

        