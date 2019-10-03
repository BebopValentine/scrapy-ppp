import smtplib
from email.mime.text import MIMEText
from email.header import Header


class EmailSend(object):
    def __init__(self):
        self.email_host = 'smtp.163.com'
        self.email_port = 25
        self.email_pass = '123456aa'

    def send_text_email(self, from_addr, to_addrs, subject, content):
        message_text = MIMEText(content, 'plain', 'utf-8')
        message_text['From'] = from_addr
        message_text['To'] = to_addrs
        message_text['Subject'] = subject

        try:
            # 在创建客户端对象的同时，连接到邮箱服务器。
            client = smtplib.SMTP()
            connect = client.connect(self.email_host, self.email_port)
            login_result = client.login(from_addr, self.email_pass)
            print('开始登录', login_result)
            #  (235, b'Authentication successful')
            if login_result and login_result[0] == 235:
                print('登录成功')
                client.sendmail(from_addr, to_addrs, message_text.as_string())
                print('邮件发送成功')
            else:
                print('邮件发送异常：', login_result[0], login_result[1])
        except Exception as e:
            print('连接邮箱服务器异常：', e)
