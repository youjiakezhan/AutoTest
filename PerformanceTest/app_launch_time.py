import re
import sys
import threading
import time

import numpy as np
import uiautomator2
from matplotlib import pyplot as plt

from AutoTest.myfunction.matplotlib_setting import matplot_init
from AutoTest.myfunction.send_email import SendEmail
from AutoTest.performancetest.comman import *

__doc__ = """
    脚本功能:
            检测指定目录下是否有apk文件,有的话自动执行安装过程(自动安装仅限oppoR7),如果没有则继续等待直到apk文件出现;
            安装后调出广告和信息流,然后执行back,home,冷启动的时间测试;
            首轮测试结束后卸载apk,安装比对版本的apk进行第二轮测试;
            测试完毕后收集测试数据输出图形报告;
            测试报告邮件发送;
    测试环境:
            测试前请确保手机内至少装有一款热门应用(如微信等);
"""


# 手机测试环境设置
class ForwardSetting(object):

    def __init__(self, apk_path, style='apk', phone='oppoR7'):
        self.pkg_name = pkg_name
        self.activity = activity
        self.apk_path = apk_path
        self.style = style
        self.phone = phone

    @staticmethod
    def check_adb_connect():
        """查看USB是否已连接"""
        if 'device' in os.popen('adb devices').readlines()[1]:
            print('USB已连接')
            return True
        else:
            print('USB未连接')
            return False

    def get_file_path(self):
        """获取安装包路径"""
        file_list = os.listdir(self.apk_path)
        for file in file_list:
            if self.style in file:
                file_path = os.path.join(self.apk_path, file)
                os.rename(file_path, file_path.replace(' ', ''))
                time.sleep(1)
                return file_path

    def uninstall_apk(self):
        """卸载本机已有双开助手apk"""
        try:
            os.popen('adb uninstall com.excelliance.dualaid')
        except Exception:
            print('本机未安装双开助手')

    def install_apk(self):
        """安装daily review包"""
        os.popen('adb install -r ' + self.get_file_path())
        d.screen_on()
        if self.phone == 'oppoR7':
            while True:
                try:
                    if d(resourceId="com.android.packageinstaller:id/apk_info_view").exists(15) is True:
                        time.sleep(1)
                        d(text="继续安装").click(timeout=10)
                        time.sleep(1)
                        d(text="安装").click(timeout=3)
                        time.sleep(1)
                        d(text="完成").click(timeout=3)
                        print('apk安装完成')
                        # 获取apk的版本号
                        app_version = os.popen(
                            'adb shell pm dump com.excelliance.dualaid | findstr "versionName"').read().replace(
                            'versionName=', '').strip()
                        print('版本号：%s' % app_version)
                        return app_version
                    else:
                        time.sleep(2)
                except uiautomator2.UiObjectNotFoundError:
                    print('apk安装失败，正在尝试重新安装')

    def install_control(self):
        self.uninstall_apk()
        time.sleep(2)
        app_version = self.install_apk()
        print('开始配置测试环境')
        return app_version

    def monitor(self):
        while True:
            if self.get_file_path() is not None:
                print('检测到apk安装包，准备测试...')
                break
            else:
                print('未检测到双开助手安装包\n本次检测时间：%s' % time.strftime('%Y.%m.%d_%H:%M:%S'))
                time.sleep(5)


# 线程创建/结束
class CreateThread(object):

    def start_thread(self, func):
        """开启一条执行func函数的新线程"""
        global alert_flag
        alert_flag = 1
        thread = threading.Thread(target=func)
        thread.start()

    def stop_thread(self):
        global alert_flag
        alert_flag = 0
        while True:
            if threading.active_count() > 1:
                time.sleep(1)
            else:
                break


# 弹窗监控处理
class SuperVision(object):

    def update_alert(self):
        """监控并处理应用安装弹窗"""
        print('监控1已启动')
        while True:
            if alert_flag == 1:
                try:
                    if d(resourceId='com.excelliance.dualaid:id/ll_dialog').exists(10):
                        print('检测到apk更新提示，正在处理...')
                        d(resourceId='com.excelliance.dualaid:id/cb_noToast').click(timeout=5)
                        d(resourceId='com.excelliance.dualaid:id/tv_left').click(timeout=5)
                        print('已忽略apk更新')
                except Exception:
                    continue
            else:
                print('监控1已停止')
                break

    def pemission_alert(self):
        print('监控2已启动')
        while True:
            if alert_flag == 1:
                try:
                    if d(resourceId='oppo:id/permission_prompt').exists(10):
                        print('检测到apk权限弹窗，正在处理...')
                        d(text='不再提醒').click(timeout=5)
                        d(text='允许').click(timeout=5)
                        print('已同意apk获取权限')
                except Exception:
                    continue
            else:
                print('监控2已停止')
                break


# app启动时间测试类
class StartTimeTest(object):

    def __init__(self, phone='oppoR7'):
        self.phone = phone
        self.list_back_test = []
        self.list_home_test = []
        self.list_force_test = []
        self.list_back_std = []
        self.list_home_std = []
        self.list_force_std = []

    # 计算列表的中位数
    def list_middle(self, lists):
        lists.sort()
        half = len(lists) // 2
        return (lists[half] + lists[~half]) / 2

    # 计算列表的差值
    def diff_value(self, list1, list2):
        import numpy as np
        return list(np.array(list1) - np.array(list2))

    # 启动并获取启动时间
    def start_and_get_date(self):
        # 正则匹配方式获取
        time_data = os.popen('adb shell am start -W ' + pkg_name + '/' + activity)
        b = re.search(r'(TotalTime:)\s(\d+)', time_data.read())
        app_start_time = int(b.group(2))
        return app_start_time
        # # 循环方式获取
        # time_data = os.popen('adb shell am start -W ' + pkg_name + '/' + activity).readlines()
        # for i in time_data:
        #     if 'TotalTime' in i:
        #         app_start_time = i.split(':')[path].strip()
        #         return int(app_start_time)

    # 设置手机（oppoR7/honor9）系统时间
    def set_phone_time(self, kind='normal'):
        while True:
            if self.phone == 'oppoR7':
                try:
                    if kind == 'normal':
                        print('正在设置手机时间')
                        d.app_stop(pkg_name)
                        time.sleep(1)
                        d.press('home')
                        time.sleep(1)
                        d.press('home')
                        time.sleep(1)
                        d(text='设置').click()
                        time.sleep(1)
                        d(scrollable=True).fling()
                        time.sleep(2)
                        d(text='日期和时间').click(timeout=5)
                        time.sleep(1)
                        if d(text='设置日期').info['enabled'] is False:
                            d(resourceId='android:id/checkbox')[0].click(timeout=5)
                            time.sleep(1)
                            d(text='设置日期').click(timeout=5)
                            time.sleep(1)
                            d(resourceId='oppo:id/increment')[1].click(timeout=5)
                            time.sleep(1)
                            d(resourceId='android:id/button1').click(timeout=5)
                            time.sleep(1)
                        else:
                            d(text='设置日期').click(timeout=5)
                            time.sleep(1)
                            d(resourceId='oppo:id/increment')[1].click(timeout=5)
                            time.sleep(1)
                            d(resourceId='android:id/button1').click(timeout=5)
                            time.sleep(1)
                        d.press('home')
                        time.sleep(2)
                        d.app_start(pkg_name)
                        d(resourceId='com.excelliance.dualaid:id/add_but').exists(10)
                        d.press('back')
                        time.sleep(2)
                        d.app_start(pkg_name)
                        d(resourceId='com.excelliance.dualaid:id/add_but').exists(10)
                        break
                    elif kind == 'recovery':
                        print('正在恢复手机时间')
                        d.press('home')
                        time.sleep(1)
                        d.press('home')
                        time.sleep(1)
                        d(text='设置').click(timeout=5)
                        time.sleep(1)
                        d(scrollable=True).fling()
                        time.sleep(2)
                        d(text='日期和时间').click(timeout=5)
                        time.sleep(1)
                        if d(text='设置日期').info['enabled'] is True:
                            time.sleep(1)
                            d(resourceId='android:id/checkbox')[0].click(timeout=5)
                            time.sleep(1)
                            d.press('home')
                            time.sleep(2)
                            d.app_start(pkg_name)
                            d(resourceId='com.excelliance.dualaid:id/add_but').exists(10)
                            d.press('back')
                            time.sleep(2)
                            d.app_start(pkg_name)
                            d(resourceId='com.excelliance.dualaid:id/add_but').exists(10)
                            print('手机时间已恢复至当前时间')
                            break
                        else:
                            d.press('home')
                            time.sleep(2)
                            d.app_start(pkg_name)
                            d(resourceId='com.excelliance.dualaid:id/add_but').exists(10)
                            d.press('back')
                            time.sleep(2)
                            d.app_start(pkg_name)
                            d(resourceId='com.excelliance.dualaid:id/add_but').exists(10)
                            print('手机时间已经为当前时间')
                            break
                except uiautomator2.UiObjectNotFoundError:
                    continue
            elif self.phone == 'honor9':
                try:
                    if kind == 'normal':
                        print('正在设置手机时间')
                        d.app_stop(pkg_name)
                        time.sleep(1)
                        d.press('home')
                        time.sleep(1)
                        d.press('home')
                        time.sleep(1)
                        d(text='设置').click()
                        time.sleep(1)
                        d(scrollable=True).fling()
                        time.sleep(2)
                        d(text='系统').click(timeout=5)
                        d(text='日期和时间').click(timeout=5)
                        time.sleep(1)
                        if d(text="日期").info['enabled'] is False:
                            d(resourceId="android:id/switch_widget").click(timeout=5)
                            time.sleep(1)
                            d(text='日期').click(timeout=5)
                            time.sleep(1)
                            d.click(800, 1500)
                            time.sleep(0.5)
                            d.click(800, 1500)
                            time.sleep(0.5)
                            d.click(800, 1500)
                            time.sleep(1)
                            d(text='确定').click(timeout=5)
                            time.sleep(1)
                        else:
                            d(text='日期').click(timeout=5)
                            time.sleep(1)
                            d(800, 1500).click(timeout=3)
                            d(800, 1500).click(timeout=3)
                            d(800, 1500).click(timeout=3)
                            time.sleep(1)
                            d(text='确定').click(timeout=5)
                            time.sleep(1)
                        d.press('home')
                        time.sleep(2)
                        d.app_start(pkg_name)
                        d(resourceId='com.excelliance.dualaid:id/add_but').exists(10)
                        d.press('back')
                        time.sleep(2)
                        d.app_start(pkg_name)
                        d(resourceId='com.excelliance.dualaid:id/add_but').exists(10)
                        break
                    elif kind == 'recovery':
                        print('正在恢复手机时间')
                        d.press('home')
                        time.sleep(1)
                        d.press('home')
                        time.sleep(1)
                        d(text='设置').click(timeout=5)
                        time.sleep(1)
                        d(scrollable=True).fling()
                        time.sleep(2)
                        d(text='系统').click(timeout=5)
                        time.sleep(1)
                        if d(text='日期').info['enabled'] is True:
                            time.sleep(1)
                            d(resourceId="android:id/switch_widget").click(timeout=5)
                            time.sleep(1)
                            d.press('home')
                            time.sleep(2)
                            d.app_start(pkg_name)
                            d(resourceId='com.excelliance.dualaid:id/add_but').exists(10)
                            d.press('back')
                            time.sleep(2)
                            d.app_start(pkg_name)
                            d(resourceId='com.excelliance.dualaid:id/add_but').exists(10)
                            print('手机时间已恢复至当前时间')
                            break
                        else:
                            d.press('home')
                            time.sleep(2)
                            d.app_start(pkg_name)
                            d(resourceId='com.excelliance.dualaid:id/add_but').exists(10)
                            d.press('back')
                            time.sleep(2)
                            d.app_start(pkg_name)
                            d(resourceId='com.excelliance.dualaid:id/add_but').exists(10)
                            print('手机时间已经为当前时间')
                            break
                except uiautomator2.UiObjectNotFoundError:
                    continue

    # 设置app到指定状态，拉出banner和icon广告
    def set_app_status(self):
        """启动APP至状态（有banner，icon，无信息流，无钻石按钮的主界面）"""

        def set_step():
            d(text=u'点击加号，添加双开应用').exists(5)
            d(scrollable=True).fling.horiz.forward(100)
            d(scrollable=True).fling.horiz.forward(100)
            d(text='开始体验').click(timeout=5)
            d(text='跳过').click_exists(5)
            d(resourceId='com.excelliance.dualaid:id/tv_bt_add').exists(10)
            d.press('back')
            time.sleep(2)
            d.press('back')
            time.sleep(2)
            d.app_start(pkg_name)
            time.sleep(1)
            d.press('back')
            time.sleep(2)
            d.app_start(pkg_name)

        try:
            set_step()
        except Exception:
            d.app_clear(pkg_name)
            time.sleep(3)
            set_step()
        print('正在检测非标位')
        d(resourceId="com.excelliance.dualaid:id/add_but").exists(5)
        time.sleep(5)
        if d(resourceId='com.excelliance.dualaid:id/fl_off_standard_position').exists(5):
            print('拉取到非标位版本，重新拉取')
            d.app_clear(pkg_name)
            time.sleep(3)
            d.app_start(pkg_name)
            self.set_app_status()
        i = 1
        while i <= 10:
            try:
                if d(resourceId="com.excelliance.dualaid:id/iv_ad_alimama").exists(3) is False and d(
                        resourceId="com.excelliance.dualaid:id/ad_but").exists(3) is False:
                    print("广告拉取失败%d次" % i)
                    if i == 3:
                        print('尝试设置手机时间后拉取')
                        self.set_phone_time()
                        if d(resourceId="com.excelliance.dualaid:id/iv_ad_alimama").exists(3) is True or d(
                                resourceId="com.excelliance.dualaid:id/ad_but").exists(3) is True:
                            print('广告拉取成功')
                            break
                    elif i == 5:
                        print('尝试恢复手机时间后拉取')
                        self.set_phone_time('recovery')
                        if d(resourceId="com.excelliance.dualaid:id/iv_ad_alimama").exists(3) is True or d(
                                resourceId="com.excelliance.dualaid:id/ad_but").exists(3) is True:
                            print('广告拉取成功')
                            break
                    elif i == 10:
                        print('测试失败，广告拉取部分可能有问题')
                        global email_content_flag
                        email_content_flag = 2
                        em = SendEmail('wangzhongchang@excelliance.cn', 'wzc6851498')
                        em.create_email(t)
                        time.sleep(5)
                        print('系统正在退出...')
                        thread.stop_thread()
                        sys.exit()
                    else:
                        d.press('back')
                        time.sleep(2)
                        d.app_start(pkg_name)
                else:
                    print('广告拉取成功')
                    break
            except Exception:
                continue
            i += 1

    # 设置测试环境（拉取信息流）
    def set_until_find_ad(self):
        d.app_start(pkg_name)
        time.sleep(2)
        try:
            self.set_app_status()
            if d(text='跳过').exists(5) is True:
                d(text='跳过').click(timeout=5)
            if d(resourceId='com.excelliance.dualaid:id/iv_close').exists(5):
                d(resourceId='com.excelliance.dualaid:id/iv_close').click(timeout=5)
                print('关闭banner上部提示成功')
        except uiautomator2.UiObjectNotFoundError:
            print('关闭banner上部提示失败')
        time.sleep(2)
        # 添加微信
        print('正在添加微信')
        try:
            d(text="微信").click()
        except uiautomator2.UiObjectNotFoundError:
            time.sleep(5)
            d(text="微信").click()
        if d(resourceId='com.excelliance.dualaid:id/tv_app_add').exists(10) is True:
            print('微信添加成功')
            d.press('back')
        else:
            print('微信添加失败')
        # 调出信息流
        if d(resourceId='com.excelliance.dualaid:id/tv_title').exists(10) is not True:
            self.set_phone_time()
            i = 1
            while i <= 10:
                print('第%s次拉取信息流' % i)
                d(resourceId='com.excelliance.dualaid:id/add_btn').exists(10)
                if d(resourceId='com.excelliance.dualaid:id/tv_title').exists(10) is True:
                    d.press('back')
                    print('信息流拉取成功，开始进行调试')
                    time.sleep(2)
                    break
                elif d(text='双开资讯').exists(10) is True:
                    d.press('back')
                    print('信息流拉取成功，开始进行调试')
                    time.sleep(2)
                    break
                elif d(text='今日热点').exists(10) is True:
                    d.press('back')
                    print('信息流拉取成功，开始进行调试')
                    time.sleep(2)
                    break
                else:
                    print('拉取信息流失败，尝试重新拉取')
                    # 3次拉取失败的话，恢复系统时间再试
                    if i == 3:
                        self.set_phone_time(kind='recovery')
                    # 6次拉取失败的话，恢复系统时间再试
                    elif i == 6:
                        self.set_phone_time(kind='recovery')
                    # 10次拉取不到的话，邮件通知拉取不到信息流
                    elif i == 10:
                        global email_content_flag
                        email_content_flag = 3
                        em = SendEmail('wangzhongchang@excelliance.cn', 'wzc6851498', state='debug')
                        em.create_email(mail_content)
                        time.sleep(5)
                        print('系统正在退出...')
                        sys.exit()
                    else:
                        self.set_phone_time(kind='normal')
                i += 1
        else:
            print('信息流已存在，开始进行调试')

    # 各场景测试前调试
    def set(self, state):
        i = 0
        d.app_stop(pkg_name)
        while i < 3:
            time.sleep(t)
            d.app_start(pkg_name)
            d(resourceId='com.excelliance.dualaid:id/tv_title').exists(10)
            if state == 'force_stop':
                d.app_stop(pkg_name)
            else:
                d.press(state)
            time.sleep(t)
            i += 1

    # back场景测试
    def test_back(self, t, n):
        list_back = []
        self.set('back')
        print('调试结束，测试开始\n场景一：back')
        while len(list_back) < n:
            start_time = self.start_and_get_date()
            if d(resourceId='com.excelliance.dualaid:id/tv_title').exists(5) is True and 0 < start_time < 500:
                list_back.append(start_time)
            elif d(text='双开资讯').exists(3) is True and 0 < start_time < 500:
                list_back.append(start_time)
            elif d(text='今日热点').exists(3) is True and 0 < start_time < 500:
                list_back.append(start_time)
            d.press('back')
            time.sleep(t)
        # 去掉一个最大值和一个最小值
        list_back.remove(max(list_back))
        list_back.remove(min(list_back))
        print(round(sum(list_back) / len(list_back), 1))
        # print(self.list_middle(list_back))
        return list_back

    # home场景测试
    def test_home(self, t, n):
        list_home = []
        self.set('home')
        print('调试结束，测试开始\n场景二：home')
        i = 0
        while len(list_home) < n:
            i += 1
            start_time = self.start_and_get_date()
            if d(resourceId='com.excelliance.dualaid:id/tv_title').exists(10) is True and 0 < start_time < 500:
                list_home.append(start_time)
            elif d(text='双开资讯').exists(3) is True and 0 < start_time < 500:
                list_home.append(start_time)
            elif d(text='今日热点').exists(3) is True and 0 < start_time < 500:
                list_home.append(start_time)
            elif i > 5:
                d.app_stop(pkg_name)
                time.sleep(2)
                d.app_start(pkg_name)
                time.sleep(5)
            d.press('home')
            time.sleep(t)
        # 去掉一个最大值和一个最小值
        list_home.remove(max(list_home))
        list_home.remove(min(list_home))
        print(round(sum(list_home) / len(list_home), 1))
        # print(self.list_middle(list_home))
        return list_home

    # 冷启动场景测试
    def test_force(self, t, n):
        list_force = []
        self.set('force_stop')
        print('调试结束，测试开始\n场景三：冷启动')
        while len(list_force) < n:
            start_time = self.start_and_get_date()
            if d(resourceId='com.excelliance.dualaid:id/tv_title').exists(10) is True and 0 < start_time:
                list_force.append(start_time)
            elif d(text='双开资讯').exists(3) is True and 0 < start_time:
                list_force.append(start_time)
            elif d(text='今日热点').exists(3) is True and 0 < start_time:
                list_force.append(start_time)
            d.app_stop(pkg_name)
            time.sleep(t)
        # 去掉一个最大值和一个最小值
        list_force.remove(max(list_force))
        list_force.remove(min(list_force))
        print(round(sum(list_force) / len(list_force), 1))
        # print(self.list_middle(list_force))
        return list_force

    # 启动并收集测试数据（3.0.6版本）
    def test_and_get_data1(self, t, n):
        # 将app调试到可测环境(调出广告和信息流)
        self.set_until_find_ad()
        d.app_start(pkg_name)
        time.sleep(2)
        # 停止监控线程
        new_thread.stop_thread()
        time.sleep(5)
        # 开始场景一测试
        self.list_back_std = self.test_back(t, n)
        time.sleep(2)
        # 开始场景二测试
        self.list_home_std = self.test_home(t, n)
        time.sleep(2)
        # 开始场景三测试
        self.list_force_std = self.test_force(t, n)
        time.sleep(2)

    # 启动并收集测试数据（新版本）
    def test_and_get_data2(self, t, n):
        # 将app调试到可测环境(调出广告和信息流)
        self.set_until_find_ad()
        d.app_start(pkg_name)
        time.sleep(2)
        # 停止监控线程
        new_thread.stop_thread()
        time.sleep(5)
        # 开始场景一测试
        self.list_back_test = self.test_back(t, n)
        time.sleep(2)
        # 开始场景二测试
        self.list_home_test = self.test_home(t, n)
        time.sleep(2)
        # 开始场景三测试
        self.list_force_test = self.test_force(t, n)
        time.sleep(2)

    def part_one(self, t, n):
        # 开启监控线程
        new_thread.start_thread(alert.update_alert)
        new_thread.start_thread(alert.pemission_alert)
        # 安装比对版本(3.0.6)
        install_old = ForwardSetting(r'Z:\start_time_SKZS\start_time_files\apk', style='3.0.6')
        install_old.install_control()
        time.sleep(2)
        print('阶段一：3.0.6版本测试')
        self.test_and_get_data1(t, n)
        global restart_flag
        restart_flag = 0

    def part_two(self, t, n):
        # 开启监控线程
        new_thread.start_thread(alert.update_alert)
        new_thread.start_thread(alert.pemission_alert)
        # 安装新版本
        install_new = ForwardSetting(r'Z:\start_time_SKZS', style='apk')
        try:
            global new_app_version
            new_app_version = install_new.install_control()
            # 保存本次测试apk
            os.popen('move ' + install_new.get_file_path() + r' Z:\start_time_SKZS\start_time_files\apk')
        except FileNotFoundError:
            print('未连接到公盘')
            new_thread.stop_thread()
            print('正在退出系统...')
            sys.exit()
        print('阶段二：新版本测试')
        self.test_and_get_data2(t, n)

    def create_image(self, save_path, sample):
        # 解决matplotlib显示中文问题
        matplot_init()
        plt.figure(dpi=140)
        plt.title('新老版本均值差走势图')
        plt.xlabel('样本数(%d组)' % sample)
        plt.ylabel('均值差(ms)')
        y_ticks = np.arange(-50, 150, 10)
        plt.yticks(y_ticks)
        plt.plot(image_list1, 'r', label='back')
        plt.plot(image_list2, 'g', label='home')
        plt.plot(image_list3, 'b', label='force')
        plt.legend()
        plt.grid(color='skyblue')
        plt.savefig(save_path + '\\time_image\\%s.png' % time.strftime('%Y%m%d%H%M%S'))

    # 数据收集和处理
    def data_handle(self):
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

        # 收集数据用于生成图表
        global image_list1, image_list2, image_list3
        image_list1 = self.diff_value(self.list_back_test, self.list_back_std)
        image_list2 = self.diff_value(self.list_home_test, self.list_home_std)
        image_list3 = self.diff_value(self.list_force_test, self.list_force_std)
        print(image_list1)
        print(image_list2)
        print(image_list3)

        # 定义邮件正文内容
        global mail_content
        if email_content_flag == 1:
            mail_content = """
<html>
<body>
<div>
    <h2>双开助手性能测试：启动时间测试</h2>
    <p>测试数据单位均为毫秒（ms）</p>
    <div id="content">
        <table border="path" bordercolor="#87ceeb" width="800">
            <tr>
                <td><strong>版本号</strong></td>
                <td><strong>back(avg)</strong></td>
                <td><strong>back(max)</strong></td>
                <td><strong>home(avg)</strong></td>
                <td><strong>home(max)</strong></td>
                <td><strong>冷启动(avg)</strong></td>
                <td><strong>冷启动(max)</strong></td>
            </tr>
            <tr>
                <td>%s</td>
                <td>%d</td>
                <td>%d</td>
                <td>%d</td>
                <td>%d</td>
                <td>%d</td>
                <td>%d</td>
            </tr>
            <tr>
                <td>3.0.6</td>
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
                <td bgcolor="#87ceeb"></td>
                <td>%d</td>
                <td bgcolor="#87ceeb"></td>
                <td>%d</td>
                <td bgcolor="#87ceeb"></td>
            </tr>
        </table>
    </div>
</div>
</body>
</html>
                """ % \
                           (new_app_version, data_dict['新版back均值'], data_dict['新版back最大值'], data_dict['新版home均值'],
                            data_dict['新版home最大值'], data_dict['新版force均值'], data_dict['新版force最大值'],
                            data_dict['老版back均值'], data_dict['老版back最大值'], data_dict['老版home均值'],
                            data_dict['老版home最大值'], data_dict['老版force均值'], data_dict['老版force最大值'],
                            data_dict['back差值'], data_dict['home差值'], data_dict['force差值']
                            )
        elif email_content_flag == 2:
            mail_content = """
                            <html>
                            <body>
                            <h2>启动时间测试失败<h2>
                            <p>失败原因：10次拉取banner和icon广告失败，该模块可能存在问题（已尝试往前和往后调节手机时间再拉取）</p>
                            </body>
                            </html>
                            """
        elif email_content_flag == 3:
            mail_content = """
                            <html>
                            <body>
                            <h2>启动时间测试失败<h2>
                            <p>失败原因：10次拉取信息流失败，该模块可能存在问题（已尝试往前和往后调节手机时间再拉取）</p>
                            </body>
                            </html>
                            """

    # 启动测试入口
    def run_test(self, t, n):
        # 新包监控
        apk_monitor = ForwardSetting(r'Z:\start_time_SKZS', style='apk')
        try:
            apk_monitor.monitor()
        except FileNotFoundError:
            print('公盘未连接，正在退出系统')
            sys.exit()
        # 初始化弹窗监控线程
        global new_thread, alert
        alert = SuperVision()
        new_thread = CreateThread()
        while True:
            try:
                self.part_one(t, n)
                print('阶段一测试完成')
                break
            except Exception:
                print('阶段一测试出错，重新开始测试')
                self.test_and_get_data1(t, n)
        while True:
            try:
                self.part_two(t, n)
                print('阶段二测试完成')
                break
            except Exception:
                print('阶段二测试出错，重新开始测试')
                self.test_and_get_data2(t, n)
        # 数据处理和报告生成
        self.data_handle()


def run_start_time(state, n=22):
    global thread, t, email_content_flag, alert_flag
    path = os.path.abspath(os.path.dirname('__file__'))
    thread = CreateThread()
    test = StartTimeTest()
    e = SendEmail('wangzhongchang@excelliance.cn', 'wzc6851498', state, image_path=path + '\\time_image')
    email_content_flag = 1
    alert_flag = 1
    while True:
        if ForwardSetting.check_adb_connect() is True:
            # 设置app启动的时间间隔
            t = 1
            test.run_test(t, n)
            test.create_image(path, n)
            e.create_email(mail_content)
            print('启动时间模块测试结束，准备开始测试cpu/内存模块')
            break
        else:
            print('系统正在退出')
            thread.stop_thread()
            sys.exit()


if __name__ == '__main__':
    run_start_time(state='debug')
