import re
import random
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django_redis import get_redis_connection
from django.conf import settings
# Create your views here.
from users.forms import RegisterForm, LoginSmsForm
from utils import tencent, encrypt
from .models import Register


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})


def send_sms(request):
    if request.method == 'POST':
        tpl = request.POST.get('tpl')
        phone_number = request.POST.get('phone_number')

        if not all([tpl, phone_number]):
            return JsonResponse({'status': 500202, 'errmsg': '参数不全'})
        if not tpl:
            return JsonResponse({'status': 216601, 'errmsg': '没有对应模板'})
        template_id = settings.SMS_TEMPLATE_ID.get(tpl)

        if not phone_number:
            return JsonResponse({'status': 217601, 'errmsg': '手机号不能为空', 'key': 'phone_number'})
        if not re.match(r'^1(3\d|4[5-8]|5[0-35-9]|6[567]|7[01345-8]|8\d|9[025-9])\d{8}$', phone_number):
            # 手机不合法
            return JsonResponse({'status': 217601, 'errmsg': '手机号格式不正确', 'key': 'phone_number'})

        exists = Register.objects.filter(phone_number=phone_number).exists()
        if exists:
            return JsonResponse({'status': 221111, 'errmsg': '手机号已注册', 'key': 'phone_number'})

        sms_code = random.randrange(10000, 99999)
        conn = get_redis_connection()
        conn.setex(phone_number, 90, sms_code)
        response = tencent.sms.send_sms_single(phone_number, template_id, [sms_code, 3])
        if response['result'] != 0:
            return JsonResponse({'status': 216601, 'errmsg': response['errmsg'], 'key': 'code'})
        return JsonResponse({'status': 200000, 'errmsg': '发送成功'})


def submit_handler(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        username_exist = Register.objects.filter(username=username).exists()
        if username_exist:
            return JsonResponse({'status': 221111, 'errmsg': '用户名不能重复', 'key': 'username'})

        email = request.POST.get('email')
        if not re.match(r'^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$', email):
            return JsonResponse({'status': 217601, 'errmsg': '邮箱合适不正确', 'key': 'email'})

        email_exist = Register.objects.filter(email=email).exists()
        if email_exist:
            return JsonResponse({'status': 221111, 'errmsg': '邮箱不能重复', 'key': 'username'})

        password = request.POST.get('password')
        if len(password) < 8:
            return JsonResponse({'status': 500203, 'errmsg': '密码长度不能小于8位', 'key': 'password'})
        if len(password) > 16:
            return JsonResponse({'status': 500203, 'errmsg': '密码长度不能长与16位', 'key': 'password'})

        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            return JsonResponse({'status': 304404, 'errmsg': '两次输入的密码不一致', 'key': 'confirm_password'})
        encrypt_password = encrypt.md5_encrypt(password)

        phone_number = request.POST.get('phone_number')
        if not re.match(r'^1(3\d|4[5-8]|5[0-35-9]|6[567]|7[01345-8]|8\d|9[025-9])\d{8}$', phone_number):
            # 手机不合法
            return JsonResponse({'status': 217601, 'errmsg': '手机号格式不正确', 'key': 'phone_number'})
        exists = Register.objects.filter(phone_number=phone_number).exists()
        if exists:
            return JsonResponse({'status': 221111, 'errmsg': '手机号已注册', 'key': 'phone_number'})

        code = request.POST.get('code')
        # 验证验证码
        conn = get_redis_connection()
        real_code = conn.get(phone_number).decode('utf-8')
        if not real_code:
            return JsonResponse({'status': 2116601, 'errmsg': '验证码失效或未发送，请重新发送', 'key': 'code'})

        print(code, real_code)
        if code != real_code:
            return JsonResponse({'status': 10001, 'errmsg': '验证码不匹配', 'key': 'code'})

        # 存入数据库
        print(username, email, password, confirm_password, phone_number, code)
        Register.objects.create(username=username, email=email, password=encrypt_password, phone_number=phone_number)
        return JsonResponse({'status': 200000, 'errmsg': '发送成功'})


def login_sms(request):
    if request.method == 'GET':
        form = LoginSmsForm()
        return render(request, 'users/login_sms.html', {'form': form})
