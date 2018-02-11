

from django.shortcuts import render
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import login,authenticate



from users.models import UserProfile
from Mxonline.settings import BASE_DIR


import logging

# Create your views here.


logger = logging.getLogger('defualt')


def user_login(request):
    if request.method=='POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return render(request, 'index.html')
        else:
            return render(request,'login.html')
    elif request.method=='GET':
        return render(request,'login.html')


def user_register(request):
    if request.method=='POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            user = UserProfile.objects.get(username=username)
        except:
            logger.info('%s is not exist' %username)
            user = None
        if user:
            flag=check_password(password,user.password)
            logger.info('flag=%s' % (flag))
            if flag:
                request.session['username']=username
                request.session['passwd'] = password
                return render(request,'index.html',{'username':username,'flag':flag})
            else:
                return render(request, 'register.html', {'username': username,'msg':'账号或密码错误'})
        else:
            return render(request,'login.html')
    elif request.method=='GET':
        return render(request,'login.html')



def user_logout(request):
    request.session.flush()
    return render(request,'index.html')





