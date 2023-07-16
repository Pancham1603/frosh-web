from django.shortcuts import render
from .models import UserProfile
def login(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password']
        
        try:
            user_profile = UserProfile.objects.get(registration_id=username)
            stored_password = user_profile.password
            stored_username=user_profile.registration_id

            if (password == stored_password and stored_username==username): 
                print("Login Successful")
            else:
                print("Try Again")
        
        except UserProfile.DoesNotExist:
            print("User not found")
    
    return render(request, 'login.html')
