import datetime
import imaplib

from Mail_Push_Core.myprint import myprint


def mail_login(Imap_url, Port, User, Passwd):
    global BIT_mail
    try:
        BIT_mail = imaplib.IMAP4(host=Imap_url, port=Port) if Port == 143 else imaplib.IMAP4_SSL(host=Imap_url,
                                                                                                 port=Port)
        BIT_mail.login(User, Passwd)
        myprint(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 重登录成功')
    except Exception as e:
        myprint(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 重登录失败')
        myprint("ErrorType : {}, Error : {}".format(type(e).__name__, e))

    return BIT_mail
