import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import matplotlib.pyplot as plt

from FunctionTest.func_script.appium_server_check import AppiumServerCheck
from FunctionTest.func_script.check_and_install_apk import FilePath
from FunctionTest.func_script.func_lib import *

"""
    脚本功能:
            检测指定目录下是否有apk文件,有的话自动执行安装过程(自动安装仅限oppoR7),如果没有则继续等待直到apk文件出现;
            安装后调出广告和信息流,然后执行back,home,冷启动的时间测试;
            首轮测试结束后卸载apk,安装比对版本的apk进行第二轮测试;
            测试完毕后收集测试数据输出图形报告;
            测试报告邮件发送;
    测试环境:
            测试前请确保手机内已安装有双开助手apk(版本不限,仅为开启appium-server使用);
            测试前请确保手机内至少装有一款热门应用(如微信等);
"""
# 指定默认字体
plt.rcParams['font.sans-serif'] = ['KaiTi']
# 解决保存图像是负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False
email_content_flag = 1


class StartTimeTest(FindElement, UserOperation, Waiting, AppOperation):
    """app启动时间测试类"""

    def __init__(self):
        self.list_back_test = []
        self.list_home_test = []
        self.list_force_test = []
        self.list_back_std = []
        self.list_home_std = []
        self.list_force_std = []

    # 启动并获取启动时间
    def start_and_get_date(self):
        app_start_time = ''
        date = os.popen('adb shell am start -W ' + pck_name + '/' + activity).readlines()
        for i in date:
            if 'TotalTime' in i:
                app_start_time = i.split(':')[1].strip()
                # print(app_start_time)
        return int(app_start_time)

    # 设置手机（oppoR7）系统时间
    def set_status(self):
        self.back()
        self.wait_for()
        self.home()
        self.wait_for()
        self.find_element('//*[@text="设置"]').click()
        # self.wait_for()
        try:
            self.swipe_find_element('//*[@text="日期和时间"]')
        except Exception:
            self.swipe_find_element('//*[@text="日期和时间"]')
        # self.wait_for()
        if self.find_element('//*[@text="设置日期"]').is_enabled() is True:
            pass
        else:
            self.find_elements('android:id/checkbox')[0].click()
        # self.wait_for(1)
        self.find_element('//*[@text="设置日期"]').click()
        # self.wait_for(1)
        self.find_elements('oppo:id/increment')[1].click()
        # self.wait_for(1)
        self.find_element('android:id/button1').click()
        # self.wait_for(1)
        self.home()
        self.wait_for()
        self.start_app()
        self.wait_explicit_ele('com.excelliance.dualaid:id/add_but')

    def set_until_find_ad(self):
        """设置测试环境（拉取广告及信息流）"""
        self.start_app()
        self.wait_for()
        try:
            self.set_app_status3()
            if self.find_element('com.excelliance.dualaid:id/iv_close').is_displayed():
                self.find_element('com.excelliance.dualaid:id/iv_close').click()
        except selenium.common.exceptions.NoSuchElementException:
            print('未拉取到广告')
        except selenium.common.exceptions.TimeoutException:
            print('未拉取到广告')
        # 调出信息流
        self.set_status()
        i = 1
        while i <= 5:
            print('第%s次拉取信息流' % i)
            i += 1
            if '双开资讯' or 'com.excelliance.dualaid:id/tv_news' in getinfo.get_xml():
                self.back()
                self.wait_for()
                break
            else:
                print('拉取信息流失败')
                self.set_status()
        if i == 5:
            global email_content_flag
            email_content_flag = 0
            em = EmailSending('wangzhongchang@excelliance.cn', 'wzc6851498')
            em.create_email()

    def test_back(self):
        """back场景测试"""
        list_back = []
        self.back()
        self.wait_for()
        self.start_app()
        self.wait_for()
        self.back()
        self.wait_for()
        print('调试结束，测试开始\n场景一：back')
        while len(list_back) < 10:
            start_time = self.start_and_get_date()
            try:
                self.wait_explicit_ele('com.excelliance.dualaid:id/add_but', 15, 1)
            except Exception:
                # self.start_app()
                self.wait_explicit_ele('com.excelliance.dualaid:id/add_but', 15, 1)
            if '双开资讯' or 'com.excelliance.dualaid:id/tv_news' in getinfo.get_xml():
                list_back.append(start_time)
                print(list_back)
            self.back()
            time.sleep(2)
        return list_back

    def test_home(self):
        """home场景测试"""
        list_home = []
        self.start_app()
        self.wait_for()
        self.home()
        self.wait_for()
        self.start_app()
        self.wait_for()
        self.home()
        self.wait_for()
        print('调试结束，测试开始\n场景二：home')
        while len(list_home) < 10:
            start_time = self.start_and_get_date()
            try:
                self.wait_explicit_ele('com.excelliance.dualaid:id/ad_but', 15, 1)
            except Exception:
                self.wait_explicit_ele('com.excelliance.dualaid:id/ad_but', 15, 1)
            if '双开资讯' or 'com.excelliance.dualaid:id/tv_news' in getinfo.get_xml():
                list_home.append(start_time)
                print(list_home)
            self.home()
            time.sleep(2)
        return list_home

    def test_force(self):
        """冷启动场景测试"""
        list_force = []
        self.force_stop()
        self.wait_for()
        self.start_app()
        self.wait_for()
        self.force_stop()
        self.wait_for()
        print('调试结束，测试开始\n场景三：冷启动')
        while len(list_force) < 10:
            start_time = self.start_and_get_date()
            try:
                self.wait_explicit_ele('com.excelliance.dualaid:id/ad_but', 15, 1)
            except Exception:
                self.wait_explicit_ele('com.excelliance.dualaid:id/ad_but', 15, 1)
            if '双开资讯' or 'com.excelliance.dualaid:id/tv_news' in getinfo.get_xml():
                list_force.append(start_time)
                print(list_force)
            self.force_stop()
            time.sleep(2)
        return list_force

    def test_and_get_data1(self):
        # 将app调试到可测环境(调出广告和信息流)
        self.set_until_find_ad()
        self.start_app()
        self.wait_for()
        # 开始场景一测试
        self.list_back_test = self.test_back()
        self.wait_for(5)
        # 开始场景二测试
        self.list_home_test = self.test_home()
        self.wait_for(5)
        # 开始场景三测试
        self.list_force_test = self.test_force()
        self.wait_for(5)

    def test_and_get_data2(self):
        # 将app调试到可测环境(调出广告和信息流)
        self.set_until_find_ad()
        self.start_app()
        self.wait_for()
        # 开始场景一测试
        self.list_back_std = self.test_back()
        self.wait_for(5)
        # 开始场景二测试
        self.list_home_std = self.test_home()
        self.wait_for(5)
        # 开始场景三测试
        self.list_force_std = self.test_force()
        self.wait_for(5)

    def run_test(self):
        check = AppiumServerCheck()
        try:
            check.check_appium_server()
        except Exception:
            print('appium初始化失败')
        # 开启弹窗监控线程
        new_thread = CreateThread()
        pop = PopupHandle()
        new_thread.start_thread(pop.install_alert)
        # apk安装检测
        install = FilePath(r'Z:\start_time_SKZS')
        install.monitor()
        # 保存本次测试apk
        os.popen('move ' + install.get_file_path() + ' ' + r'Z:\start_time_SKZS\start_time_files\apk')
        print('测试阶段一：新版本')
        self.test_and_get_data1()
        # 切换app版本至比对版本(3.0.6)
        install = FilePath(r'Z:\start_time_SKZS\start_time_files\apk', style='3.0.6')
        install.monitor()
        print('测试阶段二：3.0.6版本')
        self.test_and_get_data2()
        # 停止appium服务端程序
        check.stop_appium_server()
        # 停止弹窗监控线程
        new_thread.stop_thread()

        # 计算需要输出的数据
        def avg(source):
            total = 0
            print(len(source))
            for i in source:
                total += i
            return total / len(source)

        # 新版平均值
        t_b_avg = avg(self.list_back_test)
        t_h_avg = avg(self.list_home_test)
        t_f_avg = avg(self.list_force_test)

        # 306版平均值
        s_b_avg = avg(self.list_back_std)
        s_h_avg = avg(self.list_home_std)
        s_f_avg = avg(self.list_force_std)

        # 新版最大值
        t_b_max = max(self.list_back_test)
        t_h_max = max(self.list_home_test)
        t_f_max = max(self.list_force_test)

        # 306版最大值
        s_b_max = max(self.list_back_std)
        s_h_max = max(self.list_home_std)
        s_f_max = max(self.list_force_std)

        # 平均值差值
        b_diff = t_b_avg - s_b_avg
        h_diff = t_h_avg - s_h_avg
        f_diff = t_f_avg - s_f_avg

        # 收集输出数据至指定集合
        global data_dict
        data_dict = {
            '新版back均值': t_b_avg,
            '新版home均值': t_h_avg,
            '新版force均值': t_f_avg,
            '老版back均值': s_b_avg,
            '老版home均值': s_h_avg,
            '老版force均值': s_f_avg,
            '新版back最大值': t_b_max,
            '新版home最大值': t_h_max,
            '新版force最大值': t_f_max,
            '老版back最大值': s_b_max,
            '老版home最大值': s_h_max,
            '老版force最大值': s_f_max,
            'back差值': b_diff,
            'home差值': h_diff,
            'force差值': f_diff
        }
        return data_dict


class EmailSending(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def create_email(self):
        """创建并发送邮件，测试报告通过邮件附件的形式发出"""
        username = self.username
        password = self.password
        smtpserver = 'smtp.ym.163.com'
        sender = username
        receiver = '771432505@qq.com'

        # 通过Header对象编码的文本，包含utf-8编码信息和Base64编码信息。以下中文名测试ok
        subject = '测试报告'
        subject = Header(subject, 'utf-8').encode()

        # 构造邮件对象MIMEMultipart对象
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = receiver

        # 构造文字内容
        if email_content_flag == 1:
            mail_content = """
            <div>
            <p><strong>启动时间测试报告<strong></p>
            <p>测试数据单位均为毫秒（ms）</p>
            <div id="content">
            <table border="1" bordercolor="#87ceeb" width="800">
                <tr>
                    <td>版本</td>
                    <td>back(avg)</td>
                    <td>back(max)</td>
                    <td>home(avg)</td>
                    <td>home(max)</td>
                    <td>冷启动(avg)</td>
                    <td>冷启动(max)</td>
                </tr>
                <tr>
                    <td>新版本</td>
                    <td>%d</td>
                    <td>%d</td>
                    <td>%d</td>
                    <td>%d</td>
                    <td>%d</td>
                    <td>%d</td>
                </tr>
                <tr>
                    <td>3.0.6版本</td>
                    <td>%d</td>
                    <td>%d</td>
                    <td>%d</td>
                    <td>%d</td>
                    <td>%d</td>
                    <td>%d</td>
                </tr>
                <tr>
                    <td>均值差</td>
                    <td>%d</td>
                    <td bgcolor="#87ceeb">null</td>
                    <td>%d</td>
                    <td bgcolor="#87ceeb">null</td>
                    <td>%d</td>
                    <td bgcolor="#87ceeb">null</td>
                </tr>
            </table>
            </div>
            </div>
            </body>
            </html>
            """ % (data_dict['新版back均值'], data_dict['新版back最大值'], data_dict['新版home均值'],
                   data_dict['新版home最大值'], data_dict['新版force均值'], data_dict['新版force最大值'],
                   data_dict['老版back均值'], data_dict['老版back最大值'], data_dict['老版home均值'],
                   data_dict['老版home最大值'], data_dict['老版force均值'], data_dict['老版force最大值'],
                   data_dict['back差值'], data_dict['home差值'], data_dict['force差值']
                   )
        else:
            mail_content = """
                        <h1>启动时间自动化测试失败<h1>
                        <p>失败原因：5次拉取信息流失败（以尝试调节系统时间后再拉取）</p>
                        """
        text = MIMEText(mail_content, 'html', 'utf-8')
        msg.attach(text)

        # 发送邮件
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver, 25)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver.split(','), msg.as_string())
        smtp.quit()


if __name__ == '__main__':
    test = StartTimeTest()
    emai = EmailSending('wangzhongchang@excelliance.cn', 'wzc6851498')
    test.run_test()
    emai.create_email()
