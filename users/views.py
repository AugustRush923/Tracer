import re
import random
from django.http import JsonResponse
from django.shortcuts import render
from django_redis import get_redis_connection
from django.conf import settings
# Create your views here.
from users.forms import RegisterForm
from utils.tencent import sms
from .models import Register


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})


def send_sms(request):
    if request.method == 'POST':
        tpl = request.POST.get('tpl')
        phone_number = request.POST.get('phone_number')
        if not tpl:
            return JsonResponse({'status': 216601, 'errmsg': '没有对应模板'})
        template_id = settings.SMS_TEMPLATE_ID.get(tpl)
        if not phone_number:
            return JsonResponse({'status': 217601, 'errmsg': '手机号不能为空', 'key': 'phone_number'})
        if not re.match(r'^1(3\d|4[5-8]|5[0-35-9]|6[567]|7[01345-8]|8\d|9[025-9])\d{8}$', phone_number):
            # 邮箱不合法
            return JsonResponse({'status': 217601, 'errmsg': '手机号格式不正确', 'key': 'phone_number'})
        if not all([tpl, phone_number]):
            return JsonResponse({'status': 500202, 'errmsg': '参数不全'})
        exists = Register.objects.filter(phone_number=phone_number).exists()
        if exists:
            return JsonResponse({'status': 221111, 'errmsg': '手机号已注册', 'key': 'phone_number'})

        sms_code = random.randrange(10000, 99999)
        conn = get_redis_connection()
        conn.setex(phone_number, 90, sms_code)
        response = sms.send_sms_single(phone_number, template_id, [sms_code, 3])
        if response['result'] != 0:
            return JsonResponse({'status': 216601, 'errmsg': response['errmsg'], 'key': 'code'})
        return JsonResponse({'status': 200000, 'errmsg': '发送成功'})
