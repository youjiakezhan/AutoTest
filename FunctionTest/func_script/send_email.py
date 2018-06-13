# coding: utf-8
import os
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailSending(object):

    def get_latest_file(self):
        report_path = r'C:\Users\BAIWAN\PycharmProjects\AutoTest\FunctionTest\test_result'
        lists = os.listdir(report_path)  # 列出目录的下所有文件和文件夹保存到lists
        lists.sort(key=lambda x: os.path.getmtime(report_path + "\\" + x))  # 按时间排序
        latest = os.path.join(report_path, lists[-1])  # 获取最新的文件保存到file_new
        return latest

    def create_email(self):
        # 设置smtplib所需的参数
        # 下面的发件人，收件人是用于邮件传输的。
        smtpserver = 'smtp.ym.163.com'
        username = 'wangzhongchang@excelliance.cn'
        password = 'wzc6851498'
        sender = 'wangzhongchang@excelliance.cn'
        receiver = '"许赫"<xuhe@excelliance.cn>,\
                   "王喆"<wangzhe@excean.com>, "齐赵迪"<qizhaodi@excean.com>, "朱瑶"<zhuyao@excean.com>, \
                   "李先状"<lixianzhuang@excelliance.cn>, 771432505@qq.com'

        # 通过Header对象编码的文本，包含utf-8编码信息和Base64编码信息。以下中文名测试ok
        subject = '来自王中昶的测试邮件'
        subject = Header(subject, 'utf-8').encode()

        # 构造邮件对象MIMEMultipart对象
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver

        # 构造文字内容
        text = "Dear All:\n本次Daily Review版本的自动化测试已结束，测试结果请关注测试报告及相关信息已添加到附件"
        text_plain = MIMEText(text, 'plain', 'utf-8')
        msg.attach(text_plain)

        # 构造附件
        with open(r'C:\Users\BAIWAN\PycharmProjects\AutoTest\FunctionTest\test_result.zip', 'rb') as file:
            sendfile = file.read()
        text_att = MIMEText(sendfile, 'base64', 'utf-8')
        text_att["Content-Type"] = 'application/octet-stream'
        # 以下附件可以重命名成aaa.txt
        text_att["Content-Disposition"] = 'attachment; filename="test_report.html"'
        msg.attach(text_att)

        # 发送邮件
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver, 25)
        # 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
        smtp.set_debuglevel(1)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver.split(','), msg.as_string())
        smtp.quit()


# email = EmailSending()
# email.create_email()
