import datetime
import email
from email.header import decode_header, make_header

from Mail_Push_Core.Wechat_push import push
from Mail_Push_Core.mail_login import mail_login

"""
Imap_url：IMAP服务地址
Port：IMAP服务端口
BIT_mail：IMAP模块
User: 邮箱地址
Passwd：密码
Date_range：监测时间范围，单位（天）
Sendkeys：推送设置
"""


def mail_summary(Imap_url, Port, BIT_mail, User, Passwd, Date_range, Sendkeys):
    print('---------------------------------------------------------')
    if BIT_mail.state == 'NONAUTH':
        BIT_mail = mail_login(Imap_url, Port, User, Passwd)
    else:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 邮件汇总任务运行正常')
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

        # All_Data = r'今日共收到邮件' + str(len(data[0].split())) + '封-' + User + '\n'
        All_Data = r'今日共收到邮件' + str(len(data[0].split())) + '封\n' + User + '\n' if int(
            Date_range) == 1 else Date_range + r'日内共收到邮件' + str(
            len(data[0].split())) + '封\n' + User + '\n'
        for msg in msgs[::-1]:
            my_msg = email.message_from_bytes(msg[0][1])

            Subject = str(make_header(decode_header(my_msg['subject'])))
            From = str(make_header(decode_header(my_msg['from'])))
            # To = str(make_header(decode_header(my_msg['to'])))
            # Date = str(make_header(decode_header(my_msg['date'])))

            All_Data = All_Data + '-----------------------------------\n'
            All_Data = All_Data + f"Subject: {Subject}" + "\n"
            All_Data = All_Data + f"From: {From}" + "\n"
            # All_Data = All_Data + f"Date: {Date}" + "\n"
            # All_Data = All_Data + f"Content: {Content}" + "\n"

        push(All_Data, Sendkeys)

    BIT_mail.close()
    print('Mailbox closed.')
    print('*********************************************************')
