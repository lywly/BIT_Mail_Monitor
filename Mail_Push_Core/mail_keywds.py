import base64
import datetime
import email
import quopri
import re
import time
from email.header import decode_header, make_header
import jieba

from Mail_Push_Core.Pushing import push
from Mail_Push_Core.mail_login import mail_login
from Mail_Push_Core.keywds_cache import kc_load, kc_save
from Mail_Push_Core.myprint import myprint

jieba.setLogLevel(20)
"""
Imap_url：IMAP服务地址
Port：IMAP服务端口
User: 邮箱地址
Passwd：密码
Date_range：监测时间范围，单位（天）
Keywords_raw：关键词，由config文件配置
Sendkeys：推送设置
"""


def encoded_words_to_text(encoded_words):
    encoded_word_regex = r'=\?{1}(.+)\?{1}([B|Q])\?{1}(.+)\?{1}='
    try:
        text = str(make_header(decode_header(encoded_words)))
    except:
        try:
            charset, encoding, encoded_text = re.match(encoded_word_regex, encoded_words).groups()
            if encoding == 'B':
                byte_string = base64.b64decode(encoded_text)
                text = byte_string.decode(charset)
            elif encoding == 'Q':
                byte_string = quopri.decodestring(encoded_text)
                text = byte_string.decode(charset)
        except:
            text = '无主题'
    return text


def keywds_monitor(Imap_url, Port, User, Passwd, Date_range, Keywords_raw, Sendkeys):
    myprint('---------------------------------------------------------')
    myprint(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 关键词监测任务开始运行')
    BIT_mail = mail_login(Imap_url, Port, User, Passwd)

    try:
        BIT_mail.select(mailbox='INBOX', readonly=True)
        myprint('Mailbox selected.')
    except Exception as e:
        myprint(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Select失败')
        myprint("ErrorType : {}, Error : {}".format(type(e).__name__, e))

    date = datetime.date.today().strftime("%d-%b-%Y") if int(Date_range) == 1 else (
            datetime.date.today() - datetime.timedelta(days=int(Date_range))).strftime("%d-%b-%Y")
    _, data = BIT_mail.search(None, '(ALL)', f'(SENTSINCE {date})')

    if data[0] is None:
        myprint('今日未收到邮件') if int(Date_range) == 1 else myprint('%s日内未收到邮件' % Date_range)
        myprint('<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>')
    else:
        myprint('今日已收到%d封邮件 - %s' % (len(data[0].split()), User)) if int(Date_range) == 1 else myprint(
            '%s日内已收到%d封邮件 - %s' % (Date_range, len(data[0].split()), User))
        myprint('<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>')
        msgs = []
        for num in data[0].split():
            typ, mail_data = BIT_mail.fetch(num, '(RFC822)')
            msgs.append(mail_data)

        keywd_flag = 0
        keywds_cache = kc_load()
        All_Data = ''
        All_Keywds = ''
        Email_count = 1
        for msg in msgs:
            my_msg = email.message_from_bytes(msg[0][1])

            Message_ID = my_msg['Message-ID']
            Subject_raw = encoded_words_to_text(my_msg['Subject'])
            Subject = Subject_raw.replace('\r\n', '').replace('\n', '')
            myprint(str(Email_count) + ' -- ' + Subject)
            Email_count += 1

            if Message_ID in keywds_cache:
                continue
            else:
                keywds_cache.append(Message_ID)

                From = str(make_header(decode_header(my_msg['From'])))
                # To = str(make_header(decode_header(my_msg['To'])))
                Date = time.strftime("%Y-%m-%d %H:%M:%S",
                                     time.localtime(email.utils.mktime_tz(email.utils.parsedate_tz(my_msg['Date']))))
                # Date = str(make_header(decode_header(my_msg['date'])))

                Single_Email = f"主题： {Subject}" + "\n" + f"发件人： {From}" + "\n" + f"日期： {Date}"

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
                        Single_Data = Single_Email + '\n******************************\n'
                        All_Data = All_Data + Single_Data
                        All_Keywds = All_Keywds + '/' + keywd.lower()
                        break

        kc_save(keywds_cache)
        myprint('<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>')
        if keywd_flag == 1:
            myprint('已监测到关键词：' + All_Keywds)
            All_Data = f"监测邮箱： {User}" + '\n' + '关键词 - ' + All_Keywds + '\n' + '推送时间：' + datetime.datetime.now().strftime(
                '%Y-%m-%d %H:%M:%S') + '\n------------------------------\n' + All_Data
            push(All_Data, Sendkeys)
        else:
            myprint('未收到关键词相关邮件或已推送，继续自动监测')

    BIT_mail.close()
    myprint('Mailbox closed.')
    BIT_mail.logout()
    myprint('退出登录')
    myprint('*********************************************************')
