
from datetime import datetime

from django.db import models


from users.models import UserProfile
from course.models import Course
# Create your models here.


"""
    UserAsk             -   用户咨询
    CourseComments      -   用户评论
    UserFavortie        -   用户收藏
    UserMessage         -   用户消息
    UserCourse          -   用户学习的课程
"""

FAV_TYPE=(
    ('1','课程'),
    ('2','讲师'),
    ('3','机构'),
)


class UserAsk(models.Model):

    name = models.CharField(max_length=30,verbose_name='姓名')
    moblie = models.CharField(max_length=11,verbose_name='手机号码')
    course_name = models.CharField(max_length=20,verbose_name='课程名')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='添加时间')

    class Meta:
        verbose_name='用户咨询'
        verbose_name_plural=verbose_name


class CourseComments(models.Model):
    '''
        课程评论
    '''
    user = models.ForeignKey(UserProfile,verbose_name='用户')
    course = models.ForeignKey(Course,verbose_name='课程')
    comment = models.CharField(max_length=200,verbose_name='评论')
    add_time = models.DateTimeField(default=datetime.now,verbose_name='评论时间')

    class Meta:
        verbose_name='课程评论'
        verbose_name_plural=verbose_name


class UserFavortie(models.Model):
    '''
        用户收藏
    '''
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    fav_id = models.IntegerField(default=0,verbose_name='数据ID')
    fav_type = models.IntegerField(default=1,verbose_name='收藏类型',choices=FAV_TYPE)

    class Meta:
        verbose_name='用户收藏'
        verbose_name_plural=verbose_name

