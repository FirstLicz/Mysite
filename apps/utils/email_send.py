#!/usr/bin/env python
#-*- coding:utf-8 -*- 

__author__ = 'licz'
__time__ = '2018/2/23 8:50'

from django.core.mail import send_mail
from users.models import EmailVerifyRecord
from Mxonline.settings import EMAIL_FROM

from random import Random
from string import ascii_lowercase,ascii_uppercase

def send_email(email,send_type='register'):
    email_record = EmailVerifyRecord()
    code = generate_random_str(16)
    email_record.code=code
    email_record.email = email
    email_record.send_type=send_type
    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = '慕学在线网注册激活链接'
        email_body = '请点击下面的链接激活你的账号:http://127.0.0.1:8000/active/{0}'.format(code)

        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            print(send_status)
    elif send_type == 'forget':
        email_title = '慕学在线网注册密码重置链接'
        email_body = '请点击下面的链接重置密码:http://127.0.0.1:8000/reset/{0}/{1}'.format(email,code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            print(send_status)

def generate_random_str(random_length=8):
    str_ , str_code = '',''
    for i in range(len(ascii_uppercase)):
        str_ += ascii_lowercase[i] + ascii_uppercase[i]
    str_+='0123456789'
    random = Random()
    length = len(str_)-1
    for i in range(random_length):
        str_code+=str_[random.randint(0,length)]
    return str_code







