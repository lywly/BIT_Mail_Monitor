import requests
import configparser
# 打包exe
import os
import sys
os.environ['REQUESTS_CA_BUNDLE'] = os.path.join(os.path.dirname(sys.argv[0]), 'cacert.pem')


def push_config(config_filename):
    config_data = configparser.ConfigParser()
    config_data.read(config_filename, encoding='utf-8')

    my_push_url = config_data.get('Sendkey', 'my_push_url')
    push_plus_sendkey = config_data.get('Sendkey', 'push_plus_sendkey')

    return [my_push_url, push_plus_sendkey]


def push(Pushing_Data, Sendkeys):
    # 自建通道
    if Sendkeys[0] != '':
        # 将url改为自建地址
        my_Pushing_Data = Pushing_Data.replace("\n", "%0D%0A")
        url = Sendkeys[0] + my_Pushing_Data
        send_info = requests.get(url)
        if "\"errmsg\":\"ok\"" in str(send_info.content, encoding = "utf-8"):
            print('自建通道已推送')
        else:
            print('自建通道推送超时')
    else:
        pass
        # print('未配置自建通道推送')

    # PushPlus通道"msg":"请求成功"
    if Sendkeys[1] != '':
        url = 'http://www.pushplus.plus/send?token=' + Sendkeys[
            1] + '&title=北理工邮箱推送&content=' + Pushing_Data + '&template=txt'
        send_info = requests.get(url)
        if "\"msg\":\"请求成功\"" in str(send_info.content, encoding="utf-8"):
            print('PushPlus通道已推送')
        else:
            print('PushPlus通道推送超时')
    else:
        pass
