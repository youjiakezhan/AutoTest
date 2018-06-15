# coding=utf-8
import os
import time
from zipfile import ZipFile, ZIP_DEFLATED


class Compression(object):
    """压缩文件和文件夹"""

    def __init__(self, result_path, dir_path):
        self.result_path = result_path
        self.dir_path = dir_path

    def compress_dir(self):
        new_file = self.result_path + '\\' + time.strftime('%Y%m%d%H%M%S') + '.zip'
        z = ZipFile(new_file, 'w', ZIP_DEFLATED)
        for root, dirs, files in os.walk(self.dir_path):
            fpath = root.replace(self.dir_path, '')
            fpath = fpath and fpath + os.sep or ''
            for file in files:
                z.write(os.path.join(root, file), fpath + file)
        z.close()


# zip = Compression()
# zip.compress_dir()

