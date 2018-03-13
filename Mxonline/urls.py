"""Mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve

from users.views import LoginView,user_logout,RegisterView,ActiveUserView,ForgetPwdView,ResetView,ModifyPwdView,\
    page_not_found
from Mxonline.settings import MEDIA_ROOT


import xadmin

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^captcha/', include('captcha.urls')),  # 这是生成验证码的图片
    url(r'^ueditor/', include('DjangoUeditor.urls')),   #uediter 富文本 url

    url(r'^$',TemplateView.as_view(template_name='index.html')),
    url(r'^login/$',LoginView.as_view(),name='login'),
    url(r'^register/$',RegisterView.as_view(),name='register'),
    url(r'^logout/$',user_logout,name='logout'),
    url(r'^active/(?P<active_code>.*)/$',ActiveUserView.as_view(),name='active'),
    url(r'^forgetpwd/$',ForgetPwdView.as_view(),name='forgetpwd'),
    url(r'^reset/(?P<email>.*)/(?P<reset_code>.*)/$',ResetView.as_view(),name='reset'),
    url(r'^modifypwd/$',ModifyPwdView.as_view(),name='modifypwd'),

    url(r'^org/',include('organization.urls',namespace='org')),

    #配置上传文件的访问处理函数
    url(r'media/(?P<path>).*',serve,{'document_root':MEDIA_ROOT}),

    #uers文件
    url(r'^users/',include('users.urls')),

    url(r'^course/',include('course.urls',namespace='course')),
]

#全局404页面配置
handler404 = page_not_found
handler500 = 'users.views.page_error'
