#!/usr/bin/env python
#-*- coding:utf-8 -*- 

__author__ = 'licz'
__time__ = '2018/2/7 11:16'


import xadmin
from xlrd import open_workbook

from django.shortcuts import HttpResponseRedirect

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
    import_excel = True


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
    #定义重载post方法来获取excel表格中的数据
    def post(self,request,*args,**kwargs):
        if 'excel' in request.FILES:
            execl_file = request.FILES.get('excel')
            print(execl_file)
            files = open_workbook(filename=None, file_contents=request.FILES['excel'].read())
            print(files.sheet_by_index(0).cell(0,0))
            print(len(files.sheet_names()))
            for index in range(len(files.sheet_names())):
                table = files.sheet_by_index(index)
                nrows= table.nrows
                print(nrows)
                for x in range(1,nrows):
                    course = Course()
                    #取出单元数据name','desc','detail','degree','learn_times','students','fav_nums','image','click_nums','add_time
                    course.name = files.sheet_by_index(index).row_values(x)[0]
                    course.desc = files.sheet_by_index(index).row_values(x)[1]
                    course.detail = files.sheet_by_index(index).row_values(x)[2]
                    course.degree = files.sheet_by_index(index).row_values(x)[3]
                    tmp = files.sheet_by_index(index).row_values(x)[4]
                    print(type(tmp))
                    course.learn_times = int(files.sheet_by_index(index).row_values(x)[4])
                    course.students = int(files.sheet_by_index(index).row_values(x)[5])
                    course.fav_nums = int(files.sheet_by_index(index).row_values(x)[6])
                    course.image.name = files.sheet_by_index(index).row_values(x)[7]
                    course.click_nums = int(files.sheet_by_index(index).row_values(x)[8])
                    #course.add_time = files.sheet_by_index(index).cell(x,9)
                    course.save()
            return HttpResponseRedirect('/xadmin/course/course')
        return super(CourseAdmin,self).post(request,*args,**kwargs)

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
