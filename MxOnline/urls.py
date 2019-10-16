# _*_ encoding:utf-8 _*_
"""MxOnline URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from django.views.static import serve
from django.views.decorators.csrf import csrf_exempt

import xadmin
from MxOnline.settings import MEDIA_ROOT

from apps.users.views import LoginView, RegisterView, ActiveView, ForgetView, ResetView, ModifyPwdView, LogoutView, \
    IndexView, SendSmsView

urlpatterns = [
    # url('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^send_sms/', csrf_exempt(SendSmsView.as_view()), name='send_sms'),
    url(r'^active/(?P<active_code>.*)/$', ActiveView.as_view(), name='user_active'),
    url('^forget/$', ForgetView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<reset_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),

    url(r'^org/', include(('apps.organizations.urls', 'org'), namespace='org')),
    url(r'^course/', include(('apps.courses.urls', 'course'), namespace='course')),
    url(r'^organization/', include(('apps.organizations.urls', 'organization'), namespace='organization')),
    url(r'^users/', include(('apps.users.urls', 'users'), namespace='users')),

    # 配置上传文件的访问url
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # url(r'^static/(?P<path>.*)$', serve, {"document_root":STATIC_ROOT}),

    # 机构相关页面
    url(r'^org/', include(('apps.organizations.urls', "organizations"), namespace="org")),

    # 机构相关页面
    url(r'^course/', include(('apps.courses.urls', "courses"), namespace="course")),

    # 用户相关操作
    url(r'^op/', include(('apps.operations.urls', "operations"), namespace="op")),

    # 个人中心
    url(r'^users/', include(('apps.users.urls', "users"), namespace="users")),

    # 配置富文本相关的url
    url(r'^ueditor/', include('DjangoUeditor.urls')),

]

# 全局404配置
# handler404 = 'apps.users.views.page_not_found'
# handler500 = 'apps.users.views.page_error'
