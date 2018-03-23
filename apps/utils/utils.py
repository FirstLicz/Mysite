#!/usr/bin/env python
#-*- coding:utf-8 -*- 

__author__ = 'licz'
__time__ = '2018/3/23 11:38'

from django.db.models import Model
from django.apps import apps
import logging

logger = logging.getLogger('defulat')

def excel_into_model(appname,model_name,excel_file):
    '''
    :param appname: app名称
    :param model_name:  model 名称
    :param excel_file:  excel 文件内容
    :return  [] 返回需要保存的字段数据
    '''
    #tmp[7].verbose_name.__str__()
    try:
        appname_ = apps.get_model(appname,model_name)
        fields = appname_._meta.fields
        #导入model,动态导入
        exec('from %s.models import %s' %(appname,model_name))
    except :
        logger.info('model_name and appname is not exist')
    field_name = []
    #只导入第一个sheet中的数据
    table = excel_file.sheet_by_index(0)
    nrows = table.nrows
    table_header = table.row_values(0)
    for cell in table_header:
        for name in fields:
            if cell in name.verbose_name.__str__():
                field_name.append(name.name)
    if 'add_time' in field_name:
        field_name.remove('add_time')
    for x in range(1, nrows):
        # 行的数据,创建对象,进行报错数据
        exec('obj' + '=%s()' % model_name)
        print(len(field_name))
        for y in range(len(field_name)):
            exec ('obj.%s'%field_name[y]+'="%s"' %(table.cell_value(x,y)))
        exec ('obj.save()')
    return field_name


























