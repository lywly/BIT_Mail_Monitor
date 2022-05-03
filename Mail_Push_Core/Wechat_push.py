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
    my_push_sendkey = config_data.get('Sendkey', 'my_push_sendkey')
    push_plus_sendkey = config_data.get('Sendkey', 'push_plus_sendkey')

    return [my_push_url, my_push_sendkey, push_plus_sendkey]


def push(Pushing_Data, Sendkeys):
    # 自建通道
    if Sendkeys[1] != '':
        # 将url改为自建地址
        my_Pushing_Data = Pushing_Data.replace("\n", "%0D%0A")
        url = Sendkeys[0] + Sendkeys[1] + '&text=' + my_Pushing_Data
        try:
            send_info = requests.get(url)
            print('自建通道已推送')
        except:
            print('自建通道推送超时')
    else:
        pass
        # print('未配置自建通道推送')

    # PushPlus通道
    if Sendkeys[2] != '':
        url = 'http://www.pushplus.plus/send?token=' + Sendkeys[
            2] + '&title=北理工邮箱推送&content=' + Pushing_Data + '&template=txt'
        try:
            send_info = requests.get(url)
            print('PushPlus通道已推送')
        except:
            print('PushPlus通道推送超时')
    else:
        pass
