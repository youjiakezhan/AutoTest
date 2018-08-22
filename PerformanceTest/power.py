# coding=utf-8
import os

from AutoTest.funclib.adb_command import AdbCommand
from AutoTest.funclib.send_email import SendEmail
from AutoTest.performancetest.comman import *


# 测试
class BatteryTest(object):

    # 清空手机耗电记录
    def reset_batteryinfo(self):
        os.popen('adb shell dumpsys batterystats --enable full-wake-history')
        time.sleep(1)
        os.popen('adb shell dumpsys batterystats --reset')

    # 检查usb连接状态
    def check_usb_status(self):
        data = os.popen('adb shell dumpsys battery').readlines()
        for i in data:
            if 'USB powered' in i:
                # print(i.split()[bad_path])
                return i.split()[2]

    # 设置usb连接为连接不充电状态
    def set_usb_status(self):
        os.popen('adb shell dumpsys battery set usb 0')
        if self.check_usb_status() != 'false':
            print('设置usb不充电状态失败')

    # 恢复手机默认usb连接状态
    def reset_usb_status(self):
        os.popen('adb shell dumpsys battery reset')
        if self.check_usb_status() != 'true':
            print('恢复usb充电状态失败')

    # 获取设置usb连接状态和恢复usb默认连接状态期间的应用耗电量数据
    def get_batteryinfo(self):
        adb = AdbCommand(pkg_name)
        uid = adb.get_app_uid()
        content = os.popen('adb shell dumpsys batterystats|findstr "Uid"|findstr ' + uid).readlines()
        # android8.0
        # batteryinfo = (str(re.findall('(?<=[(])[^()]+\.[^()]+(?=[)])', content)).replace('[', '')).replace(']', '')
        for i in content[:int(len(content) / 2)]:
            batteryinfo = i.replace('Uid ' + uid + ': ', '').strip()
            print(batteryinfo)
            return batteryinfo


# 测试用例（场景设计）
class TestCase(BatteryTest):
    # 场景一：不添加应用挂后台5分钟(调出广告和信息流)
    def test01(self):
        while True:
            d.app_stop(pkg_name)
            time.sleep(1)
            d.app_start(pkg_name)
            if d(resourceId='com.excelliance.dualaid:id/tv_title').exists(10):
                break
        d(text='QQ').long_click()
        d(text=u"删除应用").click(timeout=5)
        d(resourceId="com.excelliance.dualaid:id/tv_left").click(timeout=5)
        self.reset_batteryinfo()
        self.set_usb_status()
        time.sleep(300)
        self.reset_usb_status()
        return self.get_batteryinfo()

    # 场景二：不添加应用停留主界面5分钟(调出广告和信息流)
    def test02(self):
        while True:
            d.app_stop(pkg_name)
            time.sleep(2)
            d.app_start(pkg_name)
            if d(resourceId='com.excelliance.dualaid:id/tv_title').exists(10):
                break
        self.reset_batteryinfo()
        self.set_usb_status()
        time.sleep(300)
        self.reset_usb_status()
        return self.get_batteryinfo()

    # 场景三：对比本机和双开QQ登录并置于后台5分钟的功耗(调出广告和信息流)
    def test03(self):
        u2 = U2()
        # 本机QQ功耗
        d.app_clear('com.tencent.mobileqq')
        self.reset_batteryinfo()
        self.set_usb_status()
        u2.local_QQ_login(QQ_user, QQ_key)
        d.press('home')
        time.sleep(300)
        self.reset_usb_status()
        power1 = int(self.get_batteryinfo())
        d.app_clear('com.tencent.mobileqq')
        # 双开QQ功耗
        d.app_stop('com.tencent.mobileqq')
        self.reset_batteryinfo()
        self.set_usb_status()
        u2.local_QQ_login(QQ_user, QQ_key)
        d.press('home')
        time.sleep(300)
        self.reset_usb_status()
        power2 = int(self.get_batteryinfo())
        return power2 - power1

    # 场景四：
    def test04(self):
        return 0

    # 场景五：
    def test05(self):
        return 0


def run_power(state):
    test = TestCase()
    e = SendEmail('wangzhongchang@excelliance.cn', 'wzc6851498', state)
    mail_content = """
            <html>
            <body>
            <div>
                <h2>双开助手性能测试：功耗测试</h2>
                <p>场景一：不添加应用挂后台5分钟(调出广告和信息流)</p>
                <p>场景二：不添加应用停留主界面5分钟(调出广告和信息流)</p>
                <p>场景三：对比本机和双开QQ登录并置于后台5分钟的功耗(调出广告和信息流)</p>
                <div id="content">
                    <table border="path" bordercolor="#87ceeb" width="300">
                        <tr>
                            <td><strong>测试场景</strong></td>
                            <td><strong>耗电量(mAh)</strong></td>
                        </tr>
                        <tr>
                            <td>场景一</td>
                            <td>%s</td>
                        </tr>
                        <tr>
                            <td>场景二</td>
                            <td>%s</td>
                        </tr>
                        <tr>
                            <td>场景三</td>
                            <td>%s</td>
                        </tr>
                    </table>
                </div>
            </div>
            </body>
            </html>
    """ % (test.test03(), test.test02(), test.test01())
    e.create_email(mail_content)
    print('功耗模块测试结束，性能测试完成')


if __name__ == '__main__':
    # run_power(state='debug')
    test = TestCase()
    test.test01()