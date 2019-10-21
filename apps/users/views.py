import json

import redis
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.hashers import make_password

from MxOnline.settings import yp_apikey
from apps.courses.models import Course
from apps.operations.models import UserCourse, UserFavorite, UserMessage, Banner
from apps.organizations.models import CourseOrg, Teacher
from apps.users.forms import LoginForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm, \
    DynamicLoginForm, DynamicLoginPostForm, RegisterPostForm, RegisterGetForm
from apps.users.models import EmailVerifyRecord
from apps.utils.email_send import send_register_email
from apps.utils.message_send import send_message_code
from apps.utils.mixin_utils import LoginRequiredMixin
from apps.users.models import UserProfile
from apps.utils import random_str


class CustomAuth(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ResetView(View):
    def get(self, request, reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        email = request.POST.get('email', '')
        if modify_form.is_valid():
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            if password1 != password2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '密码不一致!'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(password1)
            user.save()
            return render(request, 'login.html')
        else:
            return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})


class ActiveView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))

        register_get_form = RegisterGetForm()
        return render(request, 'register.html', {'register_get_form': register_get_form})

    def post(self, request):
        register_post_form = RegisterPostForm(request.POST)
        if register_post_form.is_valid():
            user_name = request.POST.get('mobile', '')
            password = request.POST.get('password', '')
            user = UserProfile()
            user.username = user_name
            user.mobile = user_name
            user.set_password(password)
            user.save()

            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user
            user_message.message = '欢迎注册！！！！！'
            user_message.save()

            # send_register_email(user_name, 'register')
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            register_get_form = RegisterGetForm()
            return render(request, 'register.html',
                          {'register_get_form': register_get_form, 'register_post_form': register_post_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))

        dynamic_login_form = DynamicLoginForm()
        return render(request, 'login.html', {'dynamic_login_form': dynamic_login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=user_name, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户未激活!', 'login_form': login_form})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误!', 'login_form': login_form})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class DynamicLoginView(View):
    def post(self, request):
        dynamic_login_flag = True
        login_form = DynamicLoginPostForm(request.POST)
        if login_form.is_valid():
            mobile = login_form.cleaned_data.get('mobile')
            existed_users = UserProfile.objects.filter(mobile=mobile)
            if existed_users:
                user = existed_users[0]
            else:
                # 未查到注册信息
                user = UserProfile(username=mobile)
                user.set_password(random_str.generate_random(10, 2))
                user.mobile = mobile
                user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            d_form = DynamicLoginForm()
            return render(request, 'login.html',
                          {'login_form': login_form, 'dynamic_login_flag': dynamic_login_flag, 'd_form': d_form})


class SendSmsView(View):
    def post(self, request):
        send_sms_form = DynamicLoginForm(request.POST)
        res_dict = {}
        if send_sms_form.is_valid():
            print('验证成功')
            mobile = send_sms_form.cleaned_data.get('mobile')
            # 随机生成数字验证码
            code = random_str.generate_random(4, 0)
            response = send_message_code(yp_apikey, code, mobile)
            if response.get('code') == 0:
                res_dict['status'] = 'success'
                r = redis.Redis(host='localhost', port=6379, db=0, charset='utf8', decode_responses=True)
                r.set(str(mobile), code)
                # 设置验证码5分钟过期
                r.expire(str(mobile), 60 * 5)
            else:
                res_dict['msg'] = response.get('msg')
        else:
            print('验证失败')
            for key, value in send_sms_form.errors.items():
                res_dict[key] = value[0]
        return JsonResponse(res_dict)


class ForgetView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email')
            send_register_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


# def user_login(request):
#     if request.method == 'POST':
#         user_name = request.POST.get('username', '')
#         pass_word = request.POST.get('password', '')
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:
#             login(request, user)
#             return render(request, 'index.html')
#         else:
#             return render(request, 'login.html', {'msg': '用户名或密码错误!'})
#
#     elif request.method == 'GET':
#         return render(request, 'login.html', {})


class UserInfoView(LoginRequiredMixin, View):
    '''
    用户个人信息
    '''

    def get(self, request):
        return render(request, 'usercenter-info.html', {})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    '''
    用户修改头像
    '''

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            # image = image_form.cleaned_data['image']
            # request.user.image = image
            # request.user.save()
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(LoginRequiredMixin, View):
    '''
    个人中心修改密码
    '''

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            if password1 != password2:
                return HttpResponse('{"status":"","msg":"密码不一致!"}', content_type='application/json')
            user = request.user
            user.password = make_password(password1)
            user.save()
            return HttpResponse('{"status":"success","msg":"修改成功!"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    '''
    发送邮箱验证码
    '''

    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在!"}', content_type='application/json')
        send_register_email(email, 'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code)
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":" 验证码错误!"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    '''
    我的课程
    '''

    def get(self, request):
        current_page = 'course'
        my_courses = UserCourse.objects.filter(user=request.user)

        return render(request, 'usercenter-mycourse.html', {
            'current_page': current_page,
            'my_courses': my_courses,
        })


class MyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'fav'
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)

        return render(request, 'usercenter-fav-org.html', {
            'current_page': current_page,
            'org_list': org_list,
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'fav'
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)

        return render(request, 'usercenter-fav-teacher.html', {
            'current_page': current_page,
            'teacher_list': teacher_list,
        })


class MyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = 'fav'
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)

        return render(request, 'usercenter-fav-course.html', {
            'current_page': current_page,
            'course_list': course_list,
        })


class UserMessageView(LoginRequiredMixin, View):
    '''
    我的消息
    '''

    def get(self, request):
        current_page = 'message'

        all_messages = UserMessage.objects.filter(user=request.user.id)
        all_unread_message = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_message:
            unread_message.has_read = True
            unread_message.save()

        # 对消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, 5, request=request)
        messages = p.page(page)

        return render(request, 'usercenter-message.html', {
            'current_page': current_page,
            'all_messages': messages,
        })


class IndexView(View):
    def get(self, request):
        # 取出轮播图
        # print(1 / 0)
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]

        return render(request, 'index.html', {
            'all_banners': all_banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'course_orgs': course_orgs,
        })


class LoginUnsafeView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户未激活!'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误!'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


def page_not_found(request):
    # 全局404配置
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    # 全局500配置
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
