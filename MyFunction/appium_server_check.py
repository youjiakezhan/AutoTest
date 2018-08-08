import os
import sys
import time
import urllib

import selenium
from appium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

pck_name = ''
activity = ''


# appium封装
class AppiumServerCheck(object):

    def appium_init(self):
        """to initialise appium session"""
        desired_cups = {}
        global driver
        desired_cups['platformName'] = 'Android'
        desired_cups['platformVersion'] = '5.1.1'
        desired_cups['deviceName'] = '900ca8ab'
        desired_cups['appPackage'] = ''
        desired_cups['appActivity'] = ''
        desired_cups['autoLaunch'] = 'false'
        desired_cups['noReset'] = 'true'
        desired_cups['automationName'] = 'uiautomator2'
        driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_cups)
        return driver

    def quit(self):
        """to quit this session"""
        driver.quit()

    def wait_for(self, n=2):
        """硬等待"""
        time.sleep(n)

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

    # 检测appium服务是否已开启，如未开启则自动开启服务进行初始化
    # 如已开启直接进行初始化
    def check_appium_server(self):
        if self.check_adb_connect() is True:
            if 'node.exe' in os.popen('tasklist | findstr "node.exe"').read():
                while True:
                    try:
                        self.appium_init()
                        break
                    except ConnectionRefusedError:
                        self.wait_for(3)
                    except urllib.error.URLError:
                        self.wait_for(3)
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
                                self.wait_for(3)
                            except urllib.error.URLError:
                                self.wait_for(3)
                        print('appium初始化完成')
                        break
                    else:
                        self.wait_for(1)
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
