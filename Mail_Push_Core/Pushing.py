import requests
import json
import configparser

from Mail_Push_Core.Wechat import WeChat
from Mail_Push_Core.myprint import myprint
# 打包exe
import os
import sys

os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')


def push_config(config_filename):
    config_data = configparser.ConfigParser()
    config_data.read(config_filename, encoding='utf-8')

    my_push_url = config_data.get('Sendkey', 'my_push_url')
    push_plus_sendkey = config_data.get('Sendkey', 'push_plus_sendkey')
    CORPID = config_data.get('Sendkey', 'QYWX_CORPID')
    CORPSECRET = config_data.get('Sendkey', 'QYWX_CORPSECRET')
    agentid = config_data.get('Sendkey', 'QYWX_agentid')

    return [my_push_url, push_plus_sendkey, [CORPID, CORPSECRET, agentid]]


def push(Pushing_Data, Sendkeys):
    # 自建通道
    if Sendkeys[0] != '':
        # 将url改为自建地址
        my_Pushing_Data = Pushing_Data.replace("\n", "%0D%0A")
        my_url = Sendkeys[0] + my_Pushing_Data
        my_send_info = requests.get(my_url)
        if "\"errmsg\":\"ok\"" in str(my_send_info.content, encoding="utf-8"):
            myprint('自建通道已推送')
        else:
            myprint('自建通道推送超时')
    else:
        pass
        # myprint('未配置自建通道推送')

    # PushPlus通道"msg":"请求成功"
    if Sendkeys[1] != '':
        pushplus_token = Sendkeys[1]
        pushplus_title = '北理工邮箱推送'
        pushplus_template = 'html'
        pushplus_url = 'http://www.pushplus.plus/send'
        pushplus_data = {
            "token": pushplus_token,
            "title": pushplus_title,
            "content": Pushing_Data,
            "template": pushplus_template
        }
        pushplus_body = json.dumps(pushplus_data).encode(encoding='utf-8')
        pushplus_headers = {'Content-Type': 'application/json'}
        pushplus_send_info = requests.post(pushplus_url, data=pushplus_body, headers=pushplus_headers)

        if "\"msg\":\"请求成功\"" in str(pushplus_send_info.content, encoding="utf-8"):
            myprint('PushPlus通道已推送')
        else:
            myprint('PushPlus通道推送超时')
    else:
        pass

    if Sendkeys[2][0] != '':
        qywx = WeChat()
        qywx.CORPID = Sendkeys[2][0]
        qywx.CORPSECRET = Sendkeys[2][1]
        qywx.agentid = Sendkeys[2][2]
        qywx_send_info = qywx.send_text(Pushing_Data)
        if qywx_send_info:
            myprint('企业微信通道已推送')
        else:
            myprint('企业微信通道推送超时')
    else:
        pass
