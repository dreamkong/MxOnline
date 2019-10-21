import redis
from django import forms

from captcha.fields import CaptchaField

from MxOnline.settings import REDIS_HOST, REDIS_PORT
from apps.users.models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True, error_messages={'required': '请输入用户名'})
    password = forms.CharField(required=True, min_length=6, error_messages={'required': '请输入密码'})


class DynamicLoginForm(forms.Form):
    mobile = forms.CharField(required=True, max_length=11, min_length=11, error_messages={'required': '请输入手机号'})
    captcha = CaptchaField(label='请输入图片验证码', error_messages={'required': '请输入图片验证码', 'invalid': '图片验证码错误'})


class DynamicLoginPostForm(forms.Form):
    mobile = forms.CharField(required=True, max_length=11, min_length=11, error_messages={'required': '请输入手机号'})
    code = forms.CharField(required=True, max_length=4, min_length=4, error_messages={'required': '请输入短信验证码'})

    def clean_code(self):
        mobile = self.data.get('mobile')
        code = self.data.get('code')

        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db='0', charset='utf8', decode_responses=True)
        if code != r.get(str(mobile)):
            raise forms.ValidationError('短信验证码不正确')
        return self.cleaned_data


class RegisterGetForm(forms.Form):
    captcha = CaptchaField(error_messages={'invalid': '图片验证码错误'})


class RegisterPostForm(forms.Form):
    mobile = forms.CharField(required=True, max_length=11, min_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)
    password = forms.CharField(required=True, min_length=6)

    def clean_mobile(self):
        mobile = self.data.get('mobile')
        # 验证手机是否已经注册
        if UserProfile.objects.filter(mobile=mobile):
            raise forms.ValidationError('手机号码已注册')
        return self.cleaned_data

    def clean_code(self):
        mobile = self.data.get('mobile')
        code = self.data.get('code')

        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db='0', charset='utf8', decode_responses=True)
        if code != r.get(mobile):
            raise forms.ValidationError('短信验证码不正确')
        return self.cleaned_data


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '图片验证码错误'})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birthday', 'address', 'mobile']
