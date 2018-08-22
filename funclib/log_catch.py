# coding=utf-8
import os
import time


# 获取安卓手机的运行日志,可同时抓取多个log
class Log(object):
    def start_log(self, log_path):
        adb_list_old = []
        adb_list_new = []
        for i in os.popen('tasklist|findstr "adb.exe"').readlines():
            adb_list_old.append(i.split()[1])
            print(adb_list_old)
        os.popen('adb logcat -v time > ' + log_path)
        time.sleep(1)
        for j in os.popen('tasklist | findstr "adb.exe"').readlines():
            adb_list_new.append(j.split()[1])
            print(adb_list_new)
        for log_pid in adb_list_new:
            if log_pid not in adb_list_old:
                print(log_pid)
                return log_pid

    def stop_log(self, log_pid):
        os.popen('taskkill /f /pid %s' % log_pid)


if __name__ == '__main__':
    a = Log()
    l1 = a.start_log(r'C:\Users\BAIWAN\PycharmProjects\AutoTest\specialtest\exception_log\%s.txt' % time.strftime('%H%M%S'))
    time.sleep(5)
    l2 = a.start_log(r'C:\Users\BAIWAN\PycharmProjects\AutoTest\specialtest\exception_log\%s.txt' % time.strftime('%H%M%S'))
    time.sleep(5)
    a.stop_log(l2)
    time.sleep(10)
    a.stop_log(l1)