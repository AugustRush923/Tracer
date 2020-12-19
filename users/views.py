import random
from django.http import JsonResponse
from django.shortcuts import render
from django_redis import get_redis_connection
from django.conf import settings
# Create your views here.
from users.forms import RegisterForm
from utils.tencent import sms


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})


def send_sms(request):
    if request.method == 'POST':
        tpl = request.POST.get('tpl')
        phone_number = request.POST.get('phone_number')
        if not all([tpl, phone_number]):
            return JsonResponse({'errmsg': '参数不全'})
        if not tpl:
            return JsonResponse({'errmsg': '没有对应模板'})
        template_id = settings.SMS_TEMPLATE_ID.get(tpl)

        if not phone_number:
            return JsonResponse({'errmsg': '手机号不能为空'})
        sms_code = random.randrange(10000, 99999)
        conn = get_redis_connection()
        conn.setex(phone_number, 90, sms_code)
        sms.send_sms_single(phone_number, template_id, [sms_code, 3])
        return JsonResponse({'errmsg': '发送成功'})
