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
from django.views.generic import TemplateView
from django.views.static import serve

# import xadmin
import xadmin
from MxOnline.settings import MEDIA_ROOT

# from users.views import LoginView, RegisterView, ActiveView, ForgetView, ResetView, ModifyPwdView, LogoutView, IndexView

urlpatterns = [
    # url('admin/', admin.site.urls),
    url('xadmin/', xadmin.site.urls),
    # url('^$', IndexView.as_view(), name='index'),
    # url('^login/$', LoginView.as_view(), name='login'),
    # url('^logout/$', LogoutView.as_view(), name='logout'),
    # url('^register/$', RegisterView.as_view(), name='register'),
    # url(r'^captcha/', include('captcha.urls')),
    # url(r'^active/(?P<active_code>.*)/$', ActiveView.as_view(), name='user_active'),
    # url('^forget/$', ForgetView.as_view(), name='forget_pwd'),
    # url(r'^reset/(?P<reset_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    # url(r'^modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),
    #
    # url(r'^org/', include('organizations.urls', namespace='org')),
    # url(r'^course/', include('courses.urls', namespace='course')),
    # # url(r'^teacher/', include('organizations.urls',namespace='teacher')),
    # url(r'^users/', include('users.urls', namespace='users')),
    #
    # # 配置上传文件的访问处理函数
    # url(r'^media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),
    #
    # # url(r'^static/(?P<path>.*)', serve, {'document_root': STATIC_ROOT}),
    #
    # # 富文本相关
    # url(r'ueditor/',include('DjangoUeditor.urls'))

]

# 全局404配置
# handler404 = 'users.views.page_not_found'
# handler500 = 'users.views.page_error'
