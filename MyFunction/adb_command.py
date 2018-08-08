# coding=utf-8
import os
import time
import uiautomator2 as u2


class AdbCommand(object):
    """调用adb命令获取设备或者app的相关信息"""
    __adb_command = [
        'adb devices',
        'adb shell',
    ]

    def __init__(self, pkg_name):
        """初始化AdbCommand类，传入apk的包名参数"""
        self.pkg_name = pkg_name

    def command_list(self):
        print(self.__adb_command)

    def check_adb_connect(self):
        """查看USB连接状态"""
        text = os.popen('adb devices').readlines()
        if 'device' in text[1]:
            print('USB连接正常')
            return True
        else:
            print('USB未连接')
            return False

    def get_app_uid(self):
        """根据app包名获取其uid号"""
        content = os.popen('adb shell pm dump ' + self.pkg_name + ' | findstr "u0a"').read()
        uid = content.split()[-1].replace(':', '')
        print(uid)
        return uid

    def get_app_launch_activity(self):
        """根据app包名获取其启动入口类"""
        activity = (x.split()[5] for x in os.popen('adb shell monkey -v -v -v 0').readlines() if self.pkg_name in x)
        launch_activity = self.pkg_name + '/' + activity.__next__()
        print(launch_activity)
        return launch_activity

    def app_start(self):
        """启动app"""
        os.popen('adb shell am start ' + self.get_app_launch_activity())

    def keyevent_back(self):
        """back按键"""
        os.popen('adb shell input keyevent 4')

    def keyevent_home(self):
        """home按键"""
        os.popen('adb shell input keyevent 3')

    def app_force_stop(self):
        """强行停止app"""
        os.popen('adb shell am force-stop ' + self.pkg_name)

    def app_data_clear(self):
        """清除app数据"""
        os.popen('adb shell pm clear ' + self.pkg_name)

    def uninstall_app(self):
        """卸载app"""
        os.popen('adb uninstall com.excelliance.dualaid')

    def get_android_version(self):
        """获取设备的Android版本号"""
        version = os.popen('adb shell getprop ro.build.version.release').read().strip()
        print(version)
        return version


class UI2(AdbCommand):

    def __init__(self):
        super(UI2, self).__init__(self)
        # 初始化uiautomator2并建立连接
        print(self)
        global d
        d = u2.connect()
        # 启动uiautomator2的守护进程
        d.healthcheck()


if __name__ == '__main__':
    a = AdbCommand('com.excelliance.dualaid')
    s = UI2()
    d.press('home')
    s.command_list()
