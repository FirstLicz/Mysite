#-*- coding:utf-8 -*-
from datetime import datetime


from django.db import models

# Create your models here.
'''
    course          课程基本信息
    lession         章节信息
    video           视频信息
    courseresource  课程资源
'''


DEGREE=(
    ('cj','初级'),
    ('zj','中级'),
    ('gj','高级'),
    ('dj','顶级'),
)


class Course(models.Model):
    name = models.CharField(max_length=50,verbose_name='课程名')
    desc = models.CharField(max_length=300,verbose_name='课程描述')
    detail = models.TextField(verbose_name='课程详情',null=True,blank=True)
    degree = models.CharField(max_length=2,choices=DEGREE,verbose_name='等级')
    learn_times = models.IntegerField(default=0,verbose_name='学习时长',help_text='存储单位是分钟')
    students = models.IntegerField(default=0,verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0,verbose_name='收藏人数')
    image = models.ImageField(max_length=200,upload_to='course/%Y/%m',verbose_name='课程封面')
    click_nums = models.IntegerField(default=0,verbose_name='点击数')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name='课程'
        verbose_name_plural=verbose_name


class Lession(models.Model):

    course = models.ForeignKey(Course,verbose_name='课程')
    name = models.CharField(max_length=100,verbose_name='章节名',null=False,blank=False)
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name='章节'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name


class Video(models.Model):

    lession = models.ForeignKey(Lession,verbose_name='章节')
    name = models.CharField(max_length=50,verbose_name='视频名')
    video_url = models.FileField(max_length=200,upload_to='course/video/%Y/%m',verbose_name='视频',help_text='视频路劲')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name='视频'
        verbose_name_plural=verbose_name


class CourseResource(models.Model):

    course = models.ForeignKey(Course,verbose_name='课程')
    name = models.CharField(max_length=100,verbose_name='资源名')
    resource_file = models.FileField(max_length=200,upload_to='course/resource/%Y/%m',verbose_name='资源文件')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name='课程资源'
        verbose_name_plural=verbose_name



