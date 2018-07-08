from FunctionTest.func_script.func_lib import *
import matplotlib.pyplot as plt
import numpy as np

# 指定默认字体
plt.rcParams['font.sans-serif'] = ['KaiTi']
# 解决保存图像是负号'-'显示为方块的问题
plt.rcParams['axes.unicode_minus'] = False

pck_name = "com.excelliance.dualaid"
launchable_activity = "/com.excelliance.kxqp.ui.HelloActivity"


class StartTimeTest(FindElement, UserOperation, Waiting, AppOperation):
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
        self.wait_for(3)
        self.start_app()
        self.wait_for(5)
        self.back()
        self.wait_for(3)
        print('调试结束开始测试')
        while len(list_back) < 10:
            start_time = self.start_and_get_date()
            self.wait_explicit_ele('com.excelliance.dualaid:id/add_but', 15, 1)
            if '关闭广告' or '双开资讯' in getinfo.get_xml():
                list_back.append(start_time)
            self.back()
            time.sleep(2)
        return list_back

    def test_home(self):
        """home场景测试"""
        list_home = []
        # self.set_until_find_ad()
        self.start_app()
        self.wait_for(5)
        self.home()
        self.wait_for()
        self.start_app()
        self.wait_for(5)
        self.home()
        self.wait_for()
        print('调试结束开始测试')
        while len(list_home) < 10:
            start_time = self.start_and_get_date()
            self.wait_explicit_ele('com.excelliance.dualaid:id/ad_but', 15, 1)
            if '关闭广告' or '双开资讯' in getinfo.get_xml():
                list_home.append(start_time)
            self.home()
            time.sleep(2)
        return list_home

    def test_force(self):
        """冷启动场景测试"""
        list_force = []
        # self.set_until_find_ad()
        self.force_stop()
        self.wait_for(3)
        self.start_app()
        self.wait_for(5)
        self.force_stop()
        self.wait_for(3)
        print('调试结束开始测试')
        while len(list_force) < 10:
            start_time = self.start_and_get_date()
            self.wait_explicit_ele('com.excelliance.dualaid:id/ad_but', 15, 1)
            if '关闭广告' or '双开资讯' in getinfo.get_xml():
                list_force.append(start_time)
            self.force_stop()
            time.sleep(2)
        return list_force

    def run_test(self):
        list_back_new = self.test_back()
        self.wait_for(5)
        list_home_new = self.test_home()
        self.wait_for(5)
        list_force_new = self.test_force()
        self.wait_for(5)
        print('开始第二阶段测试')
        list_back_std = self.test_back()
        self.wait_for(5)
        list_home_std = self.test_home()
        self.wait_for(5)
        list_force_std = self.test_force()
        self.wait_for(5)

        # 数据排序
        list_back_new.sort()
        list_back_std.sort()
        list_home_new.sort()
        list_home_std.sort()
        list_force_new.sort()
        list_force_std.sort()

        # 设置图像框架
        plt.figure(1)
        # 设置x轴刻度并替代默认值
        # x = np.linspace(0, 10, 1)
        # my_x_ticks = np.arange(1, 11, 1)
        # plt.xticks(my_x_ticks)
        # 设置x，y轴的标签
        plt.xlabel('启动次数', fontsize=14, color='blue')
        plt.ylabel('启动时间（ms）', fontsize=14, color='blue')
        # 设置图片标题
        # plt.title('启动时间测试报告', fontsize=16, color='green')
        # 设置x，y轴、图例以及作图使用的线的规格类型
        plt.subplot(221)  # 设置子图
        plt.title('场景一：back')
        plt.plot(list(range(1, 11)), list_back_new, 'r', label='back')
        plt.plot(list(range(1, 11)), list_back_std, 'g--', label='back')
        # 显示图例（不加的话，设置的label图例不会显示）
        plt.legend()

        plt.subplot(222)
        plt.title('场景二：home')
        plt.plot(list(range(1, 11)), list_home_new, 'r', label='home')
        plt.plot(list(range(1, 11)), list_home_std, 'g--', label='home')
        plt.legend()

        plt.subplot(223)
        plt.title('场景三：冷启动')
        plt.plot(list(range(1, 11)), list_force_new, 'r', label='冷启动')
        plt.plot(list(range(1, 11)), list_force_std, 'g--', label='冷启动')
        plt.legend()
        # 显示图片
        # plt.show()
        # 保存图片
        plt.savefig(os.path.join(BASE_PATH, 'test_result1\start_time_report\启动时间测试报告%s.png' % getinfo.get_time()))


if __name__ == '__main__':
    appium = AppiumInit()
    appium.appium_init()

    test = StartTimeTest()
    test.run_test()
