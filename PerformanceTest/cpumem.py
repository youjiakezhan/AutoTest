# coding=utf-8
import os
import threading
import time

import matplotlib.pyplot as plt
import numpy as np
import uiautomator2 as u2
from AutoTest.myfunction.send_email import SendEmail

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
        d.app_start(self.pck)
        d(resourceId='com.excelliance.dualaid:id/iv_icon').exists(10)
        # 测试场景循环，次数为num
        i = 0
        while i < num:
            try:
                d(resourceId='com.excelliance.dualaid:id/iv_icon').click(timeout=3)
                d(resourceId='com.excelliance.dualaid:id/iv_back').click(timeout=3)
                i += 1
            except u2.UiObjectNotFoundError:
                print('未找到控件1')
                d.press('back')
                continue

    # 测试场景二：主界面点击添加按钮
    def test02(self, num):
        # 测试环境配置
        d(resourceId='com.excelliance.dualaid:id/iv_icon').exists(5)
        # 测试场景循环，次数为num
        i = 0
        while i < num:
            try:
                d(resourceId="com.excelliance.dualaid:id/add_but").click(timeout=3)
                d(resourceId="com.excelliance.dualaid:id/iv_back").click(timeout=3)
                i += 1
            except u2.UiObjectNotFoundError:
                print('未找到控件2')
                d.press('back')
                continue

    # 测试场景三：主界面启动微信（已登录）
    def test03(self, num):
        # 测试环境配置
        d(resourceId='com.excelliance.dualaid:id/iv_icon').exists(5)
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
                print('未找到控件3')
                d.press('back')
                continue

    # 测试场景四：主界面back再进
    def test04(self, num):
        # 测试环境配置
        d.press('back')
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
                d(resourceId='com.excelliance.dualaid:id/iv_icon').exists(5)
                i += 1
            except u2.UiObjectNotFoundError:
                print('未找到控件4')
                d.press('back')
                continue

    # 测试场景五：home置于后台
    def test05(self, bgtime):
        # 测试环境配置
        d.press('home')
        # app置于后台时间为bgtime（s）
        d.press('home')
        time.sleep(bgtime)


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


# 数据获取
class GetData(object):
    def meminfo(self, pck):
        global monitor_start_flag, mast, lbcore, lebian, t_mem
        mast = []
        lbcore = []
        lebian = []
        t_mem = []
        print('memory监控开启')
        while True:
            if monitor_start_flag == 1:
                try:
                    start = time.time()
                    datas = os.popen('adb shell dumpsys meminfo | findstr ' + pck).readlines()
                    for data in datas[0:int(len(datas) / 2)]:
                        i = data.strip()
                        if 'activities' in i and 'platform' not in i:
                            mast.append(round(int(i.split()[0]) / 1024))
                        elif 'lbcore' in i:
                            lbcore.append(round(int(i.split()[0]) / 1024))
                        elif 'lebian' in i:
                            lebian.append(round(int(i.split()[0]) / 1024))
                    if len(mast) > len(lbcore):
                        lbcore.append(0)
                    if len(mast) > len(lebian):
                        lebian.append(0)
                    t_mem.append(3 * len(mast))
                    print('t_mem=%s' % len(t_mem))
                    print('mast=%s' % len(mast))
                    print('lbcore=%s' % len(lbcore))
                    print('lebian=%s' % len(lebian))
                    time.sleep(1)
                    end = time.time()
                    t = round((end - start), 1)
                    print('耗时1：%s' % t)
                except UnboundLocalError:
                    print('未检测到双开进程')
                    continue
            else:
                print('memory监控关闭')
                break

    def cpuinfo(self, pck):
        global cpu_data, t_cpu
        cpu_data = []
        cpu = []
        t_cpu = []
        print('cpu监控开启')
        while True:
            if monitor_start_flag == 1:
                try:
                    start = time.time()
                    datas = os.popen('adb shell top -n 1 | findstr ' + pck).readlines()
                    for data in datas:
                        if 'excelliance' in data:
                            cpu.append(data.split()[2].replace('%', ''))
                        else:
                            cpu.append(0)
                    cpu_data.append(round(sum(list(float(i) for i in cpu))))
                    t_cpu.append(3 * len(cpu_data))
                    print('t_cpu=%s' % len(t_cpu))
                    print('cpu_data=%s' % len(cpu_data))
                    cpu = []  # 清空过度容器
                    end = time.time()
                    t = round((end - start), 1)
                    print('耗时2：%s' % t)
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
        plt.figure(figsize=(10, 14), dpi=120)
        plt.subplot(411)
        plt.title('内存——主进程')
        plt.xlabel('时间(s)')
        plt.ylabel('内存值（单位Mb）')
        # my_x_ticks = np.arange(0, max(t_mem), 3)
        my_y_ticks = np.arange(0, max(mast), 10)
        # plt.xticks(my_x_ticks)
        plt.yticks(my_y_ticks)
        plt.plot(mast, 'purple', label='主进程')
        plt.legend()
        plt.grid(color='skyblue')

        plt.subplot(412)
        plt.title('内存——lbcore')
        plt.xlabel('时间(s)')
        plt.ylabel('内存值（单位Mb）')
        # my_x_ticks = np.arange(0, max(t_mem), 3)
        my_y_ticks = np.arange(0, max(lbcore), 1)
        # plt.xticks(my_x_ticks)
        plt.yticks(my_y_ticks)
        plt.plot(lbcore, 'g', label='lbcore')
        plt.legend()
        plt.grid(color='skyblue')

        plt.subplot(413)
        plt.title('内存——lebian')
        plt.xlabel('时间(s)')
        plt.ylabel('内存值（单位Mb）')
        # my_x_ticks = np.arange(0, max(t_mem), 3)
        my_y_ticks = np.arange(0, max(lebian), 1)
        # plt.xticks(my_x_ticks)
        plt.yticks(my_y_ticks)
        plt.plot(lebian, 'b', label='lebian')
        plt.legend()
        plt.grid(color='skyblue')

        plt.subplot(414)
        plt.title('CPU')
        plt.xlabel('时间(s)')
        plt.ylabel('cpu(占用百分比%)')
        # my_x_ticks = np.arange(0, max(t_cpu), 3)
        my_y_ticks = np.arange(0, max(cpu_data), 1)
        # plt.xticks(my_x_ticks)
        plt.yticks(my_y_ticks)
        plt.plot(cpu_data, 'r', label='cpu')
        plt.legend()
        plt.grid(color='skyblue')
        plt.tight_layout(h_pad=1)
        plt.savefig(path + '\\%s.png' % time.strftime('%Y%m%d%H%M%S'))
        plt.show()


# 初始化uiautomator2
def __init__():
    global d
    # 初始化uiautomator2
    d = u2.connect_usb('900ca8ab')
    # 启动uiautomator2的守护进程
    d.healthcheck()
    return d


# 执行测试入口
def run(path, num=25, bgtime=50):
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
    case.test05(bgtime)
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
            # run(result_path, int(input('输入各个场景的循环次数：')), int(input('输入app置于后台的时间（s）：')))    # 参数设置
            run(result_path)  # 测试场景默认循环10次，app置于后台时间默认为60s
            break
        except Exception as e:
            print(e)
            continue
    sendemail.create_email('双开助手性能测试：内存/cpu测试结果')
    print(len(t_mem), len(mast), len(lbcore), len(lebian), len(cpu_data), len(t_cpu))
