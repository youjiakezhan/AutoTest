# coding=utf-8
import os
import time
from zipfile import ZipFile, ZIP_DEFLATED


class Compression(object):
    """压缩文件和文件夹"""
    result_path = r'Z:\daily_review_SKZS\daily_review_files\result'

    def compress_dir(self):
        dir_path = r'C:\Users\BAIWAN\PycharmProjects\AutoTest\FunctionTest\test_result'
        new_file = self.result_path + '\\' + time.strftime('%Y%m%d%H%M%S') + '.zip'
        z = ZipFile(new_file, 'w', ZIP_DEFLATED)
        for root, dirs, files in os.walk(dir_path):
            fpath = root.replace(dir_path, '')
            fpath = fpath and fpath + os.sep or ''
            for file in files:
                z.write(os.path.join(root, file), fpath + file)
        z.close()


# zip = Compression()
# zip.compress_dir()

