# Secret_Santa/urls.py (This is the main URL configuration file for your project)

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Santas_Secret.santa.urls')),
]
