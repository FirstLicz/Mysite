#!/usr/bin/env python
#-*- coding:utf-8 -*- 

__author__ = 'licz'
__time__ = '2018/2/7 11:16'


import xadmin


from .models import Course,CourseResource,Video,Lession


class CourseAdmin(object):

    list_display = ['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time']
    search_field = ['name','degree','learn_times','students','fav_nums','click_nums','add_time']
    list_filter = ['name','degree','learn_times','students','fav_nums','click_nums','add_time']


class CourseResourceAdmin(object):

    list_display = ['course','name','add_time','resource_file']
    search_field = ['course','name','add_time']
    list_filter = ['course','name','add_time']


class VideoAdmin(object):

    list_display = ['lession','name','video_url','add_time']
    search_field = ['lession','name','add_time']
    list_filter = ['lession','name','add_time']


class LessionAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_field = ['course', 'name', 'add_time']
    list_filter = ['course', 'name', 'add_time']


xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lession,LessionAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)
