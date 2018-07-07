import unittest
from FunctionTest.func_script.func_lib import *
import matplotlib.pyplot as plt
import numpy as np


plt.rcParams['font.sans-serif'] = ['KaiTi']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
pck_name = "com.excelliance.dualaid"
launchable_activity = "/com.excelliance.kxqp.ui.HelloActivity"


class StartTimeTest(unittest.TestCase, FindElement, UserOperation, Waiting, AppOperation):
    """app启动时间测试类"""
    def start_and_get_date(self):
        """启动并获取启动时间"""
        app_start_time = ''
        date = os.popen('adb shell am start -W ' + pck_name + launchable_activity).readlines()
        for i in date:
            if 'TotalTime' in i:
                app_start_time = i.split(':')[1].strip()
                # print(app_start_time)
        return app_start_time

    def set_until_find_ad(self):
        """设置测试环境（拉取广告及信息流）"""
        try:
            self.set_app_status3()
        except selenium.common.exceptions.NoSuchElementException:
            print('未拉取到广告')
        self.force_stop()
        self.wait_for()
        self.home()
        self.wait_for(5)
        self.find_element('//*[@text="设置"]').click()
        self.wait_for()
        self.swipe_find_element('//*[@text="日期和时间"]')
        self.wait_for()
        try:
            self.find_element('//*[@text="设置日期"]').click()
        except Exception:
            self.find_elements('android:id/checkbox')[0].click()
        self.wait_for(1)
        self.find_element('//*[@text="设置日期"]').click()
        self.wait_for(1)
        self.find_elements('oppo:id/increment')[2].click()
        self.wait_for(1)
        self.find_elements('oppo:id/increment')[2].click()
        self.wait_for(1)
        self.find_elements('oppo:id/increment')[2].click()
        self.wait_for(1)
        self.find_element('android:id/button1').click()
        self.wait_for(1)
        self.home()
        self.wait_for(2)
        self.start_app()
        self.wait_explicit_ele('//*[@text="双开助手"]')
        if '关闭广告' and '双开资讯' in getinfo.get_xml():
            self.home()
            self.wait_for()

    def test_back(self):
        """back场景测试"""
        list_back = []
        # self.set_until_find_ad()
        self.back()
        time.sleep(2)
        while len(list_back) < 10:
            # time.sleep(5)
            start_time = self.start_and_get_date()
            if '关闭广告' or '双开资讯' in getinfo.get_xml():
                list_back.append(start_time)
            else:
                time.sleep(2)
            self.back()
            time.sleep(2)
        return list_back

    def test_home(self):
        """home场景测试"""
        list_home = []
        # self.set_until_find_ad()
        self.home()
        time.sleep(2)
        while len(list_home) < 10:
            # time.sleep(5)
            start_time = self.start_and_get_date()
            if '关闭广告' or '双开资讯' in getinfo.get_xml():
                list_home.append(start_time)
            else:
                time.sleep(2)
            self.home()
            time.sleep(2)
        return list_home

    def test_force(self):
        """home场景测试"""
        list_force = []
        # self.set_until_find_ad()
        self.force_stop()
        time.sleep(2)
        while len(list_force) < 10:
            # time.sleep(5)
            start_time = self.start_and_get_date()
            if '关闭广告' or '双开资讯' in getinfo.get_xml():
                list_force.append(start_time)
            else:
                time.sleep(2)
            self.force_stop()
            time.sleep(2)
        return list_force

    def run_test(self):
        list_back = self.test_back()
        self.wait_for(5)
        list_home = self.test_home()
        self.wait_for(5)
        list_force = self.test_force()
        self.wait_for(5)

        # 设置图像框架
        plt.figure(1)
        plt.title('启动时间测试报告')
        # 设置x轴刻度并替代默认值
        my_x_ticks = np.arange(1, 11, 1)
        plt.xticks(my_x_ticks)
        # 设置x，y轴的标签
        plt.xlabel('启动次数', fontsize=14, color='blue')
        plt.ylabel('启动时间（ms）', fontsize=14, color='blue')
        # 设置x，y轴以及作图使用的线的规格类型
        plt.subplot(311)
        plt.plot(list(range(1, 11)), list_back, 'ro')

        plt.subplot(312)
        plt.plot(list(range(1, 11)), list_home, 'go')

        plt.subplot(313)
        plt.plot(list(range(1, 11)), list_force, 'bo')
        plt.show()
        # plt.savefig('测试报告.png')


if __name__ == '__main__':
    appium = AppiumInit()
    appium.appium_init()

    test = StartTimeTest()
    test.run_test()
