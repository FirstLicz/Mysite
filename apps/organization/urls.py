#!/usr/bin/env python
#-*- coding:utf-8 -*- 

__author__ = 'licz'
__time__ = '2018/2/23 17:46'


from django.conf.urls import url


from organization.views import OrganzationView,AddUserAskView,OrgHomeView,OrgCourseView,\
    OrgDescView,OrgTeacherView,AddFavOrgView,TeacherListView,TeacherDetailView


urlpatterns = [
    url(r'^list/$',OrganzationView.as_view(),name='list'),
    url(r'^add_ask/$',AddUserAskView.as_view(),name='adduser'),
    url(r'^(?P<org_id>.*)/org_home/$',OrgHomeView.as_view(),name='org_home'),
    url(r'^(?P<org_id>.*)/org_course/$',OrgCourseView.as_view(),name='org_course'),
    url(r'^(?P<org_id>.*)/org_desc/$',OrgDescView.as_view(),name='org_desc'),
    url(r'^(?P<org_id>.*)/org_teacher/$',OrgTeacherView.as_view(),name='org_teacher'),

    #讲师列表页
    url(r'^teacher/list/$',TeacherListView.as_view(),name='teacher_list'),

    url(r'^teacher/(?P<teacher_id>\d+)/detail/$',TeacherDetailView.as_view(),name='teacher_detail'),
    #用户收藏,异步url
    url(r'^add_fav/$',AddFavOrgView.as_view(),name='org_addfav'),
]

