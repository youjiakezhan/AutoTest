# coding: utf-8
import os
import smtplib
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email_content_flag = 1


class SendEmail(object):
    def __init__(self, username, password, state='debug', file_path=None, html_path=None, image_path=None):
        self.file_path = file_path
        self.image_path = image_path
        self.html_path = html_path
        self.username = username
        self.password = password
        self.state = state

    def get_latest_file(self, get_path=None):
        """获取指定目录下按改动时间排序最新文件"""
        # 列出目录下所有文件和文件夹保存到lists
        lists = os.listdir(get_path)
        # 按时间排序
        lists.sort(key=lambda x: os.path.getmtime(get_path + "\\" + x))
        # 获取最新的文件保存到latest
        latest = os.path.join(get_path, lists[-1])
        return latest

    def create_email(self, mail_content):
        """创建并发送邮件，测试报告通过邮件附件的形式发出"""
        username = self.username
        password = self.password
        smtpserver = 'smtp.ym.163.com'
        sender = username
        receiver = ''
        if self.state == 'debug':
            receiver = 'wangzhongchang@excelliance.cn'
        elif self.state == 'send':
            receiver = 'xuhe@excelliance.cn,wangzhe@excean.com,huanggao@excelliance.cn,liminde@excelliance.cn,\
                        zhuyao@excean.com,lixianzhuang@excelliance.cn,wangzhongchang@excelliance.cn,\
                       gezhipeng@excelliance.cn'
        # 通过Header对象编码的文本，包含utf-8编码信息和Base64编码信息。以下中文名测试ok
        subject = '测试报告'
        subject = Header(subject, 'utf-8').encode()

        # 构造邮件对象MIMEMultipart对象
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver

        # 邮件正文内容
        text = MIMEText(mail_content, 'html', 'utf-8')
        msg.attach(text)

        # 邮件正文插入图片
        if self.image_path is not None:
            with open(self.get_latest_file(self.image_path), 'rb') as image_file:
                image = MIMEImage(image_file.read())
            image.add_header('Content-ID', self.image_path)
            msg.attach(image)
            # 将图片添加至邮件正文中
            show_image = """
            <p><img src='cid:%s'></p>
            """ % self.image_path
            img = MIMEText(show_image, 'html', 'utf-8')
            msg.attach(img)

        # 邮件添加附件
        if self.file_path is not None:
            with open(self.get_latest_file(self.file_path), 'rb') as file:
                sendfile = file.read()
            text_att = MIMEText(sendfile, 'base64', 'utf-8')
            text_att["Content-Type"] = 'application/octet-stream'
            # 以下附件可以重命名成aaa.txt
            text_att["Content-Disposition"] = 'attachment; filename="test_report.zip"'
            msg.attach(text_att)

        # 发送邮件
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver, 25)
        # 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
        # smtp.set_debuglevel(1)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver.split(','), msg.as_string())
        smtp.quit()
