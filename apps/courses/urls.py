# coding:utf-8
__author__ = 'Luguaa'
__date__ = '2020/4/11 16:54'

from django.conf.urls import include, url
from .views import CourseListView, CourseDetailView, CourseInfoView, CommentsView, AddCommentsView

urlpatterns = [
    # 课程机构列表页
    url(r'^list/$', CourseListView.as_view(), name='course_list'),

    # 课程详情页
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),

    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),

    # 课程评论
    url(r'^comment/(?P<course_id>\d+)/$', CommentsView.as_view(), name='course_comments'),

    # 添加课程评论
    url(r'^add_comment/$', AddCommentsView.as_view(), name='add_comments'),

]