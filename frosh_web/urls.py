"""
URL configuration for frosh_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.users import views as user_views
from apps.events import views as event_views

urlpatterns = [
   path('', user_views.login_user),
   path('bablucopter/', admin.site.urls),
   path('bablucopter/login', user_views.login_user),
   path('login/', user_views.login_user),
   path('logout/', user_views.logout_user),
   path('', include("apps.users.urls")),
   path('users/', include("django.contrib.auth.urls")),
   path('events/', include("apps.events.urls")),
   path('scanner/', include("apps.validation.urls"))
]
