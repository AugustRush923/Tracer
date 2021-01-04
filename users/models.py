from django.db import models


# Create your models here.


class Register(models.Model):
    username = models.CharField(max_length=32, verbose_name='用户名')
    email = models.EmailField(verbose_name='邮箱')
    phone_number = models.CharField(max_length=11, verbose_name='手机号')
    password = models.CharField(max_length=16, verbose_name='密码')


class PriceStrategy(models.Model):
    category_choice = (
        (0, '免费版'),
        (1, 'VIP'),
        (2, 'SVIP')
    )
    category = models.SmallIntegerField(choices=category_choice, default=0, verbose_name='分类')
    title = models.CharField(max_length=64, verbose_name='标题')
    price = models.FloatField(verbose_name='价格/年')
    project_num = models.PositiveIntegerField(verbose_name='创建项目个数')
    project_member = models.PositiveIntegerField(verbose_name='项目成员')
    project_space = models.PositiveIntegerField(verbose_name='项目空间')
    single_file = models.PositiveIntegerField(verbose_name='单个文件')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')


class Transaction(models.Model):
    status_choice = (
        (0, '未支付'),
        (1, '已成功')
    )
    status = models.SmallIntegerField(choices=status_choice, default=0, verbose_name='订单状态')
    order = models.CharField(max_length=64, unique=True, verbose_name='订单号')
    user = models.ForeignKey(to="Register", verbose_name='用户', on_delete=models.CASCADE)
    price_strategy = models.ForeignKey(to="PriceStrategy", verbose_name='价格策略', on_delete=models.CASCADE)
    count = models.PositiveIntegerField(verbose_name='数量(年)', help_text='0为无限时限')
    price = models.FloatField(verbose_name='实际支付金额')
    start_time = models.DateTimeField(null=True, blank=True, verbose_name='开始时间')
    end_time = models.DateTimeField(null=True, blank=True, verbose_name='结束时间')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')


class Project(models.Model):
    color_choice = (
        (0, '#56b8eb'),
        (1, '#f28033'),
        (2, '#ebc656'),
        (3, '#a2d148'),
        (4, '#20BFA4'),
        (5, '#7461c2'),
        (6, '#20bfa3'),
    )
    name = models.CharField(max_length=32, verbose_name='项目名称')
    color = models.SmallIntegerField(choices=color_choice, default=0, verbose_name='颜色')
    desc = models.CharField(max_length=255, null=True, blank=True, verbose_name='项目描述')
    use_space = models.PositiveIntegerField(verbose_name='项目使用空间', default=0)
    star = models.BooleanField(verbose_name='星标', default=False)
    join_count = models.PositiveSmallIntegerField(verbose_name='参与人数', default=1)
    founder = models.ForeignKey(to="Register", verbose_name='创建者', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')


class ProjectUser(models.Model):
    user = models.ForeignKey(verbose_name='用户', to='Register', related_name='projects', on_delete=models.CASCADE)
    project = models.ForeignKey(verbose_name='项目', to='Project', on_delete=models.CASCADE)
    invitee = models.ForeignKey(verbose_name='邀请者', to='Register', related_name='invites', null=True, blank=True,
                                on_delete=models.CASCADE)
    star = models.BooleanField(verbose_name='星标', default=False)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
