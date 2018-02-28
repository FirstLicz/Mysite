from django.shortcuts import render,HttpResponse
from django.views.generic import View


from .models import Course
from operation.models import UserFavortie,CourseComments,UserCourse
from course.models import CourseResource
from utils.login_utils import LoginRequiredMust


from pure_pagination.paginator import Paginator,PageNotAnInteger
import json
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
        if request.user.is_authenticated():
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


class CourseInfoView(LoginRequiredMust,View):
    '''
        点击我要学习后的页面
    '''
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        course.students +=1
        course.save()
        flag_tag = 'video'
        course_users = UserCourse.objects.filter(course=course)
        #遍历改课程学的学生所有ID
        user_ids = [ cours.user.id for cours in course_users ]
        #找出课程中学生

        lessions = course.lession_set.all()
        return render(request,'course/course-video.html',{
            'course':course,'lessions':lessions,
            'flag_tag':flag_tag,
        })


class CourseCommentView(LoginRequiredMust,View):
    '''
        课程的评论
    '''
    def get(self,request,course_id):
        flag_tag = 'comment'
        course = Course.objects.get(id=int(course_id))
        all_comments = course.coursecomments_set.all()[:8]
        return render(request,'course/course-comment.html',{
            'flag_tag':flag_tag,'course':course,
            'all_comments':all_comments,
        })

class CourseAddCommentView(View):

    def post(self,request):
        context = {}
        context['status'] = 'fail'
        context['msg'] = '用户未登录'
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps(context),content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and len(comments)!=0:
            course = Course.objects.get(id=int(course_id))
            comment = CourseComments()
            comment.course=course
            comment.user = request.user
            comment.comment = comments
            comment.save()
            context['status'] = 'success'
            context['msg'] = '评论成功'
        else:
            context['msg'] = '评论失败'
        return HttpResponse(json.dumps(context),content_type='application/json')