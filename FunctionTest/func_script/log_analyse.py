# coding=utf-8

from FunctionTest.func_script.func_lib import *


class LogAnalyse(object):
    def catch_anr_and_crash(self):
        for i in os.listdir(os.path.join(BASE_PATH, 'test_data\\logs')):
            with open(os.path.join(BASE_PATH, 'test_data\\logs\\' + i), 'rb') as f:
                for j in f.readlines():
                    if b'anr in' in j:
                        with open(os.path.join(BASE_PATH, 'test_result/anr_log/anr.txt'),
                                  'a') as f1:
                            f1.write(str(j) + '\n')
                    elif b'CrashHandler' in j:
                        with open(os.path.join(BASE_PATH, 'test_result/crash_log/crash.txt'),
                                  'a') as f2:
                            f2.write(str(j) + '\n')


if __name__ == '__main__':
    log_analyse = LogAnalyse()
    log_analyse.catch_anr_and_crash()
