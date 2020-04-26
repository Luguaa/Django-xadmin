# coding:utf-8
__author__ = 'Luguaa'
__date__ = '2020/4/13 20:01'

from django.conf.urls import include, url
from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, MyCourseView, \
    MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView


urlpatterns = [
    # 用户信息页
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    # 用户头像上传
    url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),
    # 用户个人中心修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),
    # 发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendmail_code'),
    # 修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),
    # 用户参加的课程
    url(r'^mycourse/$', MyCourseView.as_view(), name='mycourse'),
    # 用户收藏的课程机构
    url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfav_org'),
    # 用户收藏的授课讲师
    url(r'^myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),
    # 用户收藏的课程
    url(r'^myfav/course/$', MyFavCourseView.as_view(), name='myfav_course'),
    # 用户消息
    url(r'^mymessage/$', MyMessageView.as_view(), name='mymessage'),

]