

from django.shortcuts import render
from django.contrib.auth import login


from users.models import UserProfile
from Mxonline.settings import BASE_DIR


import logging

# Create your views here.


logger = logging.getLogger(__name__)

def index(request):
    userid = request.session.get('username','')
    passwd = request.session.get('passwd','')
    print(BASE_DIR)
    return render(request,'index.html')



def mx_login(request):

    if request.method=='POST':
        userid = request.POST.get('username', '')
        passwd = request.POST.get('passwd', '')
        try:
            user=UserProfile.objects.get(username=userid)
        except:
            logger.info('user=%s is not exit' %userid)
        if user:
            login(request,user)
        request.session['username']=userid
        request.session['passwd'] = passwd


    elif request.method=='GET':
        return render(request,'login.html')







