#-*- coding:utf-8 -*-
from datetime import datetime


from django.db import models

# Create your models here.


'''
    CourseOrg   -   课程机构基本信息
    Teacher     -   讲师基本信息
    CityDict    -   城市信息
'''

ORG_CATEGORY = (
    ('org','培训机构'),
    ('colleges','高校'),
    ('personal','个人')
)


class CityDict(models.Model):
    name = models.CharField(max_length=50,verbose_name='城市')
    desc = models.CharField(max_length=200,verbose_name='描述')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name='城市'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

class CourseOrg(models.Model):

    name = models.CharField(verbose_name='机构名称',max_length=50)
    category = models.CharField(max_length=20,choices=ORG_CATEGORY,verbose_name='机构类别',default='org')
    desc = models.TextField(verbose_name='机构描述')
    click_nums = models.IntegerField(default=0,verbose_name='点击数')
    fav_nums = models.IntegerField(default=0,verbose_name='收藏数')
    image = models.ImageField(upload_to='courseorg/%Y/%m',verbose_name='封面图')
    address = models.CharField(max_length=150,verbose_name='机构地址')
    city = models.ForeignKey(CityDict,verbose_name='所在城市')
    students = models.IntegerField(verbose_name='学习人数',default=0)
    courses = models.IntegerField(verbose_name='课程数',default=0)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name='课程机构'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

class Teacher(models.Model):

    org = models.ForeignKey(CourseOrg,verbose_name='所属机构')
    name = models.CharField(max_length=50,verbose_name='讲师名')
    image = models.ImageField(upload_to='teacher/%Y/%m',verbose_name='讲师头像',null=True,blank=True)
    work_year = models.IntegerField(default=0,verbose_name='工作年限')
    work_company = models.CharField(max_length=100,verbose_name='所在单位')
    work_position = models.CharField(max_length=50,verbose_name='就职名称')
    domain = models.CharField(max_length=50,verbose_name='教学领域')
    click_nums = models.IntegerField(default=0,verbose_name='点击数')
    fav_nums = models.IntegerField(default=0,verbose_name='收藏数')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name='讲师'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name



