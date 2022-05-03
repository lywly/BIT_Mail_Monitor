import datetime
import imaplib
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import warnings
warnings.filterwarnings("ignore")

from Mail_Push_Core.Wechat_push import push_config
from Mail_Push_Core.file_select_GUI import file_select_GUI
from Mail_Push_Core.monitor_config import monitor_config
from Mail_Push_Core.mail_keywds import keywds_monitor
from Mail_Push_Core.mail_summary import mail_summary


def main():
    config_filename = file_select_GUI()
    User, Passwd, Keywords_raw, hour_keywd, minute_keywd, hour_summary, minute_summary, Date_range, Imap_url, Port_raw = monitor_config(
        config_filename)
    Sendkeys = push_config(config_filename)

    Port = int(Port_raw)
    BIT_mail = imaplib.IMAP4(host=Imap_url, port=Port)
    try:
        BIT_mail.login(User, Passwd)
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 登录成功')
    except Exception as e:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' 登录失败')
        print("ErrorType : {}, Error : {}".format(type(e).__name__, e))
    # print(BIT_mail)

    scheduler = BlockingScheduler(timezone="Asia/Shanghai")
    # Cron定时器设置方法参阅：'https://crontab.guru'
    # 添加关键词监测任务
    if Keywords_raw != '':
        trigger_Keywords = CronTrigger(hour=hour_keywd, minute=minute_keywd)
        scheduler.add_job(keywds_monitor, trigger_Keywords, max_instances=5,
                          args=[Imap_url, Port, BIT_mail, User, Passwd, Date_range, Keywords_raw, Sendkeys])
    # 添加邮件汇总推送任务
    trigger_mail_summary = CronTrigger(hour=hour_summary, minute=minute_summary, second='30')
    scheduler.add_job(mail_summary, trigger_mail_summary, max_instances=5,
                      args=[Imap_url, Port, BIT_mail, User, Passwd, Date_range, Sendkeys])
    # 启动任务
    scheduler.start()


if __name__ == '__main__':
    main()
