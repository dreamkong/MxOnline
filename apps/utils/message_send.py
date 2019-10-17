import requests

from MxOnline.settings import yp_apikey


def send_message_code(api_key, code, mobile):
    headers = {
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        "Accept": "application/json;charset=utf-8"
    }
    url = "https://sms.yunpian.com/v2/sms/single_send.json"
    text = "【慕学生鲜】您的验证码是{}".format(code)
    data = {
        'apikey': api_key,
        'text': text,
        'mobile': mobile
    }
    # response = requests.post(url, headers=headers, data=data).json()
    response = {'code': 0}
    return response


if __name__ == '__main__':
    response = send_message_code(yp_apikey, 666666, 18812345678)
    code = response['code']
    msg = response['msg']
    if code == 0:
        print('发送成功')
    else:
        print('发送失败：{}'.format(msg))
    print(response)
