# coding=utf-8
import os
from zipfile import ZipFile, ZIP_DEFLATED


class Zipping(object):
    """压缩文件和文件夹"""

    def zip_dir(self):
        dir_path = r'C:\Users\BAIWAN\PycharmProjects\AutoTest\FunctionTest\test_result'
        new_file = dir_path + '.zip'
        z = ZipFile(new_file, 'w', ZIP_DEFLATED)
        for root, dirs, files in os.walk(dir_path):
            for dir in dirs:
                z.write(os.path.join(root, dir))
            for file in files:
                z.write(os.path.join(root, file))
        z.close()

# zip = Zip()
# zip.zip_dir()
