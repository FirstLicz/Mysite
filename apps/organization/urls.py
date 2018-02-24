#!/usr/bin/env python
#-*- coding:utf-8 -*- 

__author__ = 'licz'
__time__ = '2018/2/23 17:46'


from django.conf.urls import url


from organization.views import OrganzationView,AddUserAskView

urlpatterns = [
    url(r'^$',OrganzationView.as_view(),name='index'),
    url(r'^add_ask/$',AddUserAskView.as_view(),name='adduser'),
]

