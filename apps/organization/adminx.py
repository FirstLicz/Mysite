#!/usr/bin/env python
#-*- coding:utf-8 -*- 

__author__ = 'licz'
__time__ = '2018/2/7 11:16'


from .models import CityDict,CourseOrg,Teacher


import xadmin


class CityDictAdmin(object):
    list_display=['name','desc','add_time']
    search_fields = ['name','add_time']
    list_filter = ['name','add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'image', 'address', 'city', 'add_time']
    search_fields = ['name', 'click_nums', 'fav_nums', 'city', 'add_time']
    list_filter = ['name', 'click_nums', 'fav_nums', 'city', 'add_time']


class TeacherAdmin(object):
    list_display = ['org','name', 'work_year','work_company','work_position','domain','click_nums','fav_nums', 'add_time']
    search_fields = ['org','name', 'work_year','work_company','work_position','domain','click_nums','fav_nums', 'add_time']
    list_filter = ['org','name', 'work_year','work_company','work_position','domain','click_nums','fav_nums', 'add_time']


xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)