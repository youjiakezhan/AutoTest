# coding = UTF-8

import os

APK_PATH = 'Z:\daily_review_SKZS'


class FilePath(object):

    def get_file_path(self):
        for file in os.listdir(APK_PATH):
            file_path = os.path.join(APK_PATH, file)
            if "apk" in file_path and os.path.isfile(file_path):
                return file_path
