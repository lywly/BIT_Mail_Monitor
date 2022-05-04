import configparser


def monitor_config(config_filename):
    # 导入config.ini文件信息，若文件配置出错则需手动输入
    # 以下为一些默认值
    Keywords_raw = ''
    hour_keywd = '7-23'
    minute_keywd = '0,30'
    hour_summary = '23'
    minute_summary = '45'
    Date_range = '1'
    Imap_url = 'mail.bit.edu.cn'
    Port_raw = '143'

    try:
        config_data = configparser.ConfigParser()
        config_data.read(config_filename, encoding='utf-8')
        User = config_data.get('Login', 'User')
        Passwd = config_data.get('Login', 'Passwd')
        Keywords_raw = config_data.get('Monitor', 'Keywords')
        hour_keywd = config_data.get('Cron', 'hour_keywd')
        minute_keywd = config_data.get('Cron', 'minute_keywd')
        hour_summary = config_data.get('Cron', 'hour_summary')
        minute_summary = config_data.get('Cron', 'minute_summary')
        Date_range = config_data.get('Date', 'Range')
        Imap_url = config_data.get('Email', 'Imap_url')
        Port_raw = config_data.get('Email', 'Port')
    except:
        User = input("Please input your Email address: ")
        Passwd = input("Please input your Password: ")

    return User, Passwd, Keywords_raw, hour_keywd, minute_keywd, hour_summary, minute_summary, Date_range, Imap_url, Port_raw
