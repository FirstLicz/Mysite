from django.shortcuts import render,HttpResponse
from django.views.generic import View


from .models import Course
from operation.models import UserFavortie
from course.models import CourseResource

from pure_pagination.paginator import Paginator,PageNotAnInteger

# Create your views here.


class CourseListView(View):

    def get(self,request):
        # 获取排序规则
        sort_ = request.GET.get('sort', 'default')
        #遍历所有课程
        all_courses = Course.objects.all().order_by('-add_time')
        if sort_ == 'hot':
            all_courses = Course.objects.all().order_by('-click_nums')
        elif sort_ == 'students':
            all_courses = Course.objects.all().order_by('-students')

        #推荐课程，显示3个课程
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]
        try:
            page = request.GET.get('page',1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses,12,request=request)
        courses = p.page(page)
        return render(request,'course/course-list.html',{
            'courses':courses,'sort':sort_,'hot_courses':hot_courses,

        })


class CourseDescView(View):

    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums+=1
        course.save()
        fav_course_flag = False
        fav_org_flag = False
        if request.user.is_authenticated:
            fav_course_flag = UserFavortie.objects.filter(user=request.user, fav_id=int(course_id), fav_type=1)
            if fav_course_flag:
                fav_course_flag = True
            fav_org_flag = UserFavortie.objects.filter(user=request.user, fav_id=int(course.course_org.id), fav_type=3)
            if fav_org_flag:
                fav_org_flag = True
        return render(request,'course/course-detail.html',{
            'course':course,'fav_org_flag':fav_org_flag,
            'fav_course_flag':fav_course_flag,
        })


class CourseInfoView(View):
    '''
        点击我要学习后的页面
    '''
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        course.students +=1
        course.save()
        lessions = course.lession_set.all()
        return render(request,'course/course-video.html',{
            'course':course,'lessions':lessions,
        })


class CourseCommentView(View):

    def get(self,request,course_id):


        return render(request,'course/course-comment.html')