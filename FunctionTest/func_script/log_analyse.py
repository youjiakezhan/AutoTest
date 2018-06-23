# coding=utf-8

from FunctionTest.func_script.func_lib import *


class LogAnalyse(object):
    def __init__(self, log_path, anr_path, crash_path):
        self.log_path = log_path
        self.anr_path = anr_path
        self.crash_path = crash_path

    def catch_anr_and_crash(self):
        for i in os.listdir(os.path.join(self.log_path)):
            with open(os.path.join(self.log_path + i), 'rb') as f:
                for j in f.readlines():
                    if b'anr in' in j:
                        with open(os.path.join(self.anr_path),
                                  'a') as f1:
                            f1.write(str(j) + '\n')
                    elif b'CrashHandler' in j:
                        with open(os.path.join(self.crash_path),
                                  'a') as f2:
                            f2.write(str(j) + '\n')


if __name__ == '__main__':
    log_analyse = LogAnalyse(log_path=BASE_PATH + '\\test_result2\\logs',
                             anr_path=BASE_PATH + '\\test_result1\\anr_log\\anr.txt',
                             crash_path=BASE_PATH + '\\test_result1\\crash_log\\crash.txt')
    log_analyse.catch_anr_and_crash()
