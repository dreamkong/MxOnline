# # _*_ coding:utf-8 _*_
# from django.conf.urls import url
#
# from apps.users.views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, MyCourseView, \
#     MyFavOrgView, UserMessageView, MyFavCourseView, \
#     MyFavTeacherView
#
# urlpatterns = [
#
#     # 课程机构列表页
#     # url(r'^list/$', OrgListView.as_view(), name='org_list'),
#     # url(r'^add_ask/$', AddUserAskView.as_view(), name='add_ask'),
#     # 用户信息
#     url(r'^info/$', UserInfoView.as_view(), name='user_info'),
#     # 用户头像上传
#     url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),
#     # 个人中心修改密码
#     url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),
#     # 发送邮箱验证码
#     url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'),
#     # 修改邮箱
#     url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),
#     # 我的课程
#     url(r'^mycourse/$', MyCourseView.as_view(), name='my_course'),
#     # 我收藏的课程机构
#     url(r'^myfav/org/$', MyFavOrgView.as_view(), name='myfav_org'),
#     # 我收藏的讲师
#     url(r'myfav/teacher/$', MyFavTeacherView.as_view(), name='myfav_teacher'),
#     # 我收藏的课程
#     url(r'^myfav/course/$', MyFavCourseView.as_view(), name='myfav_course'),
#     # 我的消息
#     url(r'^message/$', UserMessageView.as_view(), name='user_message'),
#
#     # 机构收藏
#     # url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),
#     #
#     # # 讲师列表页
#     # url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher_list'),
#     #
#     # url(r'^teacher/detail/(?P<teacher_id>\d+)$', TeacherDetailView.as_view(), name='teacher_detail'),
# ]
