# 北京理工大学邮箱推送服务

### 功能
1. 可添加`关键词`进行`监测`，发现相关邮件将`推送`到设定平台
2. 可将邮箱信息定时`汇总`推送到设定平台
2. 目前支持`自建推送平台`设置、PushPlus[^1]推送设置
3. 关键词监测`时间间隔`与信息汇总`推送时间`均可`自定义`
4. 监测时间范围自定义：`今日`、`7日内`等

### How to use

- 基于`Python=3.9`，相关依赖列于[requirements.txt](./requirements.txt)
- 配置文件模板[`config_template.ini`](./config_template.ini)中对各项参数作了详细备注，请仔细阅读
- 必填项为 `User` `Passwd`
- 如需添加关键词自动监测，需填写 `Keywords`项，程序将在Terminal中显示运行结果
- 如需将监控结果与邮件汇总推送到微信，需填写 `push_plus_sendkey` 项，或自建推送通道
- 修改后的配置文件重命名为`config.ini`，与主程序放置于同目录，否则将启动GUI进行手动选择配置文件
- 其余参数不再赘述

### ToDo
1. 添加`企业微信`推送通道
2. `GUI`界面（有谁能`PR`一下吗？写不动了...）
3. ...

程序使用Pyinstaller打包，有一些坑，参考[^2] [^3] [^4]解决

`pyinstaller -F -i favicon.ico BIT_Mail.py`

`pyinstaller test.spec`

[^1]:http://www.pushplus.plus/
[^2]:https://blog.csdn.net/gt5201314haa/article/details/121359646
[^3]:https://www.jianshu.com/p/cc42591dcca9
[^4]:https://blog.csdn.net/whatday/article/details/109138454