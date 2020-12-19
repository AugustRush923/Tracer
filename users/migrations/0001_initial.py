# Generated by Django 2.2 on 2020-12-19 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, verbose_name='用户名')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('phone_number', models.CharField(max_length=11, verbose_name='手机号')),
                ('password', models.CharField(max_length=16, verbose_name='密码')),
            ],
        ),
    ]