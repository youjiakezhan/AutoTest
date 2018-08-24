# coding=utf-8
import os

import matplotlib.pyplot as plt
import numpy as np

from AutoTest.funclib.matplotlib_setting import matplot_init
from AutoTest.funclib.send_email import SendEmail
from AutoTest.performancetest.comman import *

# 脚本功能说明文档
__doc__ = """
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

    # 测试场景一：主界面点击个人中心按钮
    def test01(self, num):
        # 测试环境配置
        d.press('back')
        d.press('home')
        time.sleep(.5)
        d.app_start(pkg_name)
        d(resourceId='com.excelliance.dualaid:id/iv_icon').exists(10)
        # 测试场景循环，次数为num
        i = 0
        while i < num:
            try:
                d(resourceId='com.excelliance.dualaid:id/iv_icon').click(timeout=10)
                time.sleep(.5)
                d(resourceId='com.excelliance.dualaid:id/iv_back').click(timeout=10)
                i += 1
            except Exception as e:
                print('未找到控件1:%s' % e)
                d.press('back')
                time.sleep(.5)
                d.press('home')
                time.sleep(.5)
                d.app_start(pkg_name)

    # 测试场景二：主界面点击添加按钮
    def test02(self, num):
        # 测试环境配置
        d(resourceId='com.excelliance.dualaid:id/iv_icon').exists(5)
        # 测试场景循环，次数为num
        i = 0
        while i < num:
            try:
                d(resourceId="com.excelliance.dualaid:id/add_but").click(timeout=8)
                time.sleep(.5)
                d(resourceId="com.excelliance.dualaid:id/iv_back").click(timeout=8)
                i += 1
            except u2.UiObjectNotFoundError:
                print('未找到控件2')
                d.press('back')
                d.press('home')
                time.sleep(.5)
                d.app_start(pkg_name)

    # 测试场景三：主界面启动微信（未登录）
    def test03(self, num):
        # 测试环境配置
        d(resourceId='com.excelliance.dualaid:id/iv_icon').exists(5)
        # 测试场景循环，次数为num
        i = 0
        while i < num:
            try:
                d(resourceId="com.excelliance.dualaid:id/item_app_name", text=u"微信").click()
                if d(text='以后再说').exists(3) is True:
                    d(text='以后再说').click(timeout=5)
                time.sleep(.5)
                d(text='登录').exists(10)
                d.press('back')
                time.sleep(.5)
                d(text='微信').exists(5)
                i += 1
            except u2.UiObjectNotFoundError:
                print('未找到控件3')
                if d(text='以后再说').exists(3) is True:
                    d(text='以后再说').click(timeout=5)
                else:
                    d.press('back')
                    d.press('home')
                    time.sleep(.5)
                    d.app_start(pkg_name)

    # 测试场景四：主界面back再进
    def test04(self, num):
        # 测试环境配置
        d.press('back')
        time.sleep(1)
        d.app_start(pkg_name)
        while True:
            if d(resourceId='com.excelliance.dualaid:id/iv_icon').exists(5) is True:
                break
            else:
                time.sleep(.5)
        # 测试场景循环，次数为num
        i = 1
        while i < num:
            try:
                d.press('back')
                time.sleep(1)
                d.app_start(pkg_name)
                d(resourceId='com.excelliance.dualaid:id/iv_icon').exists(10)
                i += 1
            except u2.UiObjectNotFoundError:
                print('未找到控件4')
                d.press('back')
                d.press('home')
                time.sleep(.5)
                d.app_start(pkg_name)

    # 测试场景五：home置于后台
    def test05(self, bgtime):
        # 测试环境配置
        d.press('home')
        # app置于后台时间为bgtime（s）
        d.press('home')
        time.sleep(bgtime)


# 数据获取
class GetData(object):
    def meminfo1(self):
        global thread_flag, mast
        mast = []
        print('memory1监控开启')
        while True:
            if thread_flag == 1:
                try:
                    datas = os.popen('adb shell dumpsys meminfo | findstr "excelliance"').readlines()
                    for data in datas[0:int(len(datas) / 2)]:
                        if 'activities' in data and 'platform' not in data:
                            mast.append(round(int(data.split()[0].replace(',', '').replace('K:', '')) / 1024))
                        else:
                            continue
                except UnboundLocalError:
                    print('未检测到双开进程')
                    continue
            else:
                print('memory1监控关闭')
                break

    def meminfo2(self):
        global thread_flag, lbcore
        lbcore = []
        print('memory2监控开启')
        while True:
            if thread_flag == 1:
                try:
                    datas = os.popen('adb shell dumpsys meminfo | findstr com.excelliance.dualaid:lbcore').readlines()[
                        0].split()[0]
                    if datas is not None:
                        lbcore.append(round(int(datas.replace(',', '').replace('K:', '')) / 1024))
                except IndexError:
                    lbcore.append(0)
            else:
                print('memory2监控关闭')
                break

    def meminfo3(self):
        global thread_flag, lebian
        lebian = []
        print('memory3监控开启')
        while True:
            if thread_flag == 1:
                try:
                    datas = \
                        os.popen('adb shell dumpsys meminfo | findstr "com.excelliance.dualaid:lebian"').readlines()[
                            0].split()[0]
                    if datas is not None:
                        lebian.append(round(int(datas.replace(',', '').replace('K:', '')) / 1024))
                except IndexError:
                    lebian.append(0)
            else:
                print('memory3监控关闭')
                break

    def cpuinfo(self):
        global thread_flag, cpu_data
        cpu_data = []
        cpu = []
        print('cpu监控开启')
        while True:
            if thread_flag == 1:
                try:
                    datas = os.popen('adb shell top -n 1 | findstr "com.excelliance.dualaid"').readlines()
                    for data in datas:
                        if 'excelliance' in data:
                            cpu.append(data.split()[2].replace('%', ''))
                        else:
                            cpu.append(0)
                    cpu_data.append(round(sum(list(float(i) for i in cpu))))
                    cpu = []  # 清空过度容器
                except UnboundLocalError:
                    print('未检测到双开进程')
                    continue
            else:
                print('cpu监控关闭')
                break


# 数据处理
class DataOperate(object):
    # 数据可视化
    def create_picture(self, path):
        matplot_init()  # 设置matplotlib中文显示问题
        plt.figure(figsize=(8, 12), dpi=120)  # 设置图片框架
        plt.subplot(411)  # 设置子图片
        plt.title('内存—主进程')  # 设置图片标题
        plt.xlabel('样本数(%d组)' % len(mast))  # 设置x轴标签
        plt.ylabel('内存值(单位Mb)')  # 设置y轴标签
        my_y_ticks = np.arange(0, max(mast), 10)
        plt.yticks(my_y_ticks)  # 设置y轴刻度
        plt.plot(mast, 'purple', label='主进程')
        plt.legend()  # 显示标注
        plt.grid(color='skyblue')  # 显示网格线

        plt.subplot(412)
        plt.title('内存—lbcore')
        plt.xlabel('样本数(%d组)' % len(lbcore))
        plt.ylabel('内存值(单位Mb)')
        my_y_ticks = np.arange(0, max(lbcore), 1)
        plt.yticks(my_y_ticks)
        plt.plot(lbcore, 'g', label='lbcore')
        plt.legend()
        plt.grid(color='skyblue')

        plt.subplot(413)
        plt.title('内存—lebian')
        plt.xlabel('样本数(%d组)' % len(lebian))
        plt.ylabel('内存值(单位Mb)')
        my_y_ticks = np.arange(0, max(lebian), 1)
        plt.yticks(my_y_ticks)
        plt.plot(lebian, 'b', label='lebian')
        plt.legend()
        plt.grid(color='skyblue')

        plt.subplot(414)
        plt.title('CPU')
        plt.xlabel('样本数(%d组)' % len(cpu_data))
        plt.ylabel('cpu(占用百分比%)')
        my_y_ticks = np.arange(0, max(cpu_data), 1)
        plt.yticks(my_y_ticks)
        plt.plot(cpu_data, 'r', label='cpu')
        plt.legend()
        plt.grid(color='skyblue')
        plt.tight_layout(h_pad=1)  # 设置子图片间的位置
        plt.savefig(path + '\\cpumem_image\\%s.png' % time.strftime('%Y%m%d%H%M%S'))  # 保存生成的图片


# 执行测试入口
def run_cpu_mem(state='debug', num=30, bgtime=60):
    global thread_flag
    thread_flag = 1
    path = os.path.abspath(os.path.dirname('__file__'))
    case = Case()
    data_opr = DataOperate()
    new_thread = NewThread()
    data = GetData()
    sendemail = SendEmail('wangzhongchang@excelliance.cn', 'wzc6851498', state, image_path=path + r'\cpumem_image')
    # 开启监控线程（开始获取数据）
    new_thread.start_thread(data.cpuinfo)
    new_thread.start_thread(data.meminfo1)
    new_thread.start_thread(data.meminfo2)
    new_thread.start_thread(data.meminfo3)
    # 执行测试用例(执行方式优化+)
    case.test01(num)
    case.test02(num)
    case.test03(num)
    case.test04(num)
    case.test05(bgtime)
    # 停止监控线程
    thread_flag = 0
    time.sleep(5)
    # 根据当前获取的数据生成图表
    data_opr.create_picture(path)
    # 邮件内容
    mail_content = '''
    <html>
    <body>
    <h2>双开助手性能测试：内存/cpu测试</h2>
    <p>测试场景一：主界面点击个人中心按钮30次</p>
    <p>测试场景二：主界面点击添加按钮30次</p>
    <p>测试场景三：主界面启动微信30次（未登录）</p>
    <p>测试场景四：主界面back再进30次</p>
    <p>测试场景五：home置于后台1分钟</p>
    <div>
    <table border="path" bordercolor="#87ceeb" width="450">   
    <tr>
    <td><strong>监控项</strong></td>
    <td><strong>均值（Mb）</strong></td>
    <td><strong>波动(方差)</strong></td>
    </tr> 
    <tr>
    <td>主进程</td>
    <td>% d</td>
    <td>% d</td>
    </tr>
    <tr>
    <td>lbcore</td>
    <td>% d</td>
    <td>% d</td>
    </tr>
    <tr>
    <td>lebian</td>
    <td>% d</td>
    <td>% d</td>
    </tr>
    <tr>
    <td>cpu</td>
    <td>% d</td>
    <td>% d</td>
    </tr>
    </table>
    </div>
    </body>
    </html>
    ''' % (
        sum(mast) / len(mast), np.array(mast).var(),
        sum(lbcore) / len(lbcore), np.array(lbcore).var(),
        sum(lebian) / len(lebian), np.array(lebian).var(),
        sum(cpu_data) / len(cpu_data), np.array(cpu_data).var(),
    )
    sendemail.create_email(mail_content)
    print('cpu/内存模块测试结束，准备开始测试流量模块')


if __name__ == "__main__":
    # run_cpu_mem(int(input('输入各个场景的循环次数：')), int(input('输入app置于后台的时间（s）：')))  # 参数设置
    run_cpu_mem()
