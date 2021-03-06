# coding:utf-8
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

from .models import Course, CourseResource
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin


# Create your views here.
class CourseListView(View):
    """
    课程列表
    """
    def get(self, request):

        all_courses = Course.objects.all().order_by("-add_time")
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        # 关键词搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # icontains:类似mysql的like语句，i表示不区分大小写
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) |
                                             Q(detail__icontains=search_keywords))

        # 课程排序
        # 获取排序类型
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by('-students')
            elif sort == "hot":
                all_courses = all_courses.order_by('-click_nums')

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        # 每页显示六个课程
        p = Paginator(all_courses, 6, request=request)

        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            'hot_courses': hot_courses
        })


class CourseDetailView(View):
    """
    课程详情页
    """

    def get(self, request, course_id):
        # 获取课程id
        course = Course.objects.get(id=int(course_id))

        # 增加课程点击数
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False

        # 用户认证
        if request.user.is_authenticated():
            # 收藏课程
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True

            # 收藏机构
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        # 相关课程推荐
        tag = course.tag
        if tag:
            # 获取相同tag的课程
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []

        return render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org
        })


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()
        # 查询用户是否已经关联该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        # 如果不存在，添加存在关系
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        # 获取学习该课程的所有用户id
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        # 获取用户学的所有课程id
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 获取该用户学过的其他课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        # 获取下载资源
        all_resource = CourseResource.objects.filter(course=course)

        return render(request, 'course-video.html', {
            'course': course,
            'course_resources': all_resource,
            'relate_courses': relate_courses
        })


class CommentsView(LoginRequiredMixin, View):
    """
    展示课程评论
    """
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resource = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()

        return render(request, 'course-comment.html', {
            'course': course,
            'course_resources': all_resource,
            'all_comments': all_comments
        })


class AddCommentsView(View):
    """
    添加用户评论
    """
    def post(self, request):

        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse("{'status': 'fail', 'msg':'用户未登录'}", content_type='application/json')

        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")

        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()

            return HttpResponse("{'status': 'success', 'msg':'评论成功'}", content_type='application/json')

        else:
            return HttpResponse("{'status': 'fail', 'msg':'评论失败'}", content_type='application/json')
