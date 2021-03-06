import datetime
import email
import time
from email.header import decode_header, make_header

from Mail_Push_Core.Pushing import push
from Mail_Push_Core.mail_keywds import encoded_words_to_text
from Mail_Push_Core.mail_login import mail_login
from Mail_Push_Core.myprint import myprint

"""
Imap_url：IMAP服务地址
Port：IMAP服务端口
User: 邮箱地址
Passwd：密码
Date_range：监测时间范围，单位（天）
Sendkeys：推送设置
"""


def mail_summary(Imap_url, Port, User, Passwd, Date_range, Sendkeys):
    myprint('---------------------------------------------------------')
    myprint(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 邮件汇总任务开始运行')
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

        All_Data = r'今日共收到邮件' + str(len(data[0].split())) + '封\n' + User + '\n' if int(
            Date_range) == 1 else Date_range + r'日内共收到邮件' + str(
            len(data[0].split())) + '封\n' + User + '\n'
        for msg in msgs:
            my_msg = email.message_from_bytes(msg[0][1])

            Subject_raw = encoded_words_to_text(my_msg['Subject'])
            Subject = Subject_raw.replace('\r\n', '').replace('\n', '')
            From = str(make_header(decode_header(my_msg['From'])))
            # To = str(make_header(decode_header(my_msg['To'])))
            Date = time.strftime("%Y-%m-%d %H:%M:%S",
                                 time.localtime(email.utils.mktime_tz(email.utils.parsedate_tz(my_msg['Date']))))

            All_Data = All_Data + '-----------------------------------\n'
            All_Data = All_Data + f"主题： {Subject}" + "\n"
            All_Data = All_Data + f"发件人： {From}" + "\n"
            All_Data = All_Data + f"Date: {Date}" + "\n"

        push(All_Data, Sendkeys)

    myprint('<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>')
    BIT_mail.close()
    myprint('Mailbox closed.')
    BIT_mail.logout()
    myprint('退出登录')
    myprint('*********************************************************')
