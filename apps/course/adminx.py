#!/usr/bin/env python
#-*- coding:utf-8 -*- 

__author__ = 'licz'
__time__ = '2018/2/7 11:16'


import xadmin

from .models import Course,CourseResource,Video,Lession,BannerCourse
from users.models import Banner


class LessonInline(object):
    model = Lession
    extra = 0

class CourseResourceInline(object):
    model = CourseResource
    extra = 0



class CourseAdmin(object):

    list_display = ['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time','get_lession_num']
    search_field = ['name','degree','learn_times','students','fav_nums','click_nums','add_time']
    list_filter = ['name','degree','learn_times','students','fav_nums','click_nums','add_time']
    readonly_fields = ['fav_nums']
    #list_editable 设置可编辑字段
    list_editable = ['degree']
    refresh_times = ['3',]
    inlines = [LessonInline,CourseResourceInline]
    style_fields = {'detail':'ueditor'}

    def queryset(self):
        qs = super(CourseAdmin,self).queryset()
        qs = qs.filter(is_banner = False)
        return qs

    def save_models(self):
        #在保存课程是后统计课程的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.courses = Course.objects.filter(course_org=course_org).count()
            course_org.save()

class BannerCourseAdmin(object):

    list_display = ['name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time','get_lession_num','get_goto','get_org_name']
    search_field = ['name','degree','learn_times','students','fav_nums','click_nums','add_time']
    list_filter = ['name','degree','learn_times','students','fav_nums','click_nums','add_time']
    readonly_fields = ['fav_nums']
    refresh_times = ['3',]
    inlines = [LessonInline,CourseResourceInline]

    def queryset(self):
        qs = super(BannerCourseAdmin,self).queryset()
        qs = qs.filter(is_banner = True)
        return qs

    def save_models(self):
        #在保存课程是后统计课程的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.courses = Course.objects.filter(course_org=course_org).count()
            course_org.save()


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
#注册新的model，到指定的后台位置。
xadmin.site.register(BannerCourse,BannerCourseAdmin)

xadmin.site.register(Lession,LessionAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)
