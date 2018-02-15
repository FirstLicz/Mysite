

from django.shortcuts import render
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import login,authenticate
from django.views.generic import View


from users.models import UserProfile
from Mxonline.settings import BASE_DIR
from .utils import decorate_logging_checker
from .forms import LoginForm,RegisterForm


import logging

# Create your views here.


logger = logging.getLogger('defualt')


class LoginView(View):
    def get(self,request):
        return render(request, 'login.html')
    def post(self,request):
        #检测是否已登录
        login_form = LoginForm(request.POST)     #参数接收哦一个字典
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active != 1:
                    return render(request, 'login.html', {'msg': '账号没有激活'})
                login(request, user)
                return render(request, 'index.html')
            else:
                return render(request, 'login.html', {'msg': '账号或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form })

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        register_form = RegisterForm(request.POST)  # 参数接收哦一个字典
        if register_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            password = make_password(password)
            user ,created = UserProfile.objects.get_or_create(username=username,email=username,password=password)
            if created==False:
                logger.info('%s is  exist' %username)
                return render(request,'register.html',{'msg':'用户已存在'})
            else:
                return render(request, 'register.html', {'username': username,'msg':'账号或密码错误'})
        else:
            return render(request,'register.html',{"register_form":register_form})


#函数式写法
# def user_login(request):
#     if request.method=='POST':
#
#     elif request.method=='GET':
#         return render(request,'login.html')



def user_logout(request):
    request.session.flush()
    return render(request,'index.html')





