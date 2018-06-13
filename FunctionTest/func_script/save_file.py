# coding=utf-8
# Auther:"EternalSunshine"
import os


class SaveFile(object):

    def save_file(self):
        os.popen('move ' + r'C:\Users\BAIWAN\PycharmProjects\AutoTest\FunctionTest\test_result.zip' +
                 ' ' + r'Z:\daily_review_SKZS\daily_review_files\result')
