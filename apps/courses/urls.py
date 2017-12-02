# _*_ coding:utf-8 _*_
from django.conf.urls import url, include

from courses.views import CourseListView,CourseDetailView,AddFavView,CourseInfoView,\
    CourseCommentView,AddCommentView,VideoPlayView

urlpatterns = [

    # 课程机构首页
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    # 课程详情页
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),

    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),

    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comment'),

    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),

    url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name='video_play'),

    # # 机构收藏
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),
]
