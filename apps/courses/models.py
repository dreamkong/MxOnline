from django.db import models

from apps.users.models import BaseModel
from apps.organizations.models import Teacher
from apps.organizations.models import CourseOrg

DEGREE = (
    ('cj', '初级'),
    ('zj', '中级'),
    ('gj', '高级')
)


class Course(BaseModel):
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name='课程机构', null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='讲师', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name='课程名')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播')
    degree = models.CharField(choices=DEGREE, max_length=2, verbose_name='难度')
    learn_times = models.IntegerField(default=0, verbose_name=' 学习时长(分钟数)')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    category = models.CharField(max_length=20, verbose_name='课程类别', default='后端开发')
    tag = models.CharField(max_length=10, verbose_name='课程标签', default='')

    you_need_know = models.CharField(max_length=300, verbose_name='课程须知', default='')
    teacher_tell = models.CharField(max_length=300, verbose_name='老师告诉你', default='')

    # detail = UEditorField('课程详情', width=600, height=300, imagePath="course/ueditor/",
    #                       filePath="course/ueditor/", default='')
    image = models.ImageField(upload_to='courses/%Y/%m', max_length=120, verbose_name='封面图')

    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_zj_nums(self):
        return self.lesson_set.all().count()

    get_zj_nums.short_description = '章节数'

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href = 'http://www.qinlong.men'>跳转</>")

    go_to.short_description = '跳转'

    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        # 获取课程所有章节
        return self.lesson_set.all()


class BannerCourse(Course):
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        proxy = True


class Lesson(BaseModel):
    # on_delete便是对应的外键数据被删除后，当前数据应该
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='章节名')

    class Meta:
        verbose_name = '课程章节'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_lesson_video(self):
        # 获取章节所有视频
        return self.video_set.all()


class Video(BaseModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='章节')
    name = models.CharField(max_length=100, verbose_name='视频名称')
    url = models.CharField(max_length=200, verbose_name='视频地址', default='')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')

    class Meta:
        verbose_name = '章节视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='资源名称')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name='资源文件', max_length=100)

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
