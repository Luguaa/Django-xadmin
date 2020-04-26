# coding:utf-8
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render, render_to_response
from django.views.generic import View
from django.http import HttpResponse
from django.db.models import Q

from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm
from courses.models import Course
from operation.models import UserFavorite


# Create your views here.
class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 城市
        all_cities = CityDict.objects.all()

        # 机构搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # icontains:类似mysql的like语句，i表示不区分大小写
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        # 取出筛选城市
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by('-students')
            elif sort == "courses":
                all_orgs = all_orgs.order_by('-course_nums')

        org_nums = all_orgs.count()

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs, 3, request=request)

        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_cities': all_cities,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'hot_orgs': hot_orgs,
            'sort': sort
        })


class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        # 判断格式是否正确
        if userask_form.is_valid():
            # commit=False：使用户提交的信息不会直接关联到数据库
            user_ask = userask_form.save(commit=True)
            return HttpResponse("{'status': 'success'}", content_type='application/json')
        else:
            return HttpResponse("{'status': 'fail', 'msg':'{0}'},".format(userask_form.errors))


class OrgHomeView(View):
    """
    机构首页
    """
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        # 获取该机构的所有课程与讲师
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        # 用于左侧边框高亮，表示当前是“机构首页”
        current_page = "home"
        # 默认未收藏
        has_fav = False

        if request.user.is_authenticated():
            # 判断用户是否收藏此机构
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-homepage.html', {
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgCourseView(View):
    """
    机构课程列表页
    """
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        current_page = 'course'

        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
        })
    

class OrgDescView(View):
    """
    机构介绍页
    """
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        current_page = 'desc'

        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
        })


class OrgTeacherView(View):
    """
    机构教师页
    """

    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        current_page = 'teacher'

        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
        })


class AddFavView(View):
    """
    用户收藏及取消收藏
    """
    def post(self, request):
        fav_id = request.POST.get('fav_id', '')
        fav_type = request.POST.get('fav_type', '')

        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse("{'status': 'fail', 'msg':'用户未登录'}")

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))

        if exist_records:
            # 记录已经存在，则表示用户取消收藏，并修改收藏数
            exist_records.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0 :
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                if course_org.fav_nums < 0 :
                    course_org.fav_nums = 0
                course_org.save()
            else:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0 :
                    teacher.fav_nums = 0
                teacher.save()

            return HttpResponse("{'status': 'fail', 'msg':'收藏'}", content_type='application/json')

        else:
            user_fav = UserFavorite()

            if fav_id > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                else:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                return HttpResponse("{'status': 'success', 'msg':'已收藏'}", content_type='application/json')
            else:
                return HttpResponse("{'status': 'fail', 'msg':'收藏出错'}", content_type='application/json')


class TeacherListView(View):
    """
    课程讲师列表页
    """
    def get(self, request):
        all_teachers = Teacher.objects.all()
        teacher_nums = all_teachers.count()

        # 教师搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            # icontains:类似mysql的like语句，i表示不区分大小写
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords))

        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "hot":
                all_teachers = all_teachers.order_by('-click_nums')

        # 讲师排行榜
        sorted_teachers = Teacher.objects.all().order_by('-click_nums')

        # 对讲师进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_teachers, 1, request=request)

        teachers = p.page(page)

        return render(request, "teachers-list.html", {
            'all_teachers': teachers,
            'sorted_teachers': sorted_teachers,
            'sort': sort,
            'teacher_nums': teacher_nums,
        })


class TeacherDetailView(View):
    """
    讲师详情页
    """
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        all_courses = Course.objects.filter(teacher=teacher)

        # 判断讲师是否收藏
        has_teacher_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_teacher_faved = True

        # 判断机构是否被收藏
        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_org_faved = True

        # 讲师排行榜
        sorted_teachers = Teacher.objects.all().order_by('-click_nums')

        return render(request, "teacher-detail.html", {
            'teacher': teacher,
            'all_courses': all_courses,
            'sorted_teachers': sorted_teachers,
            'has_org_faved': has_org_faved,
            'has_teacher_faved': has_teacher_faved
        })
