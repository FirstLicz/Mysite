#!/usr/bin/env python
#-*- coding:utf-8 -*- 

__author__ = 'licz'
__time__ = '2018/2/7 11:16'


from .models import UserAsk,UserFavortie,UserMessage,CourseComments,UserCourse

import xadmin


class UserAskAdmin(object):
    list_display = ['name','mobile','course_name','add_time']
    search_fields = ['name','mobile','course_name','add_time']
    list_filter = ['name','mobile','course_name','add_time']


class UserFavortieAdmin(object):
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type', 'add_time']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'has_read', 'add_time']
    list_filter = ['user','has_read', 'add_time']


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course', 'add_time']
    list_filter = ['user', 'course', 'add_time']


class CourseCommentsAdmin(object):
    list_display = ['user', 'course','comment', 'add_time']
    search_fields = ['user', 'course', 'add_time']
    list_filter = ['user', 'course', 'add_time']

xadmin.site.register(UserAsk,UserAskAdmin)
xadmin.site.register(UserFavortie,UserFavortieAdmin)
xadmin.site.register(UserMessage,UserMessageAdmin)
xadmin.site.register(UserCourse,UserCourseAdmin)
xadmin.site.register(CourseComments,CourseCommentsAdmin)