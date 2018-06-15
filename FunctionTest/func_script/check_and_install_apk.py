# coding = UTF-8

import os
import time
from FunctionTest.func_script.func_lib import getinfo


class FilePath(object):

    def __init__(self, apk_path):
        self.apk_path = apk_path

    def get_file_path(self):
        """获取daily review安装包路径"""
        for file in os.listdir(self.apk_path):
            file_path = os.path.join(self.apk_path, file)
            if ".apk" in file_path and os.path.isfile(file_path):
                return file_path

    def install_seccess(self):
        """查看本机是否安装了与daily review包同名的apk"""
        data = os.popen('adb shell pm list package -3')
        if "com.excelliance.dualaid" in data.read():
            return True

    def install_apk(self):
        """安装daily review包"""
        os.popen('adb install -r ' + self.get_file_path())

    def monitor(self):
        """
        检查本机是否有daily review包同名apk，如果有就删除，如果没有就去指定目录检查，有apk包就执行安装，没有就等待，
        直到安装成功为止，安装完成后将该目录下的安装包移动至存放apk的目录
        """
        if self.install_seccess():
            try:
                os.popen('adb uninstall com.excelliance.dualaid')
            except:
                print('卸载老版本失败，请手动卸载...\n')
        while True:
            try:
                self.install_apk()
                while True:
                    if self.install_seccess():
                        print('双开助手daily review包安装完成，开始配置测试环境...\n')
                        break
                    else:
                        print('发现daily review安装包，正在进行安装...\n')
                        time.sleep(15)
                os.popen('move ' + self.get_file_path() + ' ' + os.path.join(self.apk_path, 'daily_review_files\\apk'))
                break
            except Exception:
                print('未检测到双开助手daily review安装包\n本次检测时间：%s\n' % getinfo.get_time(2))
                time.sleep(10)


# fi = FilePath()
# fi.monitor()