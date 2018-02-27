#!/usr/bin/env python
#-*- coding:utf-8 -*- 

__author__ = 'licz'
__data__ = ' 10:07'

import sys,os
from xlrd import open_workbook
from xlutils.copy import copy
from xlwt import Style,Workbook
import MySQLdb,datetime
import calendar


#嗨皮大厅记录
db_list=['web_pv','payment_system_db']
#db_list=['web_pv','hall_interface_dx_guangxi']
mysql_data={
     "host":'192.168.44.94',
     "user":'winside',
     "passwd":'soigRw5DwugEgGji',
    #"host":'127.0.0.1',
    #"user":'root',
    #"passwd":'lcz123456',
}

hall_data_ceil=[u'PV',u'UV',u'日期',u'产品订购数',u'订购时间',]

product_list=['gamemonthhall','gamemonthhallhd','edu_pic_book','videomonthhall','gamehallphone2',
              'gamehallphone3','gamehallphone10','gamemonthhalltwo','gamemonthhalltwohd','eduwismami',
              'edu_pic_bookhd','videomonthhallhd','gamemonthtwo_once','gamemonthtwohd_once','edu_pic_book_once',]


def init_ceil_data(argument):
    data_ceil=[]
    for data in argument:
        if data in product_list:
            data_ceil.append(data)
    if data_ceil:
        tmp=hall_data_ceil[:-2]
        tmp.extend(data_ceil)
        tmp.append(u'订购时间')
        return tmp
    else:
        return hall_data_ceil


#初始化创建xls文件,并初始化头部
def init_excel(filename,data_list,styl=Style.default_style,num=0):
    new_file=Workbook()
    for i in xrange(num+1):
        table=new_file.add_sheet('sheet'+str(i)) # 用xlwt对象的方法获得要操作的sheet
        for x in xrange(len(data_list)):
            table.write(0, x, data_list[x], styl)  # xlwt对象的写方法，参数分别是行、列、值
    new_file.save(filename)

def write_xls(filename,data_list,wirte_column,num=0):
    '''
    :param filename:文件名
    :param data_list:数据list or tulpe
    :param wirte_column: 从第几列开始写入数据
    :param num:sheet编号
    :return:
    '''
    # 写入Excel
    rexcel = open_workbook(filename)  # 用wlrd提供的方法读取一个excel文件
    excel = copy(rexcel)  # 用xlutils提供的copy方法将xlrd的对象转化为xlwt的对象
    for x in xrange(num+1):
        table = excel.get_sheet(num)  # 用xlwt对象的方法获得要操作的sheet
        for k in range(len(data_list)):         #处理行数据
            for j in xrange(len(data_list[0])): #处理列数据
                table.write(k + 1, j+wirte_column, data_list[k][j])  # xlwt对象的写方法，参数分别是行、列、值
    excel.save(filename)  # xlwt对象的保存方法，这时便覆盖掉了原来的excel

def init_time(time_1):
    time_arr = time_1.split('-')
    if len(time_arr) == 1:
        time_arr = time_1.split('.')
    cur_day = time_arr[-1]
    code,msg=0,''
    if int(time_arr[1]) < 0 or int(time_arr[1]) > 12:
        msg=u'月份不在1-12之间'
        code = -1
    current_day = calendar.monthrange(int(time_arr[0]), int(time_arr[1]))[1]
    if current_day < int(cur_day):
        msg=u'天数超出当前月天数'
        code = -2
    return msg,code,time_arr

def date_list(c_key,time_1,time_2,args=[]):
    context_list=[]
    msg_1,code_1,time_arr_1=init_time(time_1)
    msg_2, code_2 ,time_arr_2= init_time(time_2)
    tmp_dict={}
    for j in xrange(len(args)):
        if args[j] in product_list:
            tmp_dict.update({'product_%s' % (j + 1): args[j]})
    print tmp_dict
    if code_2!=0 and code_1!=0:
        raise IOError,(u'时间输入错误')
    tmp=abs(int(time_arr_2[1])-int(time_arr_1[1]))
    for num in xrange(tmp+1):
        if num==0:
            start_time = time_arr_1[0] + '-' + time_arr_1[1] + '-' + time_arr_1[2]
            end_time=time_arr_1[0]+'-'+time_arr_1[1]+'-'+ str(calendar.monthrange(int(time_arr_1[0]) + num, int(time_arr_1[1]))[1])
        else:
            if int(time_arr_2[1]) == int(time_arr_1[1])+num:
                start_time = time_arr_1[0] + '-' + str(int(time_arr_1[1]) + num) + '-' + '01'
                end_time = time_arr_2[0] + '-' + time_arr_2[1] + '-' + time_arr_2[2]
                context_list.append(dict({"start_time":start_time,"end_time":end_time,"c_key":c_key,'year':time_arr_1[0] ,"month":str(int(time_arr_1[1]) + num)},**tmp_dict))
                break
            start_time = time_arr_1[0]+'-'+str(int(time_arr_1[1])+num)+'-'+ '01'
            end_time = time_arr_1[0]+'-'+str(int(time_arr_1[1])+num)+'-'+ str(calendar.monthrange(int(time_arr_1[0]) ,int(time_arr_1[1])+ num)[1])
        context_list.append(dict({"start_time": start_time, "end_time": end_time, "c_key": c_key, 'year': time_arr_1[0],"month": str(int(time_arr_1[1]) + num)},**tmp_dict))
    return context_list

def date_str(data_):
    '''
    :param data_: 二维列表数据
    :return:  string类型数据
    '''
    if len(data_)!=0:
        date_list = []
        for j in xrange(len(data_)):
            if isinstance(data_[j],(list,tuple)):
                date_list_ = []
                for k in xrange(len(data_[j])):
                    if isinstance(data_[j][k],(datetime.datetime,datetime.date)):
                        cell_=data_[j][k].strftime('%Y-%m-%d')
                        date_list_.append(cell_)
                    else:
                        date_list_.append(data_[j][k])
                date_list.append(date_list_)
        return date_list
    else:
        return None

def conn_mysql(context):
    try:
        #链接web_pv数据库
        conn=MySQLdb.connect(host=mysql_data['host'],user=mysql_data['user'],passwd=mysql_data['passwd'],db=db_list[0],port=3306)
        cur=conn.cursor()
        conn.set_character_set('utf8')
        # PV和UV,
        sql='''
        select count(userid) ,count(distinct(userid)),create_date from pv_zsjpv_%(year)s_%(month)s where 
        create_date BETWEEN '%(start_time)s' and '%(end_time)s' and c_key like '%%%(c_key)s%%' group by create_date
        ''' %(context)
        cur.execute(sql)
        print sql
        data_ = cur.fetchall()
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    return data_

def select_order(context):
    # 查看订购记录
    index_num=0
    for k,v in context.items():
        if v in product_list:
            index_num+=1
    try:
        conn = MySQLdb.connect(host=mysql_data['host'], user=mysql_data['user'],passwd=mysql_data['passwd'], db=db_list[1], port=3306)
        cur = conn.cursor()
        if index_num != 0:
            sql_order_month = """
            select count(c_userid),DATE(c_addTime) from t_month_pay_order where c_czMemo like  '%%%(c_key)s%%' AND c_product='%(product_1)s'
            and c_czState=1  and DATE(c_addTime) BETWEEN '%(start_time)s' and '%(end_time)s' GROUP BY DATE(c_addTime);
            """ % (context)
        else:
            sql_order_month="""
            select count(c_userid),DATE(c_addTime) from t_month_pay_order where c_czMemo like  '%%%(c_key)s%%' 
            and c_czState=1  and DATE(c_addTime) BETWEEN '%(start_time)s' and '%(end_time)s' GROUP BY DATE(c_addTime);
            """ %(context)
        print sql_order_month
        cur.execute(sql_order_month)
        result_pay=cur.fetchall()
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    return result_pay


if __name__=="__main__":
    if len(sys.argv) >= 3:
        current_name = sys.argv[1] + sys.argv[2] + '_' + sys.argv[3][-2:]
    else:
        current_name = os.path.split(sys.argv[0])[1].split('.')[0]
        raise IOError,(u'参数不足，activity_key,start_time,end_time,可带产品名')
    filename_hall = current_name + '.xls'
    #hall_data_=init_ceil_data(sys.argv)
    print filename_hall
    dates = date_list(sys.argv[1], sys.argv[2], sys.argv[3])
    print dates
    tmp=3
    init_excel(filename_hall, hall_data_ceil, num=len(dates))
    for x in xrange(len(dates)):
        data=conn_mysql(dates[x])
        data=date_str(data)
        data_1=select_order(dates[x])
        data_1 = date_str(data_1)
        print data
        print data_1
        if data is not None:
            write_xls(filename_hall, data, wirte_column=0, num=x)
        if data_1 is not None:
            write_xls(filename_hall, data_1, wirte_column=tmp, num=x)

