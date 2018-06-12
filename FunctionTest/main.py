# coding=utf-8

import urllib

from FunctionTest.check_and_install_apk import FilePath
from FunctionTest.func_script.log_analyse import *
from FunctionTest.func_script.send_email import *
from FunctionTest.func_script.HTMLTestRunner import HTMLTestRunner
from FunctionTest.test_case.test_SKZS_daily import *
from FunctionTest.func_lib import *


# 检测daily_review的包并安装
apk_check = FilePath()
while True:
    try:
        os.popen('adb install -r ' + apk_check.get_file_path())
        time.sleep(15)
        os.popen('move ' + apk_check.get_file_path() + ' ' + os.path.join(BASE_PATH, 'daily_review_apk'))
        break
    except Exception:
        print('没有新的安装包\n本次检测时间：%s' % getinfo.get_time(2))
        time.sleep(3)


"""初始化appium连接"""
appium = AppiumInit()
getinfo = GetInfo()
aop = AppOperation()
while True:
    try:
        appium.appium_init()
        print("测试前调试")
        time.sleep(2)
        break
    except urllib.error.URLError:
        print("检测到未连接上appium服务器，正在启动appium服务端连接程序，请稍后...")
        os.popen("start appium")
        print("appium服务端已连接，正在进行初始化...")
        time.sleep(5)
aop.force_stop('com.excelliance.dualaid')
"""开启弹窗监控线程"""
new_thread = CreateThread()
popup_handle = PopupHandle()
thread1 = new_thread.start_thread(popup_handle.sys_win_alert)
thread2 = new_thread.start_thread(popup_handle.app_alert)

"""装载测试用例"""
# start_dir = os.path.join(BASE_PATH, 'test_case')
# discover = unittest.defaultTestLoader.discover(start_dir, pattern='test.*.py', top_level_dir=None)
# runner = unittest.TextTestRunner()
# runner.run(discover)
suit = unittest.TestSuite()  # 实例化TestSuite套件
suit.addTest(unittest.TestLoader().loadTestsFromTestCase(Cases))  # 装载测试用例Cases

"""设置生成测试报告路径"""
testReport = os.path.join(BASE_PATH, 'test_result\双开助手测试报告%s.html' % getinfo.get_time())

"""执行测试并输出测试报告"""
with open(testReport, 'wb') as f:
    runner = HTMLTestRunner(f, title='双开助手UI自动化测试报告', description='测试结果展示')
    try:
        runner.run(suit)
    except Exception as e:
        print("加载或执行用例时出错：", e)
    finally:
        new_thread.stop_thread()
        time.sleep(15)
        appium.quit()
        print("测试结束,正在分析测试日志...")
        log_analyse = LogAnalyse()
        log_analyse.catch_anr_and_crash()
        print('日志分析结束')
