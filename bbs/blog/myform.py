from django import forms
from django.forms import widgets
from blog.models import User
from django.core.exceptions import ValidationError


class Myform(forms.Form):
    username = forms.CharField(max_length=10, min_length=3, label='用户名',
                               error_messages={
                                   'max_length': '用户名超出长度',
                                   'min_length': '用户名最短为3',
                                   'required': "用户名不能为空"},
                               widget=widgets.TextInput(attrs={'class': "form-control"})
                               )
    password = forms.CharField(max_length=18, min_length=6, label='密码',
                               error_messages={
                                   'max_length': '密码超出长度',
                                   'min_length': '密码最短为6',
                                   'required': "密码不能为空"
                               },
                               widget=widgets.PasswordInput(attrs={'class': "form-control"})
                               )
    re_password = forms.CharField(max_length=18, min_length=6, label='确认密码',
                                  error_messages={
                                      'max_length': '密码超出长度',
                                      'min_length': '密码最短为6',
                                      'required': "密码不能为空"
                                  },
                                  widget=widgets.PasswordInput(attrs={'class': "form-control"})
                                  )
    telephone = forms.CharField(max_length=11, min_length=11, label='手机号码',
                                error_messages={
                                    'max_length': '电话号码超出长度',
                                    'min_length': '电话号码最短为6',
                                    'required': "号码不能为空"
                                },
                                widget=widgets.TextInput(attrs={'class': "form-control"})
                                )  # ?
    email = forms.EmailField(label='邮箱',
                             error_messages={
                                 'invalid': '格式错误',
                                 'required': "不能为空"
                             },
                             widget=widgets.TextInput(attrs={'class': "form-control"})
                             )

    def clean_username(self):
        name = self.cleaned_data.get('username')
        user = User.objects.filter(username=name).first()
        if user:
            raise ValidationError('用户已存在')
        else:
            return name

    def clean(self):
        pwd = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_password')
        if pwd != re_pwd:
            raise ValidationError('两次密码不一致')
        else:
            return self.cleaned_data
