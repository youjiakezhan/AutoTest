# coding=utf-8
# Auther:"EternalSunshine"
import os


class CleanWorkspace(object):
    def clean_test_result(self):
        clean_path = os.walk(r'C:\Users\BAIWAN\PycharmProjects\AutoTest\FunctionTest\test_result')
        for root, dirs, files in clean_path:
            for file in files:
                if "readme.txt" not in file:
                    os.remove(os.path.join(root, file))


# clean = CleanWorkspace()
# clean.clean_test_result()