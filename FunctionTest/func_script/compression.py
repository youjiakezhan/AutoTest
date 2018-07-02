# coding=utf-8
import os
import time
from zipfile import ZipFile, ZIP_DEFLATED

from FunctionTest.func_script.func_lib import BASE_PATH
from FunctionTest.func_script.check_and_install_apk import FilePath

fp = FilePath(apk_path=r'Z:\daily_review_SKZS')


class Compression(object):
    """压缩文件和文件夹"""

    def __init__(self, new_file_path=None, dir_path=None):
        self.new_file_path = new_file_path
        self.dir_path = dir_path

    def compress_dir(self):
        # 压缩后文件存放路径
        new_file = self.new_file_path + '\\' + time.strftime('%Y%m%d%H%M%S') + '.zip'
        z = ZipFile(new_file, 'w', ZIP_DEFLATED)
        for root, dirs, files in os.walk(self.dir_path):
            # 去掉父级目录，只压缩指定文件目录的文件夹及内部文件
            fpath = root.replace(self.dir_path, '')
            fpath = fpath and fpath + os.sep or ''
            for file in files:
                z.write(os.path.join(root, file), fpath + file)
        z.close()
        # 保存本次测试apk
        os.popen('move ' + fp.get_file_path() + ' ' + os.path.join(fp.apk_path, 'daily_review_files\\apk'))


if __name__ == '__main__':
    z = Compression(new_file_path=r'C:\Users\BAIWAN\PycharmProjects\AutoTest\FunctionTest',
                    dir_path=BASE_PATH + '\\test_result1')
    z.compress_dir()
