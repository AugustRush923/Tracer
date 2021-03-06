from django.urls import path

from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('send_sms/', send_sms, name='send_sms'),
    path('register/handler/', submit_handler, name='register_handler'),
    path('login/', login, name='login'),
    path('login/sms/', login_sms, name='login_sms'),
    path('login/sms/handler/', login_sms_handler, name='login_sms_handler'),
    path('image_codes/<uuid:image_code_id>/', image_code, name='image_code'),
]
