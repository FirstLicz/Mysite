#!/usr/bin/env python
#-*- coding:utf-8 -*- 

__author__ = 'licz'
__time__ = '2018/2/27 10:07'


from django.template import Library
from django.template.defaultfilters import stringfilter


register = Library()

@register.filter
@stringfilter
def my_division(val,args):
    result_h = val //args
    result_m = val % args
    if result_h > 0 and result_m >0:
        return '{0}小时{1}分钟'.format(result_h,result_m)
    elif result_h > 0 and result_m ==0:
        return '{0}小时'.format(result_h)
    else:
        return '{0}分钟'.format(result_m)
