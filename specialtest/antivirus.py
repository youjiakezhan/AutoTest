# coding=utf-8
import os
import threading
import time

import uiautomator2 as u2


class CreateThread(object):
    def start_thread(self, func):
        """开启一条执行func函数的新线程"""
        global flag
        flag = 1
        threading.Thread(target=func).start()

    def stop_thread(self):
        global flag
        flag = 0
        while True:
            if threading.active_count() > 1:
                time.sleep(1)
            else:
                break


class Monitor(object):
    def __init__(self, bad_path):
        self.bad_path = bad_path

    # 检测安装
    def install_alert(self):
        """监控并处理应用安装弹窗"""
        print('监控1已启动')
        while True:
            if flag == 1:
                try:
                    if d(resourceId="com.android.packageinstaller:id/apk_info_view").exists(15) is True:
                        time.sleep(1)
                        d(text="继续安装").click(timeout=10)
                        time.sleep(1)
                        d(text="安装").click(timeout=3)
                        time.sleep(1)
                        d(text="完成").click(timeout=3)
                        print('apk安装完成')
                except Exception:
                    continue
            else:
                print('监控1已停止')
                break

    # 移动文件
    def move_file(self, path):
        os.popen('move ' + move_apk_path + ' ' + path)

    # 检测病毒1
    def antivirus_file(self):
        print('监控2已启动')
        while True:
            if flag == 1:
                try:
                    if d(resourceId="com.tencent.qqpimsecure:id/im").exists(5) is True:
                        length = len(os.listdir(self.bad_path))
                        self.move_file(self.bad_path)
                        d.press('home')
                        while True:
                            if length < len(os.listdir(self.bad_path)):
                                print('检测到报毒，已隔离apk文件至bad_path目录')
                                break
                            else:
                                time.sleep(1)
                except Exception:
                    continue
            else:
                print('监控2已停止')
                break

    # 检测病毒2
    def antivirus_url(self):
        global new_url_path
        print('监控2已启动')
        while True:
            if flag == 1:
                try:
                    if d(resourceId="com.tencent.qqpimsecure:id/im").exists(5) is False:
                        with open(new_url_path, 'a') as fp:
                            fp.write(url_path + '\n')
                        d.press('home')
                except Exception:
                    continue
            else:
                print('监控2已停止')
                break


class AppInstall(object):
    # 获取apk包名
    def get_pkg_name(self, path):
        data = os.popen('aapt dump badging ' + path).readlines()
        for i in data:
            if 'package:' in i:
                apk_name = i.split()[1].replace('name=', '')
                return apk_name

    # 按照参数指定的路径完成apk的安装
    def install(self, apk_path):
        global pkg_name
        pkg_name = self.get_pkg_name(apk_path).replace("'", '')
        os.popen('adb install -r ' + apk_path)
        print(pkg_name)
        while True:
            if pkg_name in os.popen('adb shell pm list package').read():
                print('安装完成')
                break

    # 安装前先卸载本机上安装的同名包
    def app_uninstall(self, app_name):
        try:
            os.popen('adb uninstall ' + app_name)
            time.sleep(5)
            print('已卸载')
        except Exception:
            print('no such apk')

    # 按照下载地址参数安装apk
    def url_app_install(self, urls_path):
        global url_path
        with open(urls_path, 'r') as fp:
            for i in fp:
                while True:
                    try:
                        pkg_name = d.app_install(i.strip())
                        break
                    except RuntimeError as e:
                        print(e)
                if d(text='确定').exists(5) is True:
                    d(text='确定').click(timeout=5)
                time.sleep(5)
                self.app_uninstall(pkg_name)

    # 按照文件路径参数安装apk
    def file_app_install(self, file_path):
        global move_apk_path
        for i in os.listdir(file_path):
            move_apk_path = os.path.join(file_path, i)
            print(move_apk_path)
            self.install(move_apk_path)
            time.sleep(5)
            self.app_uninstall(pkg_name)


def unlock():
    if d.info['screenOn']:
        pass
    else:
        d.screen_on()
        d.unlock()
        d.press('home')


def run():
    global d
    # 初始化引擎
    try:
        d = u2.connect()
        d.healthcheck()
    except Exception:
        d.service('uiautomator').stop()
        time.sleep(2)
        d = u2.connect()
        d.healthcheck()
    unlock()
    thread = CreateThread()
    # 指定文件保存目录
    monitor = Monitor(r'C:\Users\BAIWAN\Desktop\bad_path.txt')
    # 启动安装和扫毒监控
    # thread.start_thread(monitor.install_alert)
    thread.start_thread(monitor.antivirus_url)
    install = AppInstall()
    # 选择安装方式（默认按文件安装）
    install.url_app_install(r'C:\Users\BAIWAN\Desktop\apk.txt')
    thread.stop_thread()
    d.service('uiautomator').stop()
    print('测试结束')


if __name__ == '__main__':
    run()
