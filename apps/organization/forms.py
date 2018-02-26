#!/usr/bin/env python
#-*- coding:utf-8 -*- 

__author__ = 'licz'
__time__ = '2018/2/24 16:07'


'''
    modelform 处理
'''


from django import forms


from operation.models import UserAsk
import re

class UserAskForm(forms.ModelForm):
    '''
        继承modelform ，
    '''
    class Meta:
        model = UserAsk
        fields = ['name','mobile','course_name']

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        regx = r'^1[34578]\d{9}$'
        tmp_regx = re.compile(regx)
        if tmp_regx.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('提交数据错误',code='mobile_invalid')


