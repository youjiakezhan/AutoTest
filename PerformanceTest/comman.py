# coding=utf-8
import os

import uiautomator2 as u2

pkg_name = 'com.excelliance.dualaid'
activity = 'com.excelliance.kxqp.ui.HelloActivity'


def get_phone_ip():
    data = os.popen('adb shell netcfg').readlines()
    for i in data:
        if 'wlan0' in i:
            ip = i.split()[2].split('/')[0]
            print(ip)
            return ip


def u2_init():
    # 初始化uiautomator2
    device = u2.connect()
    return device


def send_text(text):
    d.set_fastinput_ime(True)     # 切换成FastInputIME输入法
    d.send_keys(text)   # adb广播输入
    # d.clear_text()                # 清除输入框所有内容(Require android-uiautomator.apk version >= path.0.7)
    d.set_fastinput_ime(False)    # 切换成正常的输入法


d = u2_init()
