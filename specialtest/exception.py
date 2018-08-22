# coding=utf-8
import random

from AutoTest.funclib.adb_command import AdbCommand
from AutoTest.performancetest.comman import *

adb = AdbCommand(pkg_name)
Basepath = os.getcwd()


# 测试用例
class Case(U2, NewThread, MutipleApp, PhoneSetting, Log):
    # 强行停止再启动
    def test01(self, num):
        log = self.start_log(Basepath + '\\exception_log\\log01.txt')
        i = 0
        while i <= num:
            i += 1
            d.app_stop(pkg_name)
            time.sleep(1)
            d.app_start(pkg_name)
            if not d(resourceId="com.excelliance.dualaid:id/ad_but").exists(8):
                d.screenshot((Basepath + '\\exception_error\\img01%s.png' % time.strftime('%H%M%S')))
        self.stop_log(log)
        save_log('log01')

    # 清除数据再启动
    def test02(self, num):
        log = self.start_log(Basepath + '\\exception_log\\log02.txt')
        i = 0
        while i <= num:
            i += 1
            d.app_clear(pkg_name)
            time.sleep(2)
            d.app_start(pkg_name)
            if d(text=u'点击加号，添加双开应用').exists(5):
                d(scrollable=True).fling.horiz.forward(100)
                d(scrollable=True).fling.horiz.forward(100)
                if not d(text='开始体验').exists(5):
                    d.screenshot((Basepath + '\\exception_error\\img02%s.png' % time.strftime('%H%M%S')))
        self.stop_log(log)
        save_log('log02')

    #
    def test03(self):
        pass


def save_log(log_name):
    if len(os.listdir(Basepath + '\\exception_error')) == 0:
        while True:
            try:
                os.remove(Basepath + '\\exception_log\\%s.txt' % log_name)
                break
            except PermissionError:
                time.sleep(.5)
    else:
        for i in os.listdir(Basepath + '\\exception_error'):
            if log_name in i:
                break
            else:
                while True:
                    try:
                        os.remove(Basepath + '\\exception_log\\%s.txt' % log_name)
                        break
                    except PermissionError:
                        time.sleep(.5)


def run(num=3):
    case = Case()
    case.test01(num)
    case.test02(num)


if __name__ == '__main__':
    run()
