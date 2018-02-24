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
        module = UserAsk
        fields = ['name','moblie','course_name']

    def clean_moblie(self):
        moblie = self.cleaned_data['moblie']
        regx = r'1[34578]\d{9}'
        tmp_regx = re.compile(regx)
        if tmp_regx.match(moblie):
            return moblie
        else:
            raise forms.ValidationError('提交数据错误',code='moblie_invalid')


