# coding=utf-8
import os
import threading
import time

import matplotlib.pyplot as plt
import uiautomator2 as u2

from myfunction.send_email import SendEmail

"""
功能概述：
    1.环境设置完成后脚本将执行各个测试场景的用例；
    2.用例执行期间会定期获取性能相关数据并保存；
    3.测试结束后将得到的性能相关数据进行处理；
    4.将处理后的数据生成图表并以邮件形式通知；
环境设置：
    1.安装新版双开助手apk；
    2.调出广告和信息流；
    3.第一空间内添加微信（不登录）；
"""
# 内存监控开始标志位
monitor_start_flag = 1
# 内存数据存放列表
mast = []
lbcore = []
lebian = []
cpu_data = []


# 初始化uiautomator2
def __init__():
    global d
    # 初始化uiautomator2
    d = u2.connect()
    # 启动uiautomator2的守护进程
    d.healthcheck()
    return d


# 创建、启动和停止线程
class CreateThread(object):
    def new_thread(self, func, args):
        global monitor_start_flag
        monitor_start_flag = 1
        # 另起一条线程执行meminfo和cpuinfo方法
        thread = threading.Thread(target=func, args=(args,))
        thread.start()

    def stop_thread(self):
        global monitor_start_flag
        monitor_start_flag = 0


# 测试场景
class Case(object):

    def __init__(self, pck, activity):
        self.pck = pck
        self.activity = activity

    # 测试场景一：主界面点击个人中心跳转至二级页面
    def test01(self, num):
        # 测试环境配置
        d.press('back')
        d.press('home')
        time.sleep(1)
        d.app_start(self.pck)
        while True:
            if d(resourceId='com.excelliance.dualaid:id/iv_icon').exists(5) is True:
                break
            else:
                time.sleep(2)
        # 测试场景循环，次数为num
        i = 0
        while i < num:
            try:
                d(resourceId='com.excelliance.dualaid:id/iv_icon').click(timeout=2)
                d(resourceId='com.excelliance.dualaid:id/iv_back').click(timeout=2)
                i += 1
            except u2.UiObjectNotFoundError:
                print('未找到控件')
                d.press('back')
                continue

    # 测试场景二：主界面点击添加按钮
    def test02(self, num):
        # 测试环境配置
        d.press('back')
        d.press('home')
        time.sleep(1)
        d.app_start(self.pck)
        while True:
            if d(resourceId='com.excelliance.dualaid:id/iv_icon').exists(5) is True:
                break
            else:
                time.sleep(2)
        # 测试场景循环，次数为num
        i = 0
        while i < num:
            try:
                d(resourceId="com.excelliance.dualaid:id/add_but").click(timeout=2)
                d(resourceId="com.excelliance.dualaid:id/iv_back").click(timeout=2)
                i += 1
            except u2.UiObjectNotFoundError:
                print('未找到控件')
                d.press('back')
                continue

    # 测试场景三：主界面启动微信
    def test03(self, num):
        # 测试环境配置
        d.press('back')
        d.press('home')
        time.sleep(1)
        d.app_start(self.pck)
        while True:
            if d(resourceId='com.excelliance.dualaid:id/iv_icon').exists(5) is True:
                break
            else:
                time.sleep(2)
        # 首次冷启动微信单独处理
        d(resourceId="com.excelliance.dualaid:id/item_app_name", text=u"微信").click()
        time.sleep(5)
        d.press('back')
        time.sleep(1)
        # 测试场景循环，次数为num
        i = 1  # 循环次数减少1
        while i < num:
            try:
                d(resourceId="com.excelliance.dualaid:id/item_app_name", text=u"微信").click()
                time.sleep(1)
                d.press('back')
                time.sleep(1)
                i += 1
            except u2.UiObjectNotFoundError:
                print('未找到控件')
                d.press('back')
                continue

    # 测试场景四：主界面back再进
    def test04(self, num):
        # 测试环境配置
        d.press('back')
        d.press('home')
        time.sleep(1)
        d.app_start(self.pck)
        while True:
            if d(resourceId='com.excelliance.dualaid:id/iv_icon').exists(5) is True:
                break
            else:
                time.sleep(2)
        # 测试场景循环，次数为num
        i = 1
        while i < num:
            try:
                d.press('back')
                time.sleep(1)
                d.app_start(self.pck)
                time.sleep(3)
                i += 1
            except u2.UiObjectNotFoundError:
                print('未找到控件')
                d.press('back')
                continue

    # 测试场景五：主界面force-stop再进
    def test05(self, num):
        # 测试环境配置
        d.press('back')
        d.press('home')
        time.sleep(1)
        d.app_start(self.pck)
        while True:
            if d(resourceId='com.excelliance.dualaid:id/iv_icon').exists(5) is True:
                break
            else:
                time.sleep(2)
        # 测试场景循环，次数为num
        i = 1
        while i < num:
            try:
                d.app_stop(self.pck)
                time.sleep(2)
                d.app_start(self.pck)
                time.sleep(3)
                i += 1
            except u2.UiObjectNotFoundError:
                print('未找到控件')
                d.press('back')
                continue


# 数据获取
class GetData(object):
    def meminfo(self, pck):
        global monitor_start_flag, mast, lbcore, lebian
        print('memory监控开启')
        while True:
            if monitor_start_flag == 1:
                try:
                    datas = os.popen('adb shell dumpsys meminfo | findstr ' + pck).readlines()
                    for data in datas[0:int(len(datas) / 2)]:
                        if 'activities' in data:
                            mast.append(round(int(data.split()[0]) / 1024))
                        elif 'lbcore' in data:
                            lbcore.append(round(int(data.split()[0]) / 1024))
                        elif 'lebian' in data:
                            lebian.append(round(int(data.split()[0]) / 1024))
                        if len(mast) > len(lbcore):
                            lbcore.append(0)
                        if len(mast) > len(lebian):
                            lebian.append(0)
                except UnboundLocalError:
                    print('未检测到双开进程')
                    continue
            else:
                print('memory监控关闭')
                break

    def cpuinfo(self, pck):
        global cpu_data
        cpu = []
        print('cpu监控开启')
        while True:
            if monitor_start_flag == 1:
                try:
                    datas = os.popen('adb shell dumpsys cpuinfo | findstr ' + pck)
                    for data in datas:
                        if '%' in data:
                            cpu.append(data.split()[0].replace('%', ''))
                        else:
                            cpu.append(0)
                    cpu_data.append(round(sum(list(float(i) for i in cpu))))
                    cpu = []
                    time.sleep(1)
                except UnboundLocalError:
                    print('未检测到双开进程')
                    continue
            else:
                print('cpu监控关闭')
                break


# 处理数据
class DataOperate(object):
    def __init__(self):
        # 解决matplotlib显示中文问题
        plt.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
        plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

    # 数据可视化
    def create_picture(self, path):
        fig = plt.figure()
        fig.add_subplot(221)
        plt.plot(mast, 'purple', label='主进程')
        plt.legend()
        plt.grid()
        fig.add_subplot(222)
        plt.plot(lbcore, 'g', label='lbcore')
        plt.legend()
        plt.grid()
        fig.add_subplot(223)
        plt.plot(lebian, 'b', label='lebian')
        plt.legend()
        plt.grid()
        fig.add_subplot(224)
        plt.plot(cpu_data, 'r', label='cpu')
        plt.legend()
        plt.grid()
        plt.savefig(path + '\\%s.png' % time.strftime('%Y%m%d%H%M%S'))


def run(path, num=10):
    __init__()
    pck = 'com.excelliance.dualaid'
    activity = 'com.excelliance.xkqp.ui.HelloActivity'
    case = Case(pck, activity)
    data = GetData()
    data_opr = DataOperate()
    create_thread = CreateThread()

    # 执行测试
    # 开启监控线程（开始获取数据）
    create_thread.new_thread(data.cpuinfo, pck)
    create_thread.new_thread(data.meminfo, pck)

    # 执行测试用例
    case.test01(num)
    case.test02(num)
    case.test03(num)
    case.test04(num)
    case.test05(num)

    # 停止监控线程（暂停获取数据）
    create_thread.stop_thread()

    # 根据当前获取的数据生成图表
    data_opr.create_picture(path)

    # 关闭uiautomator2的守护进程
    d.service("uiautomator").stop()


if __name__ == "__main__":
    result_path = os.path.abspath(os.path.dirname('__file__'))
    sendemail = SendEmail('wangzhongchang@excelliance.cn', 'wzc6851498', image_path=result_path)
    while True:
        try:
            run(result_path, int(input('输入各个场景的循环次数：')))    # 输入场景循环次数
            # run(result_path)                                          # 默认循环次数（10次）
            break
        except Exception:
            continue
    sendemail.create_email('双开助手性能测试：内存/cpu测试结果')
    print(len(mast), len(lbcore), len(lebian), len(cpu_data))