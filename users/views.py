import re
import uuid
import random
import datetime
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, reverse
from django_redis import get_redis_connection
from django.conf import settings
from django.db.models import Q

# Create your views here.
from users.forms import RegisterForm, LoginSmsForm, LoginForm
from utils import tencent, encrypt
from utils.captcha.captcha import captcha
from .models import Register, Transaction, PriceStrategy


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})


def send_sms(request):
    if request.method == 'POST':
        tpl = request.POST.get('tpl')
        phone_number = request.POST.get('phone_number')

        if not all([tpl, phone_number]):
            return JsonResponse({'status': 500202, 'errmsg': '手机号不能为空', 'key': 'phone_number'})
        if not tpl:
            return JsonResponse({'status': 216601, 'errmsg': '没有对应模板'})
        template_id = settings.SMS_TEMPLATE_ID.get(tpl)

        if not re.match(r'^1(3\d|4[5-8]|5[0-35-9]|6[567]|7[01345-8]|8\d|9[025-9])\d{8}$', phone_number):
            # 手机不合法
            return JsonResponse({'status': 217601, 'errmsg': '手机号格式不正确', 'key': 'phone_number'})

        exists = Register.objects.filter(phone_number=phone_number).exists()
        if tpl == 'register':
            if exists:
                return JsonResponse({'status': 221111, 'errmsg': '手机号已注册', 'key': 'phone_number'})
        else:
            if not exists:
                return JsonResponse({'status': 221111, 'errmsg': '手机号未注册', 'key': 'phone_number'})

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
        try:
            real_code = conn.get(phone_number).decode('utf-8')
        except AttributeError:
            return JsonResponse({'status': 2116601, 'errmsg': '验证码失效或未发送，请重新发送', 'key': 'code'})
        if not real_code:
            return JsonResponse({'status': 2116601, 'errmsg': '验证码失效或未发送，请重新发送', 'key': 'code'})

        print(code, real_code)
        if code != real_code:
            return JsonResponse({'status': 10001, 'errmsg': '验证码不匹配', 'key': 'code'})

        # 存入数据库
        print(username, email, password, confirm_password, phone_number, code)
        user = Register.objects.create(username=username, email=email, password=encrypt_password,
                                       phone_number=phone_number)
        # 创建交易记录
        price_strategy = PriceStrategy.objects.filter(category=0).first()
        Transaction.objects.create(
            status=1,
            order=str(uuid.uuid4()),
            user=user,
            price_strategy=price_strategy,
            count=0,
            price=0,
            start_time=datetime.datetime.now(),
        )
        return redirect('/index/')


def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'users/login.html', {'form': form})
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        code = request.POST.get('code')
        if not all([username, password, code]):
            return JsonResponse({'status': 500202, 'errmsg': '数据不全'})
        conn = get_redis_connection(alias='verify_codes')
        real_code = conn.get('img').decode('utf-8')
        if code.upper != real_code:
            return JsonResponse({'status': 10001, 'errmsg': '验证码不匹配', 'key': 'code'})
        password = encrypt.md5_encrypt(password)
        if re.match(r'^1(3\d|4[5-8]|5[0-35-9]|6[567]|7[01345-8]|8\d|9[025-9])\d{8}$', username):
            # 手机号登录
            user = Register.objects.filter(Q(email=username) | Q(password=password)).first()
        elif re.match(r'^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$', username):
            # 邮箱登录
            user = Register.objects.filter(Q(phone_number=username) | Q(password=password)).first()
        # 账户登录
        else:
            user = Register.objects.filter(Q(username=username) | Q(password=password)).first()
        if not user:
            return JsonResponse({'status': 10002, 'errmsg': '当前账户不存在', 'key': 'phone_number'})
        print("登录成功！")
        request.session['user_id'] = user.id
        # return JsonResponse({'status': 200000, 'errmsg': '登录成功'})
        return redirect(reverse('home:index'))


def login_sms(request):
    if request.method == 'GET':
        form = LoginSmsForm()
        return render(request, 'users/login_sms.html', {'form': form})


def login_sms_handler(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        if not re.match(r'^1(3\d|4[5-8]|5[0-35-9]|6[567]|7[01345-8]|8\d|9[025-9])\d{8}$', phone_number):
            # 手机不合法
            return JsonResponse({'status': 217601, 'errmsg': '手机号格式不正确', 'key': 'phone_number'})
        code = request.POST.get('code')
        conn = get_redis_connection()
        try:
            real_code = conn.get(phone_number).decode('utf-8')
        except AttributeError:
            return JsonResponse({'status': 2116601, 'errmsg': '验证码失效或未发送，请重新发送', 'key': 'code'})
        if not real_code:
            return JsonResponse({'status': 2116601, 'errmsg': '验证码失效或未发送，请重新发送', 'key': 'code'})
        if code != real_code:
            return JsonResponse({'status': 10001, 'errmsg': '验证码不匹配', 'key': 'code'})
        user = Register.objects.filter(phone_number=phone_number).first()
        if not user:
            return JsonResponse({'status': 10002, 'errmsg': '当前账户不存在', 'key': 'phone_number'})
        print('登录成功')
        request.session['user.id'] = user.id
        return JsonResponse({'status': 200000, 'errmsg': '登录成功'})
        # return redirect(reverse('home:index'))


def image_code(request, image_code_id):
    if request.method == 'GET':
        text, image = captcha.generate_captcha()
        print(text)
        redis_conn = get_redis_connection('verify_codes')
        # redis_conn.setex("img_%s" % image_code_id, 180, text)
        redis_conn.setex("img", 180, text)
        return HttpResponse(image, content_type="images/jpg")
