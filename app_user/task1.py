# demo1:task.py and celery.py in one file
# task1.py
from celery import Celery

import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 定义worker（消费者），并指定broker和backend（共享缓冲区）
app1=Celery('task1_app1',broker='redis://127.0.0.1:6379/0',backend='redis://127.0.0.1:6379/0')


# 定义task（生产者）

@app1.task
def add_self_event(username,msg):
    pass

@app1.task
def add_friend_event(username,msg_list):
    pass


@app1.task
def sendEmail(receivers,title,content):
    sender = 'zhangsuosheng9@163.com'
    # receivers = ['zhangsuosheng9@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    mail_host = "smtp.163.com"  # 使用的邮箱的smtp服务器地址，这里是163的smtp地址
    mail_user = "zhangsuosheng9"  # 用户名
    mail_pass = "zhangsuosheng9"

    # 邮件内容，三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(content, 'plain', 'utf-8')

    # 发件人收件人
    message['From'] = "emo" + "<" + mail_user + "@163.com>"
    # message['From'] = Header("emo")
    message['To'] = ";".join(receivers)

    # 邮件标题
    subject = title
    message['Subject'] = Header(subject, 'utf-8')

    try:
        server = smtplib.SMTP()
        server.connect(mail_host)  # 连接服务器
        server.login(mail_user, mail_pass)  # 登录操作
        server.sendmail(sender, receivers, message.as_string())
        server.close()
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件")