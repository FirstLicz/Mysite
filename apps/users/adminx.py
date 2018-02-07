#!/usr/bin/env python
#-*- coding:utf-8 -*- 

__author__ = 'licz'
__time__ = '2018/2/7 10:53'


import xadmin
from xadmin import views

from .models import EmailVerifyRecord,Banner


class BaseSetting(object):
    # 显示主题
    enable_themes = True
    use_bootswatch = True


class XdminSettings(object):
    site_title = '慕学在线'
    site_footer = '慕学在线'
    menu_style = 'accordion'   #可折叠的

class EmailVerifyRecordAdminx(object):

    list_display= ['code','email','send_type','send_time']
    search_fields = ['code','email','send_type','send_time']
    list_filter = ['code','email','send_type','send_time']

class BannerAdminx(object):

    list_display= ['title','image','url','priority','add_time']
    search_fields = ['title','priority','add_time']
    list_filter = ['title','priority','add_time']


xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdminx)
xadmin.site.register(Banner,BannerAdminx)

#注册xadmin后台配置

#主题功能

#全局配置
xadmin.site.register(views.CommAdminView,XdminSettings)