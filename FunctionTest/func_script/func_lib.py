# coding = UTF-8

__Auther__ = "EternalSunshine"
__title__ = "UI automator test"
import math
import operator  # for image operation and calculate
import os
import threading
import time
import winreg
from functools import reduce  # for image operation and calculate
from time import sleep

import selenium
from PIL import Image, ImageChops  # for image operation and calculate
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction  # for long_press operation
from appium.webdriver.webdriver import By  # for find toast
from appium.webdriver.webdriver import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  # for find toast

sys_alert = True
ap_alert = True


class AppiumInit(object):
    """appium server"""

    def appium_init(self):
        """to initialise appium session"""
        global driver
        getinfo = GetInfo()
        desired_cups = {}
        desired_cups['platformName'] = 'Android'
        desired_cups['platformVersion'] = getinfo.get_android_version()
        desired_cups['deviceName'] = getinfo.get_device_name()
        desired_cups['appPackage'] = 'com.excelliance.dualaid'
        desired_cups['appActivity'] = 'com.excelliance.kxqp.ui.HelloActivity'
        desired_cups['newCommandTimeout'] = 30000
        # desired_cups['noReset'] = False
        # desired_cups['unicodeKeyboard'] = 'true'
        # desired_cups['resetKeyboard'] = 'true'
        desired_cups['automationName'] = 'uiautomator2'  # define use uiautomator2 to find element,default is appium
        driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_cups)

    def quit(self):
        """to quit this session"""
        driver.quit()


class ScreenShot(object):
    """截图以及图片处理"""

    def screenshot_area(self):
        """根据状态栏尺寸，设置截图后截取图片的区域(*****需要优化*****)"""
        global box
        ele = driver.find_element_by_class_name('android.view.View')
        size = ele.size
        x2 = driver.get_window_size()['width']
        y2 = driver.get_window_size()['height']
        box = [0, size['height'], x2, y2]

    def screenshot(self, path, choice=0):
        """按设置区域截图,再转换图片位深度"""
        if choice == 1:
            driver.get_screenshot_as_file(path)
            image = Image.open(path)
            new_image = image.crop(box)
            new_image.save(path)
            Image.open(path).convert("RGB").save(path)
        elif choice == 0:
            driver.get_screenshot_as_file(path)
        else:
            print('argument error!')

    def image_contrast(self, img1, img2):
        """图片对比"""
        image1 = Image.open(img1)
        image2 = Image.open(img2)
        h1 = image1.histogram()
        h2 = image2.histogram()
        result = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
        return result

    def compare_images(self, path_one, path_two, path_diff):
        """对比两张截图并保存两张截图中不同的区域以便观察"""
        image_one = Image.open(path_one)
        image_two = Image.open(path_two)
        try:
            diff = ImageChops.difference(image_one, image_two)
            if diff.getbbox() is None:
                print("We are the same!")
            else:
                diff.save(path_diff)
        except ValueError as e:
            print(e, "错误，图片位深度可能与要求不符！")


class GetInfo(object):
    """信息获取"""

    def get_current_activity(self):
        """获取当前activity名"""
        # 第一种方法（该方法与手机型号相关，不同手机型号可能获取到的信息不同，慎用！！！）
        # a = os.popen('adb shell dumpsys activity | findstr "mF"')
        # for line in a.readlines():
        #     if "mFocusedActivity" in line:
        #         current_activity = line.split()[3]
        #         return current_activity

        # 第二种方法（appium自带的方法，获取的是去掉包名后的纯activity名）
        cur_act = driver.current_activity
        return cur_act

    def get_device_name(self):
        """获取设备名称（deviceName）"""
        b = os.popen('adb devices')
        device_name = b.readlines()[1].split()[0]
        return device_name

    def get_android_version(self):
        """获取设备Android版本"""
        c = os.popen('adb shell getprop ro.build.version.release')
        return c.readline()

    def get_middle_coordinate(self):
        """获取手机屏幕中心点坐标"""
        list1 = []
        x = (driver.get_window_size()['width'])
        y = (driver.get_window_size()['height'])
        list1.append(x)
        list1.append(y)
        return list1

    def get_time(self, display=1):
        """获取当前时间并以自定义格式返回"""
        if display == 1:
            now = time.strftime('%y%m%d%H%M%S')
        else:
            now = time.strftime('%Y.%m.%d_%H:%M:%S')
        return now

    def get_xml(self):
        """获取手机当前界面的元素信息"""
        content = driver.page_source
        return content

    def get_desktop_path(self):
        """获取系统桌面路径"""
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        return winreg.QueryValueEx(key, "Desktop")[0]


class UserOperation(object):
    """用户操作"""
    gf = GetInfo()

    def user_input(self, text):
        """用户输入"""
        for n in text:
            driver.press_keycode(int(n) + 7)

    def back(self):
        """back退出"""
        driver.press_keycode(4)

    def home(self):
        """home退出"""
        driver.press_keycode(3)

    def bg_app(self, t):
        """置于后台t秒"""
        driver.background_app(t)

    def swipe_left(self, t=300):
        """左滑"""
        L = self.gf.get_middle_coordinate()
        x1 = int(L[0] * 0.9)
        y1 = int(L[1] * 0.5)
        x2 = int(L[0] * 0.1)
        driver.swipe(x1, y1, x2, y1, t)

    def swipe_right(self, t=300):
        """右滑"""
        L = self.gf.get_middle_coordinate()
        x1 = int(L[0] * 0.1)
        y1 = int(L[1] * 0.5)
        x2 = int(L[0] * 0.9)
        driver.swipe(x1, y1, x2, y1, t)

    def swipe_up(self, t=500):
        """上滑"""
        L = self.gf.get_middle_coordinate()
        x1 = int(L[0] * 0.5)
        y1 = int(L[1] * 0.8)
        y2 = int(L[1] * 0.4)
        driver.swipe(x1, y1, x1, y2, t)

    def swipe_down(self, t=500):
        """下滑"""
        L = self.gf.get_middle_coordinate()
        x1 = int(L[0] * 0.5)
        y1 = int(L[1] * 0.4)
        y2 = int(L[1] * 0.8)
        driver.swipe(x1, y1, x1, y2, t)

    def find_element(self, ele):
        """控件定位（单个）"""
        element = []
        if ele.startswith("//"):
            element = driver.find_element_by_xpath(ele)
        elif ":id/" in ele:
            element = driver.find_element_by_id(ele)
        else:
            try:
                element = driver.find_element_by_class_name(ele)
            except:
                print("控件定位失败")
        return element

    def find_elements(self, ele):
        """控件定位（多个）"""
        elements = []
        if ele.startswith("//"):
            elements = driver.find_elements_by_xpath(ele)
        elif ":id/" in ele:
            elements = driver.find_elements_by_id(ele)
        else:
            try:
                elements = driver.find_elements_by_class_name(ele)
            except:
                print("控件定位失败")
        return elements

    def long_press(self, ele, t=1000):
        """长按"""
        touch = TouchAction(driver)
        touch.long_press(ele).wait(t).release().perform()

    def drag_and_drop(self, ele1, ele2):
        """长按元素ele1并将ele1拖动至ele2"""
        touch = TouchAction(driver)
        touch.long_press(ele1).wait(1000).move_to(ele2).wait(1000).release().perform()


class FindElement(object):
    """查找并定位控件"""
    op = UserOperation()

    def find_element(self, ele):
        """控件定位（单个）"""
        element = ""
        if ele.startswith("//"):
            element = driver.find_element_by_xpath(ele)
        elif ":id/" in ele:
            element = driver.find_element_by_id(ele)
        else:
            try:
                element = driver.find_element_by_class_name(ele)
            except:
                print("控件定位失败")
        return element

    def pc_find_elements(self, ele1, ele2):
        """控件定位（层级控件查找并按列表索引）"""
        element = self.find_element(ele1)
        elements = []
        if ele2.startswith("//"):
            elements = element.find_elements_by_xpath(ele2)
        elif ":id/" in ele2:
            elements = element.find_elements_by_id(ele2)
        else:
            try:
                elements = element.find_elements_by_class_name(ele2)
            except:
                print("控件定位失败")
        return elements

    def find_elements(self, ele):
        """控件定位3（同名控件查找并按列表索引）"""
        elements = []
        if ele.startswith("//"):
            elements = driver.find_elements_by_xpath(ele)
        elif ":id/" in ele:
            elements = driver.find_elements_by_id(ele)
        else:
            try:
                elements = driver.find_elements_by_class_name(ele)
            except:
                print("控件定位失败")
        return elements

    def find_element_new(self, ele):
        """控件定位4（uiautomator定位）"""
        element = ""
        if ":id/" in ele:
            element = driver.find_element_by_android_uiautomator('new UiSelector().resouceId(controlInfo)')
        else:
            print("定位失败，仅支持id类型的定位")
        return element

    def swipe_find_element(self, ele, t=500, direction='U'):
        """swipe down to find element whitch you want"""
        while True:
            try:
                self.find_element(ele).click()
                break
            except:
                if direction == 'U':
                    self.op.swipe_up(t)
                    sleep(0.5)
                elif direction == 'D':
                    self.op.swipe_down(t)
                    sleep(0.5)
                elif direction == 'L':
                    self.op.swipe_left(t)
                    sleep(0.5)
                elif direction == 'R':
                    self.op.swipe_right(t)
                    sleep(0.5)
                else:
                    print("argument error, you can only choose one word from (U,D,L,R)")


class Waiting(object):
    """等待方式"""
    ele = FindElement()

    def wait_for(self, n=2):
        """硬等待"""
        sleep(n)

    def wait_explicit_ele(self, controlInfo, time=15, frequency=2):
        """显式等待元素出现（直到until方法执行完毕，或者等待10秒后等待取消）"""
        WebDriverWait(driver, time, frequency).until(lambda driver: self.ele.find_element(controlInfo))

    def wait_explicit_act(self, controlInfo, time=15, frequency=2):
        """显式等待activity出现（直到until方法执行完毕，或者等待10秒后等待取消）"""
        driver.wait_activity(controlInfo, time, frequency)

    def is_toast_exist(self, message):
        """查找toast并返回布尔类型结果"""
        toast = '//*[@text="%s"]' % message
        try:
            WebDriverWait(driver, 5, 0.1).until(EC.presence_of_element_located((By.XPATH, toast)))
            return True
        except:
            return False


class PhoneSetting(object):
    """手机系统相关设置(*****需要优化适配*****)"""
    ele = FindElement()
    wait = Waiting()
    op = UserOperation()

    def set_system_time(self, n):
        """系统时间向后调3天"""
        self.op.home()
        self.wait.wait_for(1)
        try:
            self.ele.find_element('//*[@text="设置"]').click()
        except Exception as e:
            print(e, "目前调系统时间方法仅适用于 oppo R11手机!!!")
        self.wait.wait_for(1)
        try:
            self.ele.swipe_find_element('//*[@text="其他设置"]', 500)
        except Exception as e:
            print(e, "目前调系统时间方法仅适用于 oppo R11手机!!!")
        self.wait.wait_for(1)
        self.ele.find_element('//*[@text="日期与时间"]').click()
        self.wait.wait_for(1)
        try:
            self.ele.find_element('//*[@text="设置时间"]').click()
            self.wait.wait_for(1)
        except:
            self.ele.find_elements('android:id/switch_widget')[1].click()
            self.wait.wait_for(1)
            self.ele.find_element('//*[@text="设置时间"]').click()
            self.wait.wait_for(1)
        while n:
            self.ele.find_element('oppo:id/increment').click()
            self.wait.wait_for(2)
            n -= 1
        self.wait.wait_for(1)
        self.op.home()


class AppOperation(object):
    """app自身相关操作和设置"""
    op = UserOperation()
    ele = FindElement()
    wait = Waiting()
    ps = PhoneSetting()

    def clear_app(self):
        """清除数据"""
        os.popen("adb shell pm clear com.excelliance.dualaid")

    def force_stop(self, pck):
        """强行停止"""
        os.popen("adb shell am force-stop " + pck)

    def start_app(self, choice=0):
        """启动APP（choice=0正常启动，choice=1时，启动并返回启动耗时）"""
        if choice == 0:
            os.popen("adb shell am start com.excelliance.dualaid/com.excelliance.kxqp.ui.HelloActivity")
        elif choice == 1:
            t = os.popen("adb shell am start -W com.excelliance.dualaid/com.excelliance.kxqp.ui.HelloActivity")
            for line in t.readlines():
                if "TotalTime" in line:
                    start_time = line.split()[1]
                    return start_time
        else:
            print("argument error, you can only choose 0 or 1")

    def set_app_status1(self):
        """启动APP至状态1（添加引导页）"""
        self.wait.wait_for()
        self.ele.swipe_find_element('com.excelliance.dualaid:id/bt_explore', 300, 'L')
        self.wait.wait_explicit_ele('com.excelliance.dualaid:id/first_start_ok')

    def set_app_status2(self):
        """启动APP至状态2（无banner，icon，无信息流,无钻石按钮的主界面）"""
        self.set_app_status1()
        self.ele.find_element('com.excelliance.dualaid:id/jump_to').click()
        self.wait.wait_explicit_ele('com.excelliance.dualaid:id/tv_bt_add')
        self.op.back()
        self.wait.wait_for()

    def set_app_status3(self):
        """启动APP至状态3（有banner，icon，无信息流，无钻石按钮的主界面）"""
        i = 3
        self.set_app_status2()
        self.op.back()
        self.wait.wait_for()
        self.start_app()
        self.wait.wait_for()
        while i > 0:
            i -= 1
            try:
                self.wait.wait_explicit_ele("com.excelliance.dualaid:id/ad_but", 10, 1)
                break
            except Exception as e:
                print(e, "尝试第%d次" % i)
                self.op.back()
                self.wait.wait_for()
                self.start_app()
                self.wait.wait_for()

    def set_app_status4(self):
        """启动APP至状态4（有banner，icon，信息流，钻石按钮的主界面）"""
        i = 3
        j = 3
        self.wait.wait_for(2)
        self.ele.swipe_find_element('com.excelliance.dualaid:id/bt_explore', 300, 'L')
        self.wait.wait_explicit_ele('com.excelliance.dualaid:id/first_start_ok')
        self.ele.find_element('com.excelliance.dualaid:id/jump_to').click()
        self.wait.wait_explicit_ele('com.excelliance.dualaid:id/tv_bt_add')
        self.op.back()
        self.wait.wait_for(1)
        self.op.back()
        self.wait.wait_for(2)
        self.start_app()
        self.wait.wait_explicit_ele("com.excelliance.dualaid:id/iv_icon")
        while i > 0:
            i -= 1
            try:
                self.wait.wait_explicit_ele("com.excelliance.dualaid:id/ad_but", 10, 1)
                break
            except Exception as e:
                print(e, "尝试第%d次" % i)
                self.op.back()
                self.wait.wait_for()
                self.start_app()
                self.wait.wait_for()
        self.op.back()
        self.ps.set_system_time(3)
        self.wait.wait_for(1)
        self.start_app()
        while j > 0:
            j -= 1
            try:
                self.wait.wait_explicit_ele('//*[@text="双开资讯"]', 10)
                break
            except Exception as e:
                print(e)
                try:
                    self.op.back()
                    self.wait.wait_for(1)
                    self.start_app()
                    self.wait.wait_for()
                except Exception as e:
                    print(e, "尝试第%d次" % j)
                    self.op.back()
                    self.wait.wait_for(1)
                    self.ps.set_system_time(1)
                    self.start_app()
                    self.wait.wait_for()

    def set_app_status5(self):
        """启动APP至状态5（登录非VIP账号后的个人中心页）"""
        self.set_app_status2()
        self.ele.find_element('com.excelliance.dualaid:id/iv_icon').click()
        self.wait.wait_explicit_ele('//*[@text="个人中心"]')
        self.ele.find_element('com.excelliance.dualaid:id/iv_icon').click()
        self.wait.wait_explicit_ele('com.excelliance.dualaid:id/btn_next_step')
        self.op.user_input('18501701705')
        self.ele.find_element('com.excelliance.dualaid:id/btn_next_step').click()
        self.wait.wait_explicit_ele('com.excelliance.dualaid:id/tv_login')
        self.op.user_input('000000')
        self.ele.find_element('com.excelliance.dualaid:id/tv_login').click()
        self.wait.wait_explicit_ele('com.excelliance.dualaid:id/rl_update')

    def set_app_status7(self):
        """启动APP至状态7（登陆VIP账号后的平铺界面）"""
        self.set_app_status1()
        self.ele.find_element('com.excelliance.dualaid:id/tv_login_in').click()
        self.wait.wait_explicit_ele('com.excelliance.dualaid:id/btn_next_step')
        self.op.user_input('123456789')
        self.ele.find_element('com.excelliance.dualaid:id/btn_next_step').click()
        self.wait.wait_explicit_ele('com.excelliance.dualaid:id/tv_login')
        self.op.user_input('111111')
        self.ele.find_element('com.excelliance.dualaid:id/tv_login').click()
        self.wait.wait_explicit_act('com.excelliance.dualaid/com.excelliance.kxqp.ui.MainActivity', 10, 1)
        self.op.back()
        self.wait.wait_explicit_ele('com.excelliance.dualaid:id/ib_lock')

    def set_app_status6(self):
        """启动APP至状态6（登陆VIP账号后的主界面）"""
        self.set_app_status7()
        self.ele.find_element('com.excelliance.dualaid:id/ib_lock').click()
        self.wait.wait_explicit_ele('com.excelliance.dualaid:id/tv_bt_add')
        self.op.back()
        self.wait.wait_for()


class PopupHandle(object):
    """处理测试过程中不定时出现的系统弹窗和app自身的弹窗"""
    ele = FindElement()
    wait = Waiting()
    gf = GetInfo()

    def sys_win_alert(self):
        """监控并处理系统弹窗"""
        print('thread-1 is working')
        global sys_alert
        while sys_alert:
            alert = os.popen('adb shell dumpsys window|find "permission"')
            if "SYSTEM_ALERT_WINDOW" in alert.read():
                try:
                    self.ele.find_element('//*[@text="允许"]').click()
                except selenium.common.exceptions.NoSuchElementException:
                    self.ele.find_element('//*[@text="确定"]').click()
                except selenium.common.exceptions.NoSuchElementException:
                    self.ele.find_element('//*[@text="忽略"]').click()
                except selenium.common.exceptions.NoSuchElementException:
                    self.ele.find_element('//*[@text="以后再说"]').click()
            else:
                continue

    def app_alert(self):
        """监控并处理应用弹窗"""
        print('thread-2 is working')
        global ap_alert
        while ap_alert:
            if 'com.excelliance.dualaid:id/ll_dialog' in self.gf.get_xml():
                if '64位' in self.gf.get_xml():
                    self.ele.find_element('com.excelliance.dualaid:id/bt_cancel').click()
                elif '应用列表' in self.gf.get_xml():
                    try:
                        self.ele.find_element('//*[@text="不再提醒"]').click()
                        self.ele.find_element('//*[@text="以后再说"]').click()
                    except Exception:
                        self.ele.find_element('com.excelliance.dualaid:id/tv_left').click()
                    except Exception:
                        self.ele.find_element('//*[@text="忽略"]').click()
            else:
                continue


class CreateThread(object):
    """创建新线程"""

    def start_thread(self, func):
        """开启一条执行func函数的新线程"""
        thread = threading.Thread(target=func)
        thread.start()

    def stop_thread(self):
        global sys_alert
        global ap_alert
        sys_alert = False
        ap_alert = False


class Log(object):
    """用例执行日志"""
    pass


class Logcat(object):
    """手机日志"""
    # log_name = ''
    getinfo = GetInfo()
    """抓取和停止手机logcat"""

    def start_logcat(self, log_path):
        os.popen('adb logcat -c')
        log_name = os.path.join(log_path, 'log%s.txt' % self.getinfo.get_time())
        os.popen('adb logcat -v time > %s' % log_name)

    def stop_logcat(self):
        data = os.popen('adb shell ps | findstr "logcat"')
        for logcat_uid in data.readlines():
            if "shell" in logcat_uid:
                os.popen('adb shell kill ' + logcat_uid.split()[1])


class Delete(object):
    """删除文件和文件夹"""

    def del_file(self, file_path):
        if os.path.isfile(file_path):
            os.remove(file_path)
        else:
            print('No such file:%s' % file_path)

    def del_directory(self, dir_path):
        if os.path.isdir(dir_path):
            os.rmdir(dir_path)
        else:
            print('No such directory:%s' % dir_path)


# 设置基本路径
getinfo = GetInfo()
BASE_PATH = os.path.abspath(os.path.dirname('main.py'))
log_path = os.path.join(BASE_PATH, 'test_result\\logs\\')
img_path = os.path.join(BASE_PATH, 'test_result\\error_img\\')
report_path = os.path.join(BASE_PATH, 'test_result\\双开助手测试报告%s.html' % getinfo.get_time())
