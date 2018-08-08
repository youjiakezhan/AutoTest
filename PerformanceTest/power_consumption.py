# coding=utf-8
import os
import re
import time

from AutoTest.myfunction.adb_command import AdbCommand
from AutoTest.myfunction.send_email import SendEmail
from AutoTest.performancetest.comman import pkg_name, d


class BatteryTest(object):

    # 清空手机耗电记录
    def reset_batteryinfo(self):
        os.popen('adb shell dumpsys batterystats --reset')

    # 检查usb连接状态
    def check_usb_status(self):
        data = os.popen('adb shell dumpsys battery').readlines()
        for i in data:
            if 'status' in i and 'Accessory' not in i:
                print(type(i.split()[1]))
                return int(i.split()[1])

    # 设置usb连接为连接不充电状态
    def set_usb_status(self):
        os.popen('adb shell dumpsys battery set status 1')
        if self.check_usb_status() != 1:
            os.popen('adb shell dumpsys battery unplug')
            if self.check_usb_status() != 1:
                print('设置usb连接但不充电状态失败')

    # 恢复手机默认usb连接状态
    def reset_usb_status(self):
        os.popen('adb shell dumpsys battery reset')
        if self.check_usb_status() == 1:
            print('恢复usb连接可充电状态失败')

    # 获取设置usb连接状态和恢复usb默认连接状态期间的应用耗电量数据
    def get_batteryinfo(self):
        adb = AdbCommand(pkg_name)
        content = os.popen('adb shell dumpsys batterystats|findstr ' + adb.get_app_uid()).read()
        batteryinfo = (str(re.findall('(?<=[(])[^()]+\.[^()]+(?=[)])', content)).replace('[', '')).replace(']', '')
        print(batteryinfo)
        return batteryinfo


class TestCase(BatteryTest):
    # 场景一：停留主界面10分钟(调出广告和信息流)
    def test01(self):
        d.app_stop(pkg_name)
        time.sleep(1)
        d.app_start(pkg_name)
        if d(text='双开资讯').exists(10):
            self.reset_batteryinfo()
            self.set_usb_status()
            time.sleep(120)
            self.reset_usb_status()
            self.get_batteryinfo()
        else:
            print('信息流不存在')

    # 场景二：添加一个QQ并登录，停留主界面10分钟
    def test02(self):
        pass

    # 场景三：不添加应用挂后台10分钟(调出广告和信息流)
    def test03(self):
        pass

    # 场景四：添加一个QQ并登录，挂后台10分钟
    def test04(self):
        pass

    # 场景五：
    def test05(self):
        pass


def run_power():
    test = TestCase()
    e = SendEmail('a', 'd')
    test.test01()
    mail_content = """
            <html>
            <body>
            <div>
                <p><strong>双开助手(版本号：%s)</strong></p>
                <p>测试数据单位均为mAh</p>
                <div id="content">
                    <table border="1" bordercolor="#87ceeb" width="300">
                        <tr>
                            <td><strong>测试场景</strong></td>
                            <td><strong>耗电量</strong></td>
                        </tr>
                        <tr>
                            <td>场景一</td>
                            <td>%d</td>
                        </tr>
                        <tr>
                            <td>场景一</td>
                            <td>%d</td>
                        </tr>
                        <tr>
                            <td>场景一</td>
                            <td>%d</td>
                        </tr>
                        <tr>
                            <td>场景一</td>
                            <td>%d</td>
                        </tr>
                        <tr>
                            <td>场景一</td>
                            <td>%d</td>
                        </tr>
                        <tr>
                            <td>场景一</td>
                            <td>%d</td>
                        </tr>
                    </table>
                </div>
            </div>
            </body>
            </html>
    """
    e.create_email(mail_content)


if __name__ == '__main__':
    run_power()
