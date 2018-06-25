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

    def adb_connect_seccess(self):
        """查看USB是否已连接"""
        text = os.popen('adb devices')
        time.sleep(5)
        if 'device' in text.readlines()[1]:
            return True
        else:
            print('USB未连接')

    def uninstall_apk(self):
        """卸载本机已有双开助手apk"""
        if 'com.excelliance.dualaid.b64' in os.popen('adb shell pm list package -3 | findstr "excelliance"').read():
            os.popen('adb uninstall com.excelliance.dualaid.b64')
        else:
            pass
        if 'com.excelliance.dualaid' in os.popen('adb shell pm list package -3 | findstr "excelliance"').read():
            os.popen('adb uninstall com.excelliance.dualaid')
        else:
            pass

    def install_apk(self):
        """安装daily review包"""
        os.popen('adb install -r ' + self.get_file_path())

    def monitor(self):
        """
        检查本机是否有daily review包同名apk，如果有就删除，如果没有就去指定目录检查，有apk包就执行安装，没有就等待，
        直到安装成功为止，安装完成后将该目录下的安装包移动至存放apk的目录
        """
        if self.adb_connect_seccess() is True:
            self.uninstall_apk()
            time.sleep(2)
            while True:
                try:
                    print('尝试自动安装测试包\n')
                    self.install_apk()
                    time.sleep(20)
                    if 'com.excelliance.dualaid' in os.popen(
                            'adb shell pm list package -3 | findstr "excelliance"').read():
                        print('安装完成，正在配置测试环境...\n')
                        os.popen('move ' + self.get_file_path() + ' ' + os.path.join(self.apk_path,
                                                                                     'daily_review_files\\apk'))
                        break
                    else:
                        print('安装测试包失败，请手动进行安装\n')
                        continue
                except TypeError:
                    print('未检测到双开助手daily review安装包\n本次检测时间：%s\n' % getinfo.get_time(1))
                    time.sleep(10)
        else:
            pass


if __name__ == '__main__':
    fi = FilePath(apk_path=r'Z:\daily_review_SKZS')
    fi.monitor()
