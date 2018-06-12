# coding = UTF-8

import os
import time
from FunctionTest.func_script.func_lib import getinfo, BASE_PATH
APK_PATH = 'Z:\daily_review_SKZS'


class FilePath(object):

    def get_file_path(self):
        for file in os.listdir(APK_PATH):
            file_path = os.path.join(APK_PATH, file)
            if "apk" in file_path and os.path.isfile(file_path):
                return file_path

    def install_seccess(self):
        data = os.popen('adb shell pm list package -3')
        if "com.excelliance.dualaid" in data.read():
            return True

    def install_apk(self):
        os.popen('adb install -r ' + self.get_file_path())

    def monitor(self):
        count = 5
        while True:
            try:
                self.install_apk()
                while count > 0:
                    count -= 1
                    if self.install_seccess():
                        break
                    else:
                        time.sleep(5)
                        print('由于权限原因未能自动安装测试包，请手动进行安装！')
                        continue
                os.popen('move ' + self.get_file_path() + ' ' + os.path.join(BASE_PATH, 'daily_review_files\\apk'))
                break
            except Exception:
                print('没有新的安装包\n本次检测时间：%s' % getinfo.get_time(2))
                time.sleep(3)