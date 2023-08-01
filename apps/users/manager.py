from django.contrib.auth.base_user import BaseUserManager
import png, pyqrcode, os
import requests, base64, json
import random, string
from decouple import config

class UserManager(BaseUserManager):
    def create_user(self, registration_id, password=None, **extra_fields):
        counter = 0
        while True:
            try:
                if not registration_id:
                    raise ValueError("Registration ID is required!")
                
                extra_fields['email'] = self.normalize_email(extra_fields['email'])
                extra_fields['secure_id'] = generate_user_secure_id()
                # extra_fields['qr'] = upload_to_ibb(generate_qr(
                #     json.dumps({
                #         'registration_id':registration_id,
                #         'secure_id':extra_fields['secure_id']
                #     })
                # , registration_id))
                user = self.model(registration_id=registration_id, **extra_fields)
                if not extra_fields['is_superuser']:
                    user.set_password(''.join(random.choices(string.ascii_uppercase +
                            string.digits, k=8)))
                else:
                    user.set_password(password)
                user.is_active = True
                user.save(using=self.db)
                return user
            except :
                if counter <3:
                    counter+=1
                    pass 
                else:
                    break

    def create_superuser(self, registration_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(registration_id, password, **extra_fields)

    
def generate_qr(value, registration_id):
    qr = pyqrcode.create(value)
    qr.png(f'{registration_id}.png', scale=6)
    return f'{registration_id}.png'


def upload_to_ibb(file_path):
    with open(file_path, "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": config("IBB_API_KEY"),
            "image": base64.b64encode(file.read()),
        }
        res = requests.post(url, payload)
    os.remove(file_path)
    return res.json()['data']['url']


def generate_user_secure_id():
        return ''.join(random.choices(string.ascii_uppercase +
                            string.digits, k=8))
