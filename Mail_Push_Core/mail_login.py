import datetime
import imaplib


def mail_login(Imap_url, Port, User, Passwd):
    global BIT_mail
    try:
        BIT_mail = imaplib.IMAP4(host=Imap_url, port=Port) if Port == 143 else imaplib.IMAP4_SSL(host=Imap_url,
                                                                                                 port=Port)
        BIT_mail.login(User, Passwd)
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 重登录成功')
    except Exception as e:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 重登录失败')
        print("ErrorType : {}, Error : {}".format(type(e).__name__, e))

    return BIT_mail
