from django.urls import path

from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('register/send_sms/', send_sms, name='send_sms'),
]
