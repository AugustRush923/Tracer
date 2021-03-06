# Generated by Django 2.2 on 2021-01-04 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceStrategy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.SmallIntegerField(choices=[(0, '免费版'), (1, 'VIP'), (2, 'SVIP')], default=0, verbose_name='分类')),
                ('title', models.CharField(max_length=64, verbose_name='标题')),
                ('price', models.FloatField(verbose_name='价格/年')),
                ('project_num', models.PositiveIntegerField(verbose_name='创建项目个数')),
                ('project_member', models.PositiveIntegerField(verbose_name='项目成员')),
                ('project_space', models.PositiveIntegerField(verbose_name='项目空间')),
                ('single_file', models.PositiveIntegerField(verbose_name='单个文件')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='项目名称')),
                ('color', models.SmallIntegerField(choices=[(0, '#56b8eb'), (1, '#f28033'), (2, '#ebc656'), (3, '#a2d148'), (4, '#20BFA4'), (5, '#7461c2'), (6, '#20bfa3')], default=0, verbose_name='颜色')),
                ('desc', models.CharField(blank=True, max_length=255, null=True, verbose_name='项目描述')),
                ('use_space', models.PositiveIntegerField(default=0, verbose_name='项目使用空间')),
                ('star', models.BooleanField(default=False, verbose_name='星标')),
                ('join_count', models.PositiveSmallIntegerField(default=1, verbose_name='参与人数')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('founder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Register', verbose_name='创建者')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(choices=[(0, '未支付'), (1, '已成功')], default=0, verbose_name='订单状态')),
                ('order', models.CharField(max_length=64, unique=True, verbose_name='订单号')),
                ('count', models.PositiveIntegerField(help_text='0为无限时限', verbose_name='数量(年)')),
                ('price', models.FloatField(verbose_name='实际支付金额')),
                ('start_time', models.DateTimeField(blank=True, null=True, verbose_name='开始时间')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='结束时间')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('price_strategy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.PriceStrategy', verbose_name='价格策略')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Register', verbose_name='用户')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.BooleanField(default=False, verbose_name='星标')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建日期')),
                ('invitee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invites', to='users.Register', verbose_name='邀请者')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Project', verbose_name='项目')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='users.Register', verbose_name='用户')),
            ],
        ),
    ]
