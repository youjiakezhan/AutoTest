import os
import smtplib
import threading
import time
import urllib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import selenium
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

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
email_content_flag = 1
alert_flag = 1
pck_name = 'com.excelliance.dualaid'
activity = 'com.excelliance.kxqp.ui.HelloActivity'


class FilePath(object):

    def __init__(self, apk_path, style='.apk'):
        self.apk_path = apk_path
        self.style = style

    def get_file_path(self):
        """获取daily review安装包路径"""
        for file in os.listdir(self.apk_path):
            file_path = os.path.join(self.apk_path, file)
            if self.style in file_path and os.path.isfile(file_path):
                return file_path

    def check_adb_connect(self):
        """查看USB是否已连接"""
        text = os.popen('adb devices')
        time.sleep(5)
        if 'device' in text.readlines()[1]:
            return True
        else:
            print('USB未连接')
            return False

    def uninstall_apk(self):
        """卸载本机已有双开助手apk"""
        if 'com.excelliance.dualaid' in os.popen('adb shell pm list package -3 | findstr "excelliance"').read():
            os.popen('adb uninstall com.excelliance.dualaid')

    def install_apk(self):
        """安装daily review包"""

        os.popen('adb install -r ' + self.get_file_path())

    def monitor(self):
        """
        检查本机是否有daily review包同名apk，如果有就删除，如果没有就去指定目录检查，有apk包就执行安装，没有就等待，
        直到安装成功为止，安装完成后将该目录下的安装包移动至存放apk的目录
        """
        if self.check_adb_connect() is True:
            self.uninstall_apk()
            time.sleep(2)
            while True:
                try:
                    self.install_apk()
                    print('正在尝试自动安装测试包\n')
                    time.sleep(30)
                    if 'com.excelliance.dualaid' in os.popen(
                            'adb shell pm list package -3 | findstr "excelliance"').read():
                        print('安装完成，正在配置测试环境...\n')
                        break
                    else:
                        print('自动安装测试包失败，请手动进行安装\n')
                        continue
                except TypeError:
                    print('未检测到双开助手安装包\n本次检测时间：%s\n' % time.strftime('%Y.%m.%d_%H:%M:%S'))
                    time.sleep(10)


# appium封装
class AppiumServerCheck(object):

    def appium_init(self):
        """to initialise appium session"""
        desired_cups = {}
        global driver
        desired_cups['platformName'] = 'Android'
        desired_cups['platformVersion'] = '5.1.1'
        desired_cups['deviceName'] = '900ca8ab'
        desired_cups['appPackage'] = pck_name
        desired_cups['appActivity'] = activity
        desired_cups['noReset'] = 'true'
        desired_cups['automationName'] = 'appium'
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_cups)
        return driver

    def quit(self):
        """to quit this session"""
        driver.quit()

    def app_start(self):
        os.popen('adb shell am start ' + pck_name + '/' + activity)

    def app_back(self):
        os.popen('adb shell input keyevent 4')

    def app_home(self):
        os.popen('adb shell input keyevent 3')

    def app_force_stop(self):
        os.popen('adb shell am force-stop ' + pck_name)

    def app_data_clear(self):
        os.popen('adb shell pm clear ' + pck_name)

    def wait_for(self, n=2):
        """硬等待"""
        time.sleep(n)

    def wait_for_element(self, controlinfo, time=20, frequency=1):
        """显式等待元素出现（直到until方法执行完毕，或者等待10秒后等待取消）"""
        if '//' in controlinfo:
            WebDriverWait(driver, time, frequency).until(lambda driver: driver.find_element_by_xpath(controlinfo))
        elif ':id/' in controlinfo:
            WebDriverWait(driver, time, frequency).until(lambda driver: driver.find_element_by_id(controlinfo))

    def check_appium_server(self):
        # 检测appium服务是否已开启，如未开启则自动开启服务进行初始化
        # 如已开启直接进行初始化
        if 'node.exe' in os.popen('tasklist | findstr "node.exe"').read():
            while True:
                try:
                    self.appium_init()
                    break
                except ConnectionRefusedError:
                    self.wait_for(3)
                except urllib.error.URLError:
                    self.wait_for(3)
            self.app_force_stop()
            print('测试环境OK，开始执行测试\n')
        else:
            os.popen("start appium")
            print("正在启动appium服务程序，请稍等...\n")
            while True:
                if 'node.exe' in os.popen('tasklist | findstr "node.exe"').read():
                    while True:
                        try:
                            self.appium_init()
                            break
                        except ConnectionRefusedError:
                            self.wait_for(3)
                        except urllib.error.URLError:
                            self.wait_for(3)
                    self.app_force_stop()
                    print('测试环境OK，开始执行测试\n')
                    break
                else:
                    self.wait_for(3)

    def stop_appium_server(self):
        # 结束appium进程（Windows适用）
        pid_node = os.popen('tasklist | findstr "node.exe"').readlines()
        for i in pid_node:
            os.popen('taskkill /f /pid ' + i.split()[1])
        pid_cmd = os.popen('tasklist | findstr "cmd.exe"').readlines()
        for i in pid_cmd:
            os.popen('taskkill /f /pid ' + i.split()[1])

    def get_middle_coordinate(self):
        """获取手机屏幕中心点坐标"""
        list = []
        x = (driver.get_window_size()['width'])
        y = (driver.get_window_size()['height'])
        list.append(x)
        list.append(y)
        return list

    def swipe_left(self, t=300):
        """左滑"""
        L = self.get_middle_coordinate()
        x1 = int(L[0] * 0.9)
        y1 = int(L[1] * 0.5)
        x2 = int(L[0] * 0.1)
        driver.swipe(x1, y1, x2, y1, t)

    def swipe_right(self, t=300):
        """右滑"""
        L = self.get_middle_coordinate()
        x1 = int(L[0] * 0.1)
        y1 = int(L[1] * 0.5)
        x2 = int(L[0] * 0.9)
        driver.swipe(x1, y1, x2, y1, t)

    def swipe_up(self, t=500):
        """上滑"""
        L = self.get_middle_coordinate()
        x1 = int(L[0] * 0.5)
        y1 = int(L[1] * 0.8)
        y2 = int(L[1] * 0.4)
        driver.swipe(x1, y1, x1, y2, t)

    def swipe_down(self, t=500):
        """下滑"""
        L = self.get_middle_coordinate()
        x1 = int(L[0] * 0.5)
        y1 = int(L[1] * 0.4)
        y2 = int(L[1] * 0.8)
        driver.swipe(x1, y1, x1, y2, t)

    def swipe_find_element(self, controlinfo, t=500, direction='U'):
        """swipe down to find element whitch you want"""
        count = 5
        while count > 0:
            try:
                if '//' in controlinfo:
                    driver.find_element_by_xpath(controlinfo).click()
                elif ':id/' in controlinfo:
                    driver.find_element_by_id(controlinfo).click()
                break
            except Exception:
                count -= 1
                if direction == 'U':
                    self.swipe_up(t)
                    self.wait_for(1)
                elif direction == 'D':
                    self.swipe_down(t)
                    self.wait_for(1)
                elif direction == 'L':
                    self.swipe_left(t)
                    self.wait_for(1)
                elif direction == 'R':
                    self.swipe_right(t)
                    self.wait_for(1)


# 线程创建/结束
class CreateThread(object):

    def start_thread(self, func):
        """开启一条执行func函数的新线程"""
        thread = threading.Thread(target=func)
        thread.start()

    def stop_thread(self):
        global alert_flag
        alert_flag = 0
        while True:
            if threading.active_count() > 1:
                time.sleep(2)
            else:
                break


# 弹窗处理
class SuperVision(object):
    app = AppiumServerCheck()

    def install_alert(self):
        """监控并处理应用安装弹窗"""
        print('应用安装弹窗监控已启动')
        while alert_flag == 1:
            if "com.android.packageinstaller:id/apk_info_view" in driver.page_source:
                print('应用安装弹窗监控检测到apk安装提示，正在处理...')
                try:
                    app.wait_for_element('//*[@text="继续安装"]', 20, 1)
                    driver.find_element_by_xpath('//*[@text="继续安装"]').click()
                    app.wait_for_element('//*[@text="安装"]', 20, 1)
                    driver.find_element_by_xpath('//*[@text="安装"]').click()
                    app.wait_for_element('//*[@text="完成"]', 20, 1)
                    driver.find_element_by_xpath('//*[@text="完成"]').click()
                    print('apk安装完成')
                except selenium.common.exceptions.NoSuchElementException:
                    print('apk安装失败，正在尝试重新安装')
                except Exception:
                    print('apk安装失败，正在尝试重新安装')
            else:
                continue

    def pemission_alert(self):
        print('权限弹窗监控已启动')
        while alert_flag == 1:
            if "oppo:id/permission_prompt" in driver.page_source:
                print('权限弹窗监控检测到apk权限弹窗，正在处理...')
                try:
                    driver.find_element_by_xpath('//*[@text="不再提醒"]').click()
                    driver.find_element_by_id('android:id/button1').click()
                    print('已同意apk获取权限')
                except selenium.common.exceptions.NoSuchElementException:
                    # driver.find_element_by_id('oppo:id/remember_cb').click()
                    print('apk获取权限失败')
                except selenium.common.exceptions.StaleElementReferenceException:
                    print('apk获取权限失败')
            else:
                continue

    def update_alert(self):
        print('APP弹窗监控已启动')
        while alert_flag == 1:
            if 'com.excelliance.dualaid:id/ll_dialog' in driver.page_source:
                print('APP弹窗监控检测到apk更新提示弹窗，正在处理...')
                try:
                    driver.find_element_by_id('com.excelliance.dualaid:id/cb_noToast').click()
                    driver.find_element_by_id('com.excelliance.dualaid:id/tv_left').click()
                    print('已忽略apk更新')
                except selenium.common.exceptions.NoSuchElementException:
                    print('处理apk更新弹窗失败')
            else:
                continue


# 邮件发送测试报告
class EmailSending(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    # 创建并发送邮件
    def create_email(self):
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

        # 构造邮件内容（html形式）
        # 判断是否拉取到信息流
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


# app启动时间测试类
class StartTimeTest(AppiumServerCheck):

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
        date = os.popen('adb shell am start -W ' + pck_name + '/' + activity)
        time_data = date.readlines()
        for i in time_data:
            if 'TotalTime' in i:
                app_start_time = i.split(':')[1].strip()
                # print(app_start_time)
        return int(app_start_time)

    # 设置手机（oppoR7）系统时间
    def set_phone_time(self):
        self.app_back()
        self.wait_for()
        self.app_home()
        self.wait_for()
        driver.find_element_by_xpath('//*[@text="设置"]').click()
        try:
            self.swipe_find_element('//*[@text="日期和时间"]')
        except Exception:
            self.swipe_find_element('//*[@text="日期和时间"]')
        except Exception:
            print('设置手机时间失败')
        if driver.find_element_by_xpath('//*[@text="设置日期"]').is_enabled() is False:
            driver.find_elements_by_id('android:id/checkbox')[0].click()
            self.wait_for()
            driver.find_element_by_xpath('//*[@text="设置日期"]').click()
            self.wait_for()
            driver.find_elements_by_id('oppo:id/increment')[1].click()
            self.wait_for()
            driver.find_element_by_id('android:id/button1').click()
        else:
            driver.find_element_by_xpath('//*[@text="设置日期"]').click()
            self.wait_for()
            driver.find_elements_by_id('oppo:id/increment')[1].click()
            self.wait_for()
            driver.find_element_by_id('android:id/button1').click()
        self.app_home()
        self.wait_for()
        self.app_start()
        self.wait_for_element('com.excelliance.dualaid:id/add_but')

    def set_app_status(self):
        """启动APP至状态（有banner，icon，无信息流，无钻石按钮的主界面）"""
        i = 1
        self.wait_for()
        self.swipe_find_element('com.excelliance.dualaid:id/bt_explore', 300, 'L')
        self.wait_for_element('com.excelliance.dualaid:id/jump_to')
        driver.find_element_by_id('com.excelliance.dualaid:id/jump_to').click()
        self.wait_for_element('com.excelliance.dualaid:id/tv_bt_add', 30, 2)
        self.app_back()
        self.wait_for()
        self.app_back()
        self.wait_for()
        self.app_start()
        while i < 4:
            print("配置测试环境:第%d次" % i)
            try:
                self.wait_for_element("com.excelliance.dualaid:id/ad_but", 30, 2)
                break
            except selenium.common.exceptions.TimeoutException:
                print("环境配置失败")
                self.app_back()
                self.wait_for(3)
                self.app_start()
                i += 1

    # 设置测试环境（拉取广告及信息流）
    def set_until_find_ad(self):
        self.app_start()
        self.wait_for()
        try:
            self.set_app_status()
            if driver.find_element_by_id('com.excelliance.dualaid:id/iv_close').is_displayed():
                driver.find_element_by_id('com.excelliance.dualaid:id/iv_close').click()
        except selenium.common.exceptions.NoSuchElementException:
            print('未拉取到广告')
        except selenium.common.exceptions.TimeoutException:
            print('未拉取到广告')

        # 添加微信
        try:
            driver.find_element_by_xpath('//*[@text="微信"]').click()
            self.wait_for(5)
            if driver.find_element_by_id('com.excelliance.dualaid:id/tv_app_add').is_displayed() is True:
                self.app_back()
            else:
                print('添加微信失败')
        except Exception:
            print('添加微信失败')

        # 调出信息流
        self.set_phone_time()
        i = 1
        while i <= 5:
            print('第%s次拉取信息流' % i)
            i += 1
            if '双开资讯' or 'com.excelliance.dualaid:id/tv_news' in driver.page_source:
                self.app_back()
                self.wait_for()
                break
            else:
                print('拉取信息流失败')
                self.set_phone_time()
        # 5次拉取失败的话，邮件通知拉取不到信息流
        if i == 5:
            global email_content_flag
            email_content_flag = 0
            em = EmailSending('wangzhongchang@excelliance.cn', 'wzc6851498')
            em.create_email()

    # back场景测试
    def test_back(self):
        list_back = []
        driver.back()
        self.wait_for()
        self.app_start()
        self.wait_for()
        self.app_back()
        self.wait_for()
        print('调试结束，测试开始\n场景一：back')
        while len(list_back) < 22:
            start_time = self.start_and_get_date()
            try:
                self.wait_for_element('com.excelliance.dualaid:id/add_but', 15, 1)
                self.wait_for()
            except Exception:
                self.wait_for_element('com.excelliance.dualaid:id/add_but', 15, 1)
            if '双开资讯' or 'com.excelliance.dualaid:id/tv_news' in driver.page_source:
                list_back.append(start_time)
                # print(list_back)
                driver.back()
            self.wait_for(2)
            print(list_back)
        # 去掉一个最大值和一个最小值
        list_back.remove(max(list_back))
        list_back.remove(min(list_back))
        return list_back

    # home场景测试
    def test_home(self):
        list_home = []
        self.app_start()
        self.wait_for()
        self.app_home()
        self.wait_for()
        self.app_start()
        self.wait_for()
        self.app_home()
        self.wait_for()
        print('调试结束，测试开始\n场景二：home')
        while len(list_home) < 22:
            start_time = self.start_and_get_date()
            try:
                self.wait_for_element('com.excelliance.dualaid:id/ad_but', 15, 1)
            except Exception:
                self.wait_for_element('com.excelliance.dualaid:id/ad_but', 15, 1)
            if '双开资讯' or 'com.excelliance.dualaid:id/tv_news' in driver.page_source:
                list_home.append(start_time)
                # print(list_home)
                self.app_home()
            self.wait_for(2)
            print(list_home)
        # 去掉一个最大值和一个最小值
        list_home.remove(max(list_home))
        list_home.remove(min(list_home))
        return list_home

    # 冷启动场景测试
    def test_force(self):
        list_force = []
        self.app_force_stop()
        self.wait_for()
        self.app_start()
        self.wait_for()
        self.app_force_stop()
        self.wait_for()
        print('调试结束，测试开始\n场景三：冷启动')
        while len(list_force) < 22:
            start_time = self.start_and_get_date()
            try:
                self.wait_for_element('com.excelliance.dualaid:id/ad_but', 15, 1)
                self.wait_for()
            except Exception:
                self.wait_for_element('com.excelliance.dualaid:id/ad_but', 15, 1)
            if '双开资讯' or 'com.excelliance.dualaid:id/tv_news' in driver.page_source:
                list_force.append(start_time)
                # print(list_force)
            self.app_force_stop()
            self.wait_for(2)
            print(list_force)
        # 去掉一个最大值和一个最小值
        list_force.remove(max(list_force))
        list_force.remove(min(list_force))
        return list_force

    # 启动并收集测试数据（新版本）
    def test_and_get_data1(self):
        # 将app调试到可测环境(调出广告和信息流)
        self.set_until_find_ad()
        self.app_start()
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

    # 启动并收集测试数据（3.0.6版本）
    def test_and_get_data2(self):
        # 将app调试到可测环境(调出广告和信息流)
        self.set_until_find_ad()
        self.app_start()
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

    # 启动测试入口
    def run_test(self):
        self.check_appium_server()

        # 开启弹窗监控线程
        new_thread = CreateThread()
        alert = SuperVision()
        new_thread.start_thread(alert.install_alert)
        new_thread.start_thread(alert.pemission_alert)
        new_thread.start_thread(alert.update_alert)

        # apk安装检测
        install = FilePath(r'Z:\start_time_SKZS')
        install.monitor()

        # 保存本次测试apk
        os.popen('move ' + install.get_file_path() + ' ' + r'Z:\start_time_SKZS\start_time_files\apk')
        print('阶段一：新版本测试')
        self.test_and_get_data1()

        # 切换app版本至比对版本(3.0.6)
        install = FilePath(r'Z:\start_time_SKZS\start_time_files\apk', style='3.0.6')
        install.monitor()
        print('阶段二：3.0.6版本测试')
        self.test_and_get_data2()

        # 停止弹窗监控线程
        new_thread.stop_thread()

        # 计算需要输出的数据
        def avg(list):
            average = sum(list) / len(list)
            return average

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

        # 停止appium服务端程序
        self.quit()
        self.wait_for()
        self.stop_appium_server()

        return data_dict


if __name__ == '__main__':
    thread = CreateThread()
    app = AppiumServerCheck()
    test = StartTimeTest()
    e = EmailSending('wangzhongchang@excelliance.cn', 'wzc6851498')
    while True:
        test.run_test()
        e.create_email()
        time.sleep(60)
