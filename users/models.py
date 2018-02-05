#-*- coding:utf-8 -*-
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


GENDER=(
    ('male','男'),
    ('female','女'),
)

SEND_TYPE=(
    ('register','注册'),
    ('forget','找回')
)

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50,verbose_name=u'昵称',default=u'')
    gender = models.CharField(max_length=6,verbose_name='性别',default='male',choices=GENDER)
    address = models.CharField(max_length=100,verbose_name='地址',null=True,blank=True)
    moblie = models.CharField(max_length=11,verbose_name='手机',null=True,blank=True)
    image = models.ImageField(max_length=100,upload_to='image/%Y/%m',verbose_name='头像',default='image/default.png')

    class Meta:
        verbose_name='用户信息'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.username

#邮箱验证码记录
class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20,verbose_name='验证码',null=False,blank=False)
    email = models.EmailField(max_length=50,verbose_name='邮箱地址')
    send_type = models.CharField(max_length=10,choices=SEND_TYPE,verbose_name='验证码类型')
    send_time = models.DateTimeField(default=datetime.now,verbose_name='发送时间')

    class Meta:
        verbose_name='邮箱验证码'
        verbose_name_plural=verbose_name

class Banner(models.Model):
    title = models.CharField(max_length=100,verbose_name='标题')
    image = models.ImageField(max_length=100,verbose_name='图片地址',upload_to='banner/%Y/%m')
    url = models.URLField(max_length=200,verbose_name='访问地址')
    priority = models.IntegerField(default=100,verbose_name='优先级')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name='轮播图'
        verbose_name_plural=verbose_name


