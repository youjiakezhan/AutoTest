# coding=utf-8
import unittest
from FunctionTest.func_script.HTMLTestRunner import HTMLTestRunner
from FunctionTest.func_script.appium_server_check import AppiumServerCheck
from FunctionTest.func_script.check_and_install_apk import FilePath
from FunctionTest.func_script.clean_workspace import CleanWorkspace
from FunctionTest.func_script.log_analyse import *
from FunctionTest.func_script.compression import Compression
from FunctionTest.test_case.SKZS_daily_review import Cases

# 检测daily_review的包并安装
apk_check = FilePath()
apk_check.monitor()

# 初始化appium连接
ap_ser_che = AppiumServerCheck()
ap_ser_che.check_appium_server()

# 弹窗监控
thread = CreateThread()
popup_handle = PopupHandle()
thread1 = thread.start_thread(popup_handle.sys_win_alert)
thread2 = thread.start_thread(popup_handle.app_alert)
thread3 = thread.start_thread(popup_handle.android_alert)

# 装载测试用例
suit = unittest.TestSuite()
suit.addTest(unittest.TestLoader().loadTestsFromTestCase(Cases))

# 设置生成测试报告路径
testReport = os.path.join(BASE_PATH, 'test_result\\report\\双开助手测试报告%s.html' % getinfo.get_time())

# 执行测试并记录测试报告
with open(testReport, 'wb') as f:
    runner = HTMLTestRunner(f, title='双开助手版本迭代自动化测试报告', description='测试结果饼状图展示')
    runner.run(suit)

# 停止弹窗监控
thread.stop_thread()

# 结束appium会话
ap_ser_che.stop_appium_server()

# 测试用例执行完毕，分析log
log_analyse = LogAnalyse()
log_analyse.catch_anr_and_crash()

# 压缩并保存测试结果
compress = Compression()
compress.compress_dir()

# 初始化工作区
ask = input('是否清空测试数据:(输入y/Y/yes/YES/Yes清除测试数据)')
if ask == 'yes' or 'y' or 'Y' or 'YES' or 'Yes':
    cl = CleanWorkspace()
    cl.clean_test_result()
