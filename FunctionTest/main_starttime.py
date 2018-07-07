# coding=utf-8
import os
import unittest

from FunctionTest.func_script.HTMLTestRunner_01 import HTMLTestRunner
from FunctionTest.func_script.appium_server_check import AppiumServerCheck
from FunctionTest.func_script.check_and_install_apk import FilePath
from FunctionTest.func_script.clean_workspace import CleanWorkspace
from FunctionTest.func_script.compression import Compression
from FunctionTest.func_script.func_lib import getinfo, BASE_PATH
from FunctionTest.func_script.send_email import EmailSending
from FunctionTest.test_case.starttime import StartTimeTest

# 设置发件人的邮箱地址和邮箱密码
username = input('请输入发件人地址：')
password = input('请输入邮箱密码：')

# 检测daily_review的包并安装(注意：若公盘盘符不符请自行修改之后再运行！)
apk_check = FilePath(apk_path=r'Z:\start_time_SKZS')
apk_check.monitor()

# 初始化appium连接
ap_ser_che = AppiumServerCheck()
ap_ser_che.check_appium_server()

# 装载测试用例
suit = unittest.TestSuite()
suit.addTest(unittest.TestLoader().loadTestsFromTestCase(StartTimeTest))

# 设置生成测试报告路径
testReport = os.path.join(BASE_PATH, 'test_result1\\start_time_report\\双开助手启动时间测试报告%s.html' % getinfo.get_time())

# 执行测试并记录测试报告
with open(testReport, 'wb') as f:
    runner = HTMLTestRunner(stream=f, title='双开助手启动时间自动化测试报告', description='测试结果展示')
    runner.run(suit)

# 结束appium会话
ap_ser_che.stop_appium_server()

# 压缩并保存测试结果(注意：若公盘盘符不符的请自行修改之后再运行！)
compress = Compression(new_file_path=r'Z:\start_time_SKZS\start_time_files\result',
                       dir_path=BASE_PATH + '\\test_result1')
compress.compress_dir()

# 发送测试报告邮件
send_report = EmailSending(username, password, file_path=r'Z:\daily_review_SKZS\daily_review_files\result',
                           html_path=BASE_PATH + '\\test_result1\\report',
                           image_path=BASE_PATH + '\\test_result2\\screenshot')
send_report.screen_shot()
send_report.create_email()

# 初始化工作区
cl = CleanWorkspace()
cl.clean_test_result(BASE_PATH + '\\test_result1')
cl.clean_test_result(BASE_PATH + '\\test_result2')
