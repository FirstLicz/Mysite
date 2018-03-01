#!/usr/bin/env python
#-*- coding:utf-8 -*- 

__author__ = 'licz'
__time__ = '2018/2/27 8:58'


from course.views import CourseListView,CourseDescView,CourseCommentView,CourseInfoView,CourseAddCommentView,\
    CoursePlayVideoView


from django.conf.urls import url

urlpatterns = [
    url(r'^list/$',CourseListView.as_view(),name='list'),
    url(r'^(?P<course_id>\d+)/detail/$',CourseDescView.as_view(),name='detail'),
    url(r'^(?P<course_id>\d+)/info/$',CourseInfoView.as_view(),name='info'),
    url(r'^(?P<course_id>\d+)/comment/$',CourseCommentView.as_view(),name='comment'),
    url(r'^(?P<video_id>\d+)/video/$',CoursePlayVideoView.as_view(),name='video'),
    #异步添加评论
    url(r'^add_comment/$',CourseAddCommentView.as_view(),name='add_comment'),
]
