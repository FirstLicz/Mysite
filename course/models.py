#-*- coding:utf-8 -*-
from datetime import datetime


from django.db import models

# Create your models here.

DEGREE=(
    ('cj','初级'),
    ('zj','中级'),
    ('gj','高级'),
)


class Course(models.Model):
    name = models.CharField(max_length=50,verbose_name='课程名')
    desc = models.CharField(max_length=300,verbose_name='课程描述')
    detail = models.TextField(verbose_name='课程详情',null=True,blank=True)
    degree = models.CharField(max_length=2,choices=DEGREE,verbose_name='等级')
    learn_times = models.IntegerField(default=0,verbose_name='学习时长',help_text='存储单位是分钟')
    students = models.IntegerField(default=0,verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0,verbose_name='收藏人数')
    image = models.ImageField(upload_to='course/%Y/%m',verbose_name='课程封面')
    click_nums = models.IntegerField(default=0,verbose_name='点击数')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name='课程'
        verbose_name_plural=verbose_name

