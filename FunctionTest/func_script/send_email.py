# coding: utf-8
import os
import smtplib
import time
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from bs4 import BeautifulSoup
from selenium import webdriver

from FunctionTest.func_script.func_lib import BASE_PATH


class EmailSending(object):
    def __init__(self, username, password, file_path=None, html_path=None, image_path=None):
        self.file_path = file_path
        self.image_path = image_path
        self.html_path = html_path
        self.username = username
        self.password = password

    def get_latest_file(self, get_path=None):
        """获取指定目录下按改动时间排序最新文件"""
        # 列出目录下所有文件和文件夹保存到lists
        lists = os.listdir(get_path)
        # 按时间排序
        lists.sort(key=lambda x: os.path.getmtime(get_path + "\\" + x))
        # 获取最新的文件保存到latest
        latest = os.path.join(get_path, lists[-1])
        return latest

    def find_content(self):
        # 从html文件里提取测试报告执行结果
        list = []
        with open(self.get_latest_file(self.image_path),
                  'rb') as fp:
            soup = BeautifulSoup(fp, 'html.parser')
        data = soup.find_all('tr')[1].find_all('td')[1:5]
        for i in data:
            list.append(i.text)
        return list

    def screen_shot(self):
        # 使用selenium的webdriver协议通过chrome驱动打开网页进行截图
        driver = webdriver.Chrome()
        url = self.get_latest_file(self.html_path)
        driver.get(url)
        time.sleep(1)
        driver.save_screenshot(self.image_path + '\\%s.png' % time.strftime('%Y%m%d%H%M%S'))
        driver.quit()

    def create_email(self):
        """创建并发送邮件，测试报告通过邮件附件的形式发出"""
        username = self.username
        password = self.password
        smtpserver = 'smtp.ym.163.com'
        sender = username
        # receiver = 'xuhe@excelliance.cn,wangzhe@excean.com,qizhaodi@excean.com,zhuyao@excean.com, \
        #            lixianzhuang@excelliance.cn,771432505@qq.com'

        receiver = '771432505@qq.com'
        # 通过Header对象编码的文本，包含utf-8编码信息和Base64编码信息。以下中文名测试ok
        subject = '双开助手DailyReview测试报告'
        subject = Header(subject, 'utf-8').encode()

        # 构造邮件对象MIMEMultipart对象
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver

        # 插入图片
        with open(self.get_latest_file(self.image_path), 'rb') as sendimagefile:
            image = MIMEImage(sendimagefile.read())
        image.add_header('Content-ID', self.image_path)
        msg.attach(image)

        # 构造文字内容
        mail_img = """
        <p><img src='cid:%s'></p>
        """ % self.image_path
        text = MIMEText(mail_img, 'html', 'utf-8')
        msg.attach(text)

        # 构造附件
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


# email = EmailSending(username=input('邮箱：'), password=input('密码：'),
#                      file_path=r'Z:\daily_review_SKZS\daily_review_files\result',
#                      html_path=BASE_PATH + '\\test_result\\report',
#                      image_path=BASE_PATH + '\\test_result\\screenshot')
# email.screen_shot()
# email.create_email()
