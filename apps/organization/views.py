from django.shortcuts import render,HttpResponse
from django.views.generic import View
from django.core.paginator import Paginator
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


from organization.models import CourseOrg,CityDict,Teacher
from organization.forms import UserAskForm
from course.models import Course
from operation.models import UserFavortie


import json
import logging

# Create your views here.


logger = logging.getLogger('default')

class OrganzationView(View):

    def get(self,request):
        #所有机构
        all_orgs = CourseOrg.objects.all()
        #机构的排名
        orgs_order = all_orgs.order_by('-click_nums')[:3]
        #所有城市
        all_city = CityDict.objects.all()
        #筛选城市
        city_id = request.GET.get('city','')
        if city_id:
            all_orgs=all_orgs.filter(city=int(city_id))
        # 筛选类别
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)
        #根据排序选项
        sort_category = request.GET.get('sort','')
        if sort_category:
            all_orgs = all_orgs.order_by('-'+sort_category)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(all_orgs,5, request=request)
        orgs = p.page(page)
        return render(request,'organization/org-list.html',{
            'all_orgs':orgs,'all_city':all_city,
            'city_id':city_id,'category':category,'orgs_order':orgs_order,
            'sort_category':sort_category,'flag':'org'
        })


class AddUserAskView(View):
    '''
        用户添加咨询;
        json 格式的标准：' {"key":"val"} '
    '''
    def post(self,request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg": "添加出错"}',content_type='application/json')


class OrgHomeView(View):

    def get(self,request,org_id):
        #获取结构
        course_org=CourseOrg.objects.get(id=org_id)
        #获取所有讲师
        teachers = course_org.teacher_set.all()[:1]
        #获取所有课程
        courses = course_org.course_set.all()[:3]
        fav_flag = False
        fav_org = UserFavortie.objects.filter(user=request.user,fav_id=int(org_id),fav_type=3)
        if fav_org:
            fav_flag = True
        return render(request,'organization/org-detail-homepage.html',{
            'course_org':course_org,'teachers':teachers,
            'courses':courses,'current_flag':'home',
            'fav_flag':fav_flag,
        })


class OrgCourseView(View):

    def get(self,request,org_id):
        #获取结构
        course_org=CourseOrg.objects.get(id=org_id)
        #获取所有讲师
        teachers = course_org.teacher_set.all()[:1]
        #获取所有课程
        courses = course_org.course_set.all()
        fav_flag = False
        fav_org = UserFavortie.objects.filter(user=request.user, fav_id=int(org_id), fav_type=3)
        if fav_org:
            fav_flag = True
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # Provide Paginator with the request object for complete querystring generation
        p = Paginator(courses,8, request=request)
        courses = p.page(page)
        return render(request,'organization/org_detail_course.html',{
            'course_org':course_org,'teachers':teachers,
            'courses':courses,'current_flag':'course',
            'fav_flag':fav_flag,
        })


class OrgDescView(View):

    def get(self,request,org_id):
        # 获取机构
        course_org = CourseOrg.objects.get(id=org_id)
        fav_flag = False
        fav_org = UserFavortie.objects.filter(user=request.user, fav_id=int(org_id), fav_type=3)
        if fav_org:
            fav_flag = True
        return render(request,'organization/org_detail_desc.html',{
            'course_org':course_org,'current_flag':'desc',
            'fav_flag':fav_flag,
        })


class OrgTeacherView(View):
    '''
        机构，讲师列表页
    '''
    def get(self,request,org_id):
        # 获取机构
        course_org = CourseOrg.objects.get(id=org_id)
        teachers = course_org.teacher_set.all()
        fav_flag = False
        fav_org = UserFavortie.objects.filter(user=request.user, fav_id=int(org_id), fav_type=3)
        if fav_org:
            fav_flag = True
        return render(request,'organization/org_detail_teacher.html',{
            'course_org':course_org,'current_flag':'teacher',
            'teachers':teachers,'fav_flag':fav_flag,
        })


class TeacherListView(View):
    '''
        讲师列表页
    '''
    def get(self,request):
        sort_ = request.GET.get('sort','default')
        teachers = Teacher.objects.all()
        # 排序过滤
        if sort_=='hot':
            teachers = teachers.order_by('-click_nums')
        #讲师排行
        order_teachers = teachers.order_by('-click_nums')[:10]
        all_persons = len(teachers)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # 分页显示
        p = Paginator(teachers,5, request=request)
        teachers = p.page(page)
        return render(request,'organization/teachers-list.html',{
            'flag':'teacher',"teachers":teachers,
            'sort_':sort_,'order_teachers':order_teachers,
            "all_persons":all_persons,
        })


class TeacherDetailView(View):

    def get(self,request,teacher_id):
        try:
            teacher = Teacher.objects.get(id=int(teacher_id))
        except:
            logger.info('teacher_id=%s is not exist' %(teacher_id))
            return HttpResponse('<h1>网页不存在404</h1>')
        t_courses = teacher.course_set.all()
        t_ranking = Teacher.objects.filter(org=teacher.org).order_by('-click_nums')[:10]
        #查询机构收藏
        flag_org = False
        result = UserFavortie.objects.filter(user=request.user,fav_id=teacher.org_id,fav_type=3)
        if result:
            flag_org = True
        # 查询讲师收藏
        flag_teacher = False
        result = UserFavortie.objects.filter(user=request.user, fav_id=teacher.id, fav_type=2)
        if result:
            flag_teacher = True
        return render(request,'organization/teacher-detail.html',{
            'teacher':teacher,'flag':'teacher',
            't_ranking':t_ranking,'t_courses':t_courses,
            'flag_org':flag_org,'flag_teacher':flag_teacher,
        })


class AddFavOrgView(View):
    '''
        用户收藏，取消收藏;机构收藏
    '''
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)
        fav_type = request.POST.get('fav_type',0)
        context = {}
        context['status'] = 'success'
        context['msg'] = '收藏'
        if request.user.is_authenticated:
            if int(fav_id) > 0 and int(fav_type) > 0:
                exist_record = UserFavortie.objects.filter(fav_id=int(fav_id), fav_type=int(fav_type))
                if exist_record:
                    exist_record.delete()
                    return HttpResponse(json.dumps(context), content_type='application/json')
                else:
                    user_fav = UserFavortie()
                    user_fav.fav_id = int(fav_id)
                    user_fav.fav_type = fav_type
                    user_fav.user = request.user
                    user_fav.save()
                    context['msg'] = '已收藏'
                    return HttpResponse(json.dumps(context), content_type='application/json')
            else:
                context['status'] = 'fail'
                context['msg'] = '网络异常'
                return HttpResponse(json.dumps(context), content_type='application/json')
        else:
            context['status'] = 'success'
            context['msg'] = '用户未登录'
            return HttpResponse(json.dumps(context), content_type='application/json')



