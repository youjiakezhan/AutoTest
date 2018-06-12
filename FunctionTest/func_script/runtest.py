# coding=utf-8
# Auther:"EternalSunshine"
import time

from FunctionTest.func_script.HTMLTestRunner import HTMLTestRunner
from FunctionTest.main import testReport, suit, new_thread


class RunTest(object):
    """启动测试，开始执行测试用例"""
    def run_test(self):
        with open(testReport, 'wb') as f:
            runner = HTMLTestRunner(f, title='双开助手Daily Review自动化测试报告', description='测试结果饼状图展示')
            try:
                runner.run(suit)
            except Exception as e:
                print("加载或执行用例时出错：", e)
            finally:
                new_thread.stop_thread()
                time.sleep(3)
                # appium.quit()
