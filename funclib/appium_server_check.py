import os
import sys
import time
import urllib
from AutoTest.funclib.adb_command import AdbCommand
import selenium
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait


pkg_name = ''
activity = ''
device_name = ''
android_version = ''


class AppiumServerCheck(object):
    adb = AdbCommand(pkg_name)

    def appium_init(self):
        """to initialise appium session"""
        desired_cups = {}
        desired_cups['platformName'] = 'Android'
        desired_cups['platformVersion'] = android_version
        desired_cups['deviceName'] = device_name
        desired_cups['appPackage'] = pkg_name
        desired_cups['appActivity'] = activity
        desired_cups['autoLaunch'] = 'false'
        desired_cups['noReset'] = 'true'
        desired_cups['automationName'] = 'uiautomator2'
        driver = webdriver.Remote('http://127.0.0.path:4723/wd/hub', desired_cups)
        global driver
        return driver

    def quit(self):
        """to quit this session"""
        driver.quit()

    def wait_for_element(self, controlinfo, time=20, frequency=1):
        """显式等待元素出现（直到until方法执行完毕，或者等待10秒后等待取消）"""
        if r'//*' in controlinfo:
            try:
                WebDriverWait(driver, time, frequency).until(lambda driver: driver.find_element_by_xpath(controlinfo))
            except selenium.common.exceptions.WebDriverException:
                print('等待元素%s出错' % controlinfo)
        elif r'id/' in controlinfo:
            try:
                WebDriverWait(driver, time, frequency).until(lambda driver: driver.find_element_by_id(controlinfo))
            except selenium.common.exceptions.WebDriverException:
                print('等待元素%s出错' % controlinfo)

    # 检测appium服务是否已开启，如未开启则自动开启服务并进行初始化，如已开启直接进行初始化
    def check_appium_server(self):
        if self.adb.check_adb_connect() is True:
            if 'node.exe' in os.popen('tasklist | findstr "node.exe"').read():
                while True:
                    try:
                        self.appium_init()
                        break
                    except ConnectionRefusedError:
                        time.sleep(3)
                    except urllib.error.URLError:
                        time.sleep(3)
                print('appium初始化完成')
            else:
                os.popen("start appium")
                print("正在启动appium服务程序，请稍等...")
                while True:
                    if 'node.exe' in os.popen('tasklist | findstr "node.exe"').read():
                        while True:
                            try:
                                self.appium_init()
                                break
                            except ConnectionRefusedError:
                                time.sleep(3)
                            except urllib.error.URLError:
                                time.sleep(3)
                        print('appium初始化完成')
                        break
                    else:
                        time.sleep(1)
                        continue
        else:
            sys.exit()

    def stop_appium_server(self):
        # 结束appium进程（Windows适用）
        pid_node = os.popen('tasklist | findstr "node.exe"').readlines()
        for i in pid_node:
            os.popen('taskkill /f /pid ' + i.split()[1])
        pid_cmd = os.popen('tasklist | findstr "cmd.exe"').readlines()
        for i in pid_cmd:
            os.popen('taskkill /f /pid ' + i.split()[1])


