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
from django.conf.urls import url
from django.views.generic import TemplateView

from users.views import UserInfoView,ModifyHeadImageView,UpdatePwdView

urlpatterns = [
    #个人中心
    url(r'^info/$',UserInfoView.as_view(),name='user_info'),

    #修改头像
    url(r'^modify_head/$',ModifyHeadImageView.as_view(),name='modify_head'),

    #修改密码
    url(r'^update_pwd/$',UpdatePwdView.as_view(),name='update_pwd'),

]
