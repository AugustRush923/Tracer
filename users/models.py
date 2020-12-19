from django.db import models

# Create your models here.


class Register(models.Model):
    username = models.CharField(max_length=32, verbose_name='用户名')
    email = models.EmailField(verbose_name='邮箱')
    phone_number = models.CharField(max_length=11, verbose_name='手机号')
    password = models.CharField(max_length=16, verbose_name='密码')
