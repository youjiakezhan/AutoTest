# coding=utf-8
import os

from FunctionTest.func_script.func_lib import BASE_PATH


class CleanWorkspace(object):
    """清理指定文件夹下所有文件"""
    def clean_test_result(self):
        clean_path = os.walk(BASE_PATH + '\\test_result')
        for root, dirs, files in clean_path:
            for file in files:
                if "readme.txt" not in file:
                    os.remove(os.path.join(root, file))


# clean = CleanWorkspace()
# clean.clean_test_result()
