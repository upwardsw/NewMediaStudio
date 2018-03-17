#!/usr/bin/python
# -*-coding:UTF-8-*-

import requests
import json


# url:ip/route
# data is a dict
def send_json(url, data):
    headers = {'content-type': 'application/json'}
    return requests.post(url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'), headers=headers)


# # filename是保存文件名包括拓展名（字符串）
# # re是requests反悔的对象
# def save_pics(filename, rq):
#     with open('{}'.format(filename), 'wb') as fd:
#         for chunk in rq.iter_content(chunk_size=1024):
#             fd.write(chunk)
#
#
# def output_json(rq):
#     print(rq.text)


# #添加新用户
# url1 = 'http://127.0.0.1:5000/new_user'
# data1 = dict(student_id=61101162535, name='小白', department='研发中心', zhiwei='部委', password='123456')
# r1 = send_json(url1, data1)
# print(r1)

#登入部分
url1 = 'http://127.0.0.1:5000/login'
data1 = dict(student_id=61101162535, password='123456')
r1 = send_json(url1, data1)
print(r1.text)


# 修改密码部分
# url1 = 'http://127.0.0.1:5000/change_password'
# data1 = dict(student_id=6110116253, name='小白', tel='15797891491', old_password='1234', new_password='12345')
# r1 = send_json(url1, data1)
# output_json(r1)

# # 忘记密码部分
# url1 = 'http://127.0.0.1:5000/forget_password'
# data1 = dict(student_id=6110116253, name='小白', tel='15797891491', new_password='1234')
# r1 = send_json(url1, data1)
# output_json(r1)

#查看测试
url1 = 'http://127.0.0.1:5000/check'
data1 = dict()
r1 = send_json(url1, data1)
print(r1.text)



url = 'http://47.94.138.25/show_request_note_admin'
headers = {'content-type': 'application/json'}

r = requests.post(url,headers=headers)

print(r.text)


