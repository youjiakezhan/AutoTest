# coding=utf-8
import os

from AutoTest.funclib.adb_command import AdbCommand
from AutoTest.funclib.send_email import SendEmail
from AutoTest.performancetest.comman import *


# 数据获取与处理
class GetData(object):
    def get_data(self, pkg=pkg_name):
        adb = AdbCommand(pkg)
        uid = adb.get_app_uid()
        data_traffic = 0
        try:
            datas = os.popen('adb shell cat /proc/net/xt_qtaguid/stats | findstr ' + str(
                int(uid.replace('u0a', '')) + 10000)).readlines()
            for data in datas:
                if len(data) > 1:
                    data_traffic += int(data.split()[5]) / 1024 + int(data.split()[7]) / 1024
            print(round(data_traffic))
            return round(data_traffic)
        except IndexError:
            print('获取流量出错')

    # 间隔指定时间获取当前数据，若间隔前后所取的数据相等则表示数据已经稳定下来可以继续进行下一步测试；
    # 如果间隔前后获取的数据不等，则继续等待直到数据稳定再进行下一步测试；
    # 返回稳定后的数据；
    def diff(self, pkg=pkg_name):
        while True:
            data1 = self.get_data(pkg)
            time.sleep(5)
            data2 = self.get_data(pkg)
            if data1 != data2:
                print('等待数据稳定...')
                time.sleep(5)
            else:
                print('数据已稳定')
                return data2


# 场景设计
class TestCase(GetData):
    # 场景一：不添加任何应用挂后台5分钟
    def test1(self):
        while True:
            d.app_stop(pkg_name)
            time.sleep(2)
            d.app_start(pkg_name)
            if d(resourceId='com.excelliance.dualaid:id/tv_title').exists(10):
                d(text='微信').long_click()
                d(text=u"删除应用").click(timeout=5)
                d(resourceId="com.excelliance.dualaid:id/tv_left").click(timeout=5)
                d.press('home')
                start_flow = self.diff()
                time.sleep(300)
                end_flow = self.diff()
                d.app_stop(pkg_name)
                print('流量消耗：%sKb' % (end_flow - start_flow))
                return end_flow - start_flow
            else:
                continue

    # 场景二：主界面back再进至页面加载完成并停留5分钟
    def test2(self):
        while True:
            d.app_stop(pkg_name)
            time.sleep(2)
            d.app_start(pkg_name)
            if d(resourceId='com.excelliance.dualaid:id/tv_title').exists(10):
                d.press('back')
                start_flow = self.diff()
                d.app_start(pkg_name)
                d(resourceId='com.excelliance.dualaid:id/tv_title').exists(10)
                time.sleep(300)
                end_flow = self.diff()
                d.app_stop(pkg_name)
                print('流量消耗：%sKb' % (end_flow - start_flow))
                return end_flow - start_flow
            else:
                continue

    # 场景三：对比本机和双开QQ登录并置于后台5分钟的流量消耗
    def test3(self):
        u2 = U2()
        # 添加并登录本机QQ
        start_flow1 = self.diff(pkg='com.tencent.mobileqq')
        u2.local_QQ_login(QQ_user, QQ_key)
        d.press('home')
        time.sleep(5)
        d.app_stop('com.tencent.mobileqq')
        end_flow1 = self.diff(pkg='com.tencent.mobileqq')
        d.app_clear('com.tencent.mobileqq')
        flow1 = end_flow1 - start_flow1
        # 添加并登录双开QQ
        start_flow2 = self.diff()
        u2.multi_QQ_login(QQ_user, QQ_key)
        d.press('home')
        time.sleep(5)
        d.app_stop(pkg_name)
        end_flow2 = self.diff()
        flow2 = end_flow2 - start_flow2
        print('本机QQ消耗流量：%sKb' % flow1)
        print('双开QQ消耗流量：%sKb' % flow2)
        return flow2 - flow1

    # 场景四：
    def test4(self):
        return 0

    # 场景五：
    def test5(self):
        return 0


# 测试结果展示
def run_network(state):
    test = TestCase()
    e = SendEmail('wangzhongchang@excelliance.cn', 'wzc6851498', state)
    s1 = test.test1()
    s2 = test.test2()
    s3 = test.test3()
    mail_content = """
                    <html>
                    <body>
                    <div>
                    <h2>双开助手性能测试：流量测试</h2>
                    <p>场景一：空载(不添加应用)挂后台5分钟</p>
                    <p>场景二：主界面back再进至页面加载完成并停留5分钟</p>
                    <p>场景三：对比本机和双开QQ登录并置于后台5分钟的流量消耗</p>
                    <p></p>
                    <p></p>
                    <div id="content">
                        <table border="path" bordercolor="#87ceeb" width="300">
                            <tr>
                                <td><strong>测试场景</strong></td>
                                <td><strong>消耗流量(KB)</strong></td>
                            </tr>
                            <tr>
                                <td>场景一</td>
                                <td>%d</td>
                            </tr>
                            <tr>
                                <td>场景二</td>
                                <td>%d</td>
                            </tr>
                            <tr>
                                <td>场景三</td>
                                <td>%d</td>
                            </tr>
                        </table>
                    </div>
                </div>
                </body>
                </html>
            """ % (s1, s2, s3)
    e.create_email(mail_content)
    print('流量模块测试结束，准备开始测试功耗模块')


if __name__ == '__main__':
    # run_network(state='debug')
    t = TestCase()
    t.test3()
