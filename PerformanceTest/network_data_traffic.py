# coding=utf-8

import time

from AutoTest.myfunction.send_email import SendEmail
# 数据获取与处理
from AutoTest.performancetest.comman import *


class GetData(object):

    def get_uid(self):
        uid = ''
        data = os.popen('adb shell ps | findstr "excelliance"').readlines()
        try:
            uid = int(data[0].split()[0].replace('u0_a', '')) + 10000
            # print(uid)
        except IndexError:
            print('未检测到双开助手的进程')
        return str(uid)

    def get_data(self):
        data_traffic = []
        send = 0
        receive = 0
        try:
            datas = os.popen('adb shell cat /proc/net/xt_qtaguid/stats | findstr ' + self.get_uid()).readlines()
            for data in datas:
                if len(data) > 1:
                    send += int(data.split()[5]) / 1024
                    receive += int(data.split()[7]) / 1024
                else:
                    continue
            data_traffic = round(send + receive)
            print(data_traffic)
        except IndexError:
            pass
        return data_traffic

    # 间隔指定时间获取当前数据，若间隔前后所取的数据相等则表示数据已经稳定下来可以继续进行下一步测试；
    # 如果间隔前后获取的数据不等，则继续等待直到数据稳定再进行下一步测试；
    # 返回稳定后的数据；
    def diff(self):
        while True:
            data1 = self.get_data()
            time.sleep(5)
            data2 = self.get_data()
            if data1 != data2:
                print('等待数据稳定...')
                time.sleep(5)
            else:
                print('数据已稳定')
                return data2


# 场景设计
class TestCase(GetData):
    def __init__(self):
        self._QQ_username = '1037287177'
        self._QQ_key = 'wangchangQQ227x'
        self._wechat_username = '18501701705'
        self._wechat_key = 'zmcs0000'

    # 场景一：主界面back再进至页面加载完成
    def test1(self):
        while True:
            d.app_stop(pkg_name)
            time.sleep(2)
            d.app_start(pkg_name)
            if d(text='双开资讯').exists(10):
                d.press('back')
                start_flow = self.diff()
                d.app_start(pkg_name)
                d(text='双开资讯').exists(10)
                end_flow = self.diff()
                print('流量消耗：%sKb' % (end_flow - start_flow))
                return end_flow - start_flow
            else:
                continue

    # 场景二：空载挂后台10分钟
    def test2(self):
        while True:
            d.app_stop(pkg_name)
            time.sleep(2)
            d.app_start(pkg_name)
            if d(resourceId='com.excelliance.dualaid:id/tv_title').exists(10):
                d.press('home')
                start_flow = self.diff()
                time.sleep(600)
                end_flow = self.diff()
                print('流量消耗：%sKb' % (end_flow - start_flow))
                return end_flow - start_flow
            else:
                continue

    # 场景三：添加并登录一个QQ，挂后台10分钟
    def test3(self):
        # 添加并登录QQ
        def add_QQ_and_login():
            d.app_stop(pkg_name)
            time.sleep(2)
            d.app_start(pkg_name)
            d(text='双开资讯').exists(10)
            d(resourceId="com.excelliance.dualaid:id/add_but").click(timeout=5)
            d(text='QQ').click(timeout=5)
            time.sleep(2)
            d(text='QQ').click(timeout=10)
            d(resourceId="com.tencent.mobileqq:id/btn_login").click(timeout=30)
            d(text='QQ号/手机号/邮箱').click(timeout=5)
            send_text(self._QQ_username)
            time.sleep(2)
            d(resourceId="com.tencent.mobileqq:id/password").click(timeout=5)
            send_text(self._QQ_key)
            d(resourceId="com.tencent.mobileqq:id/login").click(timeout=10)
            time.sleep(10)
            if d(resourceId="android:id/content").exists(5):
                d(resourceId="com.tencent.mobileqq:id/name", description=u"已关闭").click(timeout=5)
            if d(resourceId="com.tencent.mobileqq:id/name", text=u"马上绑定").exists(5):
                d(resourceId="com.tencent.mobileqq:id/ivTitleBtnLeft").click(timeout=5)
                d(resourceId="com.tencent.mobileqq:id/name", text=u"联系人").click(timeout=5)
            time.sleep(3)
            d(resourceId="com.tencent.mobileqq:id/name", text=u"动态").click(timeout=5)
            time.sleep(3)
            d(resourceId="com.tencent.mobileqq:id/name", text=u"消息").click(timeout=5)
            time.sleep(3)
        add_QQ_and_login()
        d.press('home')
        start_flow = self.diff()
        time.sleep(600)
        end_flow = self.diff()
        print('流量消耗：%sKb' % (end_flow - start_flow))
        return end_flow - start_flow

    # 场景四：添加并登录一个微信，挂后台10分钟
    # def test4(self):
    #     d.app_stop(self.pkg_name)
    #     time.sleep(bad_path)
    #     d.app_start(self.pkg_name)
    #     d(resourceId='com.excelliance.dualaid:id/tv_title').exists(10)
    #     d(resourceId="com.excelliance.dualaid:id/add_but").click(timeout=5)
    #     d(text='微信').click(timeout=5)
    #     d(text='私密空间').click(timeout=10)
    #     while True:
    #         d.app_stop(self.pkg_name)
    #         time.sleep(bad_path)
    #         d.app_start(self.pkg_name)
    #         if d(resourceId='com.excelliance.dualaid:id/tv_title').exists(10):
    #             d.press('home')
    #             start_flow = self.diff()
    #             time.sleep(600)
    #             end_flow = self.diff()
    #             print('流量消耗：%sKb' % (end_flow - start_flow))
    #             return end_flow - start_flow
    #         else:
    #             continue

    # 场景五：添加并登录一个微信和一个QQ，挂后台10分钟
    # def test5(self):
    #     start_flow = self.diff()
    #
    #     end_flow = self.diff()
    #     return end_flow - start_flow

    # 场景六：
    # def test6(self):
    #     start_flow = self.diff()
    #
    #     end_flow = self.diff()
    #     return end_flow - start_flow


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
                            <tr>
                                <td>场景四</td>
                                <td>%d</td>
                            </tr>
                            <tr>
                                <td>场景五</td>
                                <td>%d</td>
                            </tr>
                        </table>
                    </div>
                </div>
                </body>
                </html>
            """ % (s1, s2, s3, 0, 0)
    e.create_email(mail_content)
    print('流量模块测试结束，准备开始测试功耗模块')


if __name__ == '__main__':
    run_network(state='debug')
