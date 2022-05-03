import datetime
import email
from email.header import decode_header, make_header
import jieba

from Mail_Push_Core.Wechat_push import push
from Mail_Push_Core.mail_login import mail_login

jieba.setLogLevel(20)
"""
Imap_url：IMAP服务地址
Port：IMAP服务端口
BIT_mail：IMAP模块
User: 邮箱地址
Passwd：密码
Date_range：监测时间范围，单位（天）
Keywords_raw：关键词，由config文件配置
Sendkeys：推送设置
"""


def keywds_monitor(Imap_url, Port, BIT_mail, User, Passwd, Date_range, Keywords_raw, Sendkeys):
    print('---------------------------------------------------------')
    if BIT_mail.state == 'NONAUTH':
        BIT_mail = mail_login(Imap_url, Port, User, Passwd)
    else:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 关键词监测任务运行正常')
        pass

    BIT_mail.select(mailbox='INBOX', readonly=True)
    print('Mailbox selected.')

    date = datetime.date.today().strftime("%d-%b-%Y") if int(Date_range) == 1 else (
            datetime.date.today() - datetime.timedelta(days=int(Date_range))).strftime("%d-%b-%Y")
    _, data = BIT_mail.search(None, '(ALL)', f'(SENTSINCE {date})')

    if data[0] is None:
        print('今日未收到邮件') if int(Date_range) == 1 else print('%s日内未收到邮件' % Date_range)
    else:
        print('今日已收到%d封邮件 - %s' % (len(data[0].split()), User)) if int(Date_range) == 1 else print(
            '%s日内已收到%d封邮件 - %s' % (Date_range, len(data[0].split()), User))
        msgs = []
        for num in data[0].split():
            typ, mail_data = BIT_mail.fetch(num, '(RFC822)')
            msgs.append(mail_data)

        keywd_flag = 0
        for msg in msgs[::-1]:
            my_msg = email.message_from_bytes(msg[0][1])

            Subject = str(make_header(decode_header(my_msg['subject'])))
            From = str(make_header(decode_header(my_msg['from'])))
            To = str(make_header(decode_header(my_msg['to'])))
            Date = str(make_header(decode_header(my_msg['date'])))

            Single_Email = f"主题： {Subject}" + "\n" + f"发件人： {From}" + "\n" + f"收件人： {To}" + "\n" + f"日期： {Date}" + "\n"

            words = jieba.lcut(Single_Email.lower(), cut_all=True)
            Keywords = jieba.lcut(Keywords_raw.lower(), cut_all=False)
            # 去除英文逗号
            while True:
                try:
                    Keywords.remove(',')
                except:
                    break


            for keywd in Keywords:
                if keywd.lower() in words:
                    keywd_flag = 1
                    Single_Data = r'邮件监测 - 关键词：' + keywd.lower() + r'%0D%0A推送时间：' + datetime.datetime.now().strftime(
                        '%Y-%m-%d %H:%M:%S') + '\n-----------------------------------\n' + Single_Email

                    print('已监测到关键词：' + keywd.lower())
                    push(Single_Data, Sendkeys)

        if keywd_flag == 0:
            print('未收到关键词相关邮件，30分钟后自动监测')

    BIT_mail.close()
    print('Mailbox closed.')
    print('*********************************************************')
