#-*- coding:utf-8 -*-
from datetime import datetime


from django.db import models

# Create your models here.


'''
    CourseOrg   -   课程机构基本信息
    Teacher     -   讲师基本信息
    CityDict    -   城市信息
'''


class CourseOrg(models.Model):

    name = models.CharField(verbose_name='课程机构名',max_length=50)




