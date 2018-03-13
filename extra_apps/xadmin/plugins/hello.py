#!/usr/bin/env python
#-*- coding:utf-8 -*- 

__author__ = 'licz'
__time__ = '2018/3/12 14:44'

from django.template import loader
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, ListAdminView, ModelFormAdminView, DetailAdminView


class HelloWorldPlugin(BaseAdminPlugin):
    say_hello = False
    def init_request(self, *args, **kwargs):
        return bool(self.say_hello)

    def block_top_toolbar(self,nodes):

        nodes.append('<p>ddd</p>')




site.register_plugin(HelloWorldPlugin, ListAdminView)
