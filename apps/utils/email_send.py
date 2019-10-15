# _*_ coding:utf-8 _*_
from random import Random

from django.core.mail import send_mail

from apps.users.models import EmailVerifyRecord
from MxOnline.settings import EMAIL_FROM


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    if send_type == 'update_email':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.email = email
    email_record.code = code
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = '慕学在线网注册激活链接'
        email_body = '请点击以下链接激活你的账号:http://127.0.0.1:5212/active/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = '慕学在线网密码重置链接'
        email_body = '请点击以下链接重置你的密码:http://127.0.0.1:5212/reset/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    elif send_type == 'update_email':
        email_title = '慕学在线网邮箱修改验证码'
        email_body = '你的邮箱修改验证码为:{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
