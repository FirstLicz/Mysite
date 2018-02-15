#!/usr/bin/env python
#-*- coding:utf-8 -*- 

__author__ = 'licz'
__time__ = '2018/2/12 10:42'


from django.contrib.auth.hashers import make_password,check_password
from django.db.models import F,Q
from django.contrib.auth.backends import ModelBackend
from django.shortcuts import render

from .models import UserProfile


import logging


logger = logging.getLogger('defualt')

#获取用户，验证密码
class CustomBackend(ModelBackend):
    def authenticate(self,username=None,password=None,**kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                if check_password(password,user.password):
                    return user
        except Exception as e:
            logger.info('%s is not exit')
            return None



#检测是否登录状态装饰器
def decorate_logging_checker(func):
    def run(request,**kwargs):
        user = request.session.get('_auth_user_id',None)
        if user:
            return render(request,'index.html')
        return func(request,**kwargs)
    return run





