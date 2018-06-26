# coding=utf-8
import os
import unittest

from FunctionTest.func_script.HTMLTestRunner import HTMLTestRunner
from FunctionTest.func_script.appium_server_check import AppiumServerCheck
from FunctionTest.func_script.check_and_install_apk import FilePath
from FunctionTest.func_script.clean_workspace import CleanWorkspace
from FunctionTest.func_script.compression import Compression
from FunctionTest.func_script.func_lib import getinfo, BASE_PATH, PopupHandle, CreateThread, Logcat
from FunctionTest.func_script.log_analyse import LogAnalyse
from FunctionTest.func_script.send_email import EmailSending
from FunctionTest.test_case.SKZS_daily_review import Cases

# # 设置发件人的邮箱地址和邮箱密码
# username = input('请输入发件人地址：')
# password = input('请输入邮箱密码：')
#
# 监控adb进程，初始化所有adb.exe进程（kill掉）
logcat = Logcat()
logcat.kill_adb(arg=0)

# 检测daily_review的包并安装(注意：若公盘盘符不符请自行修改之后再运行！)
apk_check = FilePath(apk_path=r'Z:\daily_review_SKZS')
apk_check.monitor()
logcat.check_adb()

# 初始化appium连接
ap_ser_che = AppiumServerCheck()
ap_ser_che.check_appium_server()

# 弹窗监控
thread = CreateThread()
popup_handle = PopupHandle()
thread1 = thread.start_thread(popup_handle.sys_win_alert)
# thread2 = thread.start_thread(popup_handle.app_alert)
thread3 = thread.start_thread(popup_handle.android_alert)

# 装载测试用例
suit = unittest.TestSuite()
suit.addTest(unittest.TestLoader().loadTestsFromTestCase(Cases))

# 设置生成测试报告路径
testReport = os.path.join(BASE_PATH, 'test_result1\\report\\双开助手测试报告%s.html' % getinfo.get_time())

# 执行测试并记录测试报告
with open(testReport, 'wb') as f:
    runner = HTMLTestRunner(f, title='双开助手DailyBuild自动化测试报告', description='测试结果饼状图展示')
    runner.run(suit)

# 停止弹窗监控
thread.stop_thread()

# 结束appium会话
ap_ser_che.stop_appium_server()

# 测试用例执行完毕，分析log
log_analyse = LogAnalyse(log_path=BASE_PATH + '\\test_result2\\logs',
                         anr_path=BASE_PATH + '\\test_result1\\anr_log\\anr.txt',
                         crash_path=BASE_PATH + '\\test_result1\\crash_log\\crash.txt')
log_analyse.catch_anr_and_crash()

# 压缩并保存测试结果(注意：若公盘盘符不符的请自行修改之后再运行！)
compress = Compression(new_file_path=r'Z:\daily_review_SKZS\daily_review_files\result',
                       dir_path=BASE_PATH + '\\test_result1')
compress.compress_dir()

# # 发送测试报告邮件
# send_report = EmailSending(username, password, file_path=r'Z:\daily_review_SKZS\daily_review_files\result',
#                            html_path=BASE_PATH + '\\test_result1\\report',
#                            image_path=BASE_PATH + '\\test_result2\\screenshot')
# send_report.screen_shot()
# send_report.create_email()
#
# # 初始化工作区
# cl = CleanWorkspace()
# cl.clean_test_result(BASE_PATH + '\\test_result1')
# cl.clean_test_result(BASE_PATH + '\\test_result2')
