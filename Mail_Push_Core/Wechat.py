import os
import time
import requests
import json


class WeChat:
    def __init__(self):
        self.CORPID = ""  # 企业ID，在管理后台获取
        self.CORPSECRET = ""  # 自建应用的Secret，每个自建应用里都有单独的secret
        self.agentid = ""
        self.touser = "@all"

    def _get_access_token(self):  # 获取access_token
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,  # 企业ID，
                  'corpsecret': self.CORPSECRET,  # 应用的Secret
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"], data["expires_in"]

    def get_access_token(self):
        cur_time = time.time()  # 获取现在的时间
        if not os.path.isdir('./cache'):
            os.makedirs('./cache')
        try:
            with open('./cache/access_token.conf', 'r') as f:
                t, expires_in, access_token = f.read().split()  # 读取文件中的t即上次获取access token的时间和access token的值
            if 0 < cur_time - float(t) < float(expires_in):  # 判断access token是否在有效期内
                return access_token  # 如果在，则返回读取的access token
            else:  # 否则，先打开文件，权限可以编辑
                with open('./cache/access_token.conf', 'w') as f:
                    access_token, expires_in = self._get_access_token()  # 获取access token
                    f.write('\t'.join([str(cur_time), str(expires_in), access_token]))  # 把获取到的Access token和当前时间写入文件
                    return access_token  # 返回access token的值

        except:  # 如果是第一次运行，则运行此语句，获取access token的值
            with open('./cache/access_token.conf', 'w') as f:
                access_token, expires_in = self._get_access_token()
                cur_time = time.time()
                f.write('\t'.join([str(cur_time), str(expires_in), access_token]))
                return access_token

    def send_text(self, _message):
        access_token = self.get_access_token()
        json_dict = {
            "touser": self.touser,
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {
                "content": _message
            },
            "safe": 0,
            "enable_id_trans": 1,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        json_str = json.dumps(json_dict)
        response_send = requests.post(
            "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}".format(
                access_token=access_token), data=json_str)
        # print("send to " + useridstr + ' ' + json.loads(response_send.text)['errmsg'])
        return json.loads(response_send.text)['errmsg'] == 'ok'
