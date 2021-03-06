

from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import login,authenticate
from django.views.generic import View


from users.models import UserProfile,EmailVerifyRecord,Banner
from Mxonline.settings import BASE_DIR
from .utils import decorate_logging_checker
from .forms import LoginForm,RegisterForm,ForgetPwdForm,ModifyPwdForm,ModifyHeadForm
from utils.email_send import send_email
from utils.login_utils import LoginRequiredMust
from course.models import Course
from organization.models import CourseOrg

import json
import logging

# Create your views here.


logger = logging.getLogger('defualt')


class IndexView(View):

    def get(self,request):
        #首页轮播图
        banners = Banner.objects.all()[:5]
        #课程轮播图
        course_banners = Course.objects.filter(is_banner=True)[:3]
        # 课程轮
        courses = Course.objects.filter(is_banner=False)[:6]
        #机构
        orgs = CourseOrg.objects.all()[:15]
        return render(request,'index.html',{
            "banners":banners,
            "course_banners":course_banners,
            "courses":courses,
            "orgs":orgs,
        })




class LoginView(View):
    def get(self,request):
        login_form = LoginForm()
        return render(request, 'login.html',locals())
    def post(self,request):
        #检测是否已登录
        login_form = LoginForm(request.POST)     #参数接收哦一个字典
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                return render(request, 'login.html', {'msg': '账号没有激活'})
            else:
                return render(request, 'login.html', {'msg': '账号或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form })

class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html',locals())

    def post(self, request):
        register_form = RegisterForm(request.POST)  # 参数接收哦一个字典
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            password = request.POST.get('password', '')
            password = make_password(password)
            user,created = UserProfile.objects.get_or_create(username=user_name,email=user_name)
            if created==False:
                logger.info('%s is  exist' %user_name)
                return render(request,'register.html',{'msg':'用户已存在'})
            else:
                user.password = password
                user.is_active = False
                user.save()
                send_email(user_name, 'register')
                return render(request, 'login.html')
        else:
            return render(request,'register.html',{"register_form":register_form})


class ActiveUserView(View):

    def get(self,request,active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()

        return render(request,'login.html')


class ForgetPwdView(View):

    def get(self,request):
        forgetpwd_form = ForgetPwdForm()
        return render(request,'forgetpwd.html',locals())

    def post(self,request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                send_email(email,'forget')
                return HttpResponse('<h1>邮件已发送，请查收</h1>')
            return render(request,'forgetpwd.html',{ 'forgetpwd_form' : forgetpwd_form ,'msg':'邮箱不存在'})
        else:
            return render(request,'forgetpwd.html',{ 'forgetpwd_form' : forgetpwd_form ,})


class ResetView(View):

    def get(self,request,email,reset_code):
        all_record = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_record:
            return render(request,'password_reset.html',{'email':email})
        else:
            return HttpResponse('邮箱不存在')


class ModifyPwdView(View):

    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            passwd1 = request.POST.get('password1','')
            passwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if passwd1!=passwd2:
                return render(request,'password_reset.html',{ 'msg': '密码不一致','email':email })
            user = UserProfile.objects.get(email=email)
            user.password = make_password(passwd1)
            user.save()
            return render(request,'login.html',{'email': email})
        else:
            return render(request,'password_reset.html',{'modify_form' : modify_form ,})


class UserInfoView(LoginRequiredMust,View):

    def get(self,request):

        return render(request,'users/usercenter-info.html')


class ModifyHeadImageView(LoginRequiredMust,View):

    def post(self,request):
        modify_head = ModifyHeadForm(request.POST,request.FILES,instance=request.user)
        if modify_head.is_valid():
            modify_head.save()
            return HttpResponse(json.dumps({'status':'success'}))
        return HttpResponse(json.dumps({'status':'fail'}))

class UpdatePwdView(View):
    '''
        个人中心，修改密码
    '''
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            passwd1 = request.POST.get('password1', '')
            passwd2 = request.POST.get('password2', '')
            if passwd1 != passwd2:
                return HttpResponse(json.dumps({'msg': '密码不一致', 'email': ''}),content_type='application/json')
            user = request.user
            user.password = make_password(passwd1)
            user.save()
            return HttpResponse(json.dumps({'status':'success'}),content_type='application/json')
        return HttpResponse(json.dumps({'status':'fail'}),content_type='application/json')


#函数式写法
# def user_login(request):
#     if request.method=='POST':
#
#     elif request.method=='GET':
#         return render(request,'login.html')



def user_logout(request):
    request.session.flush()
    return render(request,'index.html')



def page_not_found(request):
    response = render(request,'404.html')
    #response.status_code = '404'
    return response

def page_error(request):
    response = render(request,'500.html')
    return response
