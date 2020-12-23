from django import forms
from django.core.validators import RegexValidator
from users import models


class BootstrapForm(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, fields in self.fields.items():
            fields.widget.attrs = {'class': 'form-control', 'placeholder': f'请输入{fields.label}'}


class RegisterForm(BootstrapForm, forms.ModelForm):
    phone_number = forms.CharField(max_length=11, label='手机号',
                                   validators=[RegexValidator(r'^1([3|4|5|6|7|8|9])\d{9}$', '手机号格式错误')], )
    password = forms.CharField(widget=forms.PasswordInput(),
                               label='密码')
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(),
        label='确认密码')
    code = forms.CharField(label='验证码', widget=forms.TextInput())

    class Meta:
        model = models.Register
        fields = ['username', 'email', 'password', 'confirm_password', 'phone_number', 'code']


class LoginSmsForm(BootstrapForm, forms.Form):
    phone_number = forms.CharField(max_length=11, label='手机号',
                                   validators=[RegexValidator(r'^1([3|4|5|6|7|8|9])\d{9}$', '手机号格式错误')], )
    code = forms.CharField(label='验证码', widget=forms.TextInput())
