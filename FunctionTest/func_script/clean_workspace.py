# coding=utf-8
import os

from FunctionTest.func_script.func_lib import BASE_PATH


class CleanWorkspace(object):
    """清理指定文件夹下所有文件"""
    def clean_test_result(self, path):
        clean_path = os.walk(path)
        for root, dirs, files in clean_path:
            for file in files:
                if "readme.txt" not in file:
                    os.remove(os.path.join(root, file))


if __name__ == '__main__':
    clean = CleanWorkspace()
    clean.clean_test_result(BASE_PATH + '\\test_result')
    clean.clean_test_result(BASE_PATH + '\\test_data')
