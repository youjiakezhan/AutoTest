# coding=utf-8
from FunctionTest.func_script.clean_workspace import CleanWorkspace
from FunctionTest.func_script.func_lib import BASE_PATH
from FunctionTest.func_script.send_email import EmailSending
from FunctionTest.test_case.starttime import StartTimeTest

# 设置发件人的邮箱地址和邮箱密码
username = input('请输入发件人地址：')
password = input('请输入邮箱密码：')

while True:
    # 调用启动时间测试类
    start_time_test = StartTimeTest()
    start_time_test.run_test()

    # 发送测试报告邮件
    send_report = EmailSending(username, password, image_path=BASE_PATH + r'\test_result1\start_time_report')
    send_report.create_email()

    # 初始化工作区
    cl = CleanWorkspace()
    cl.clean_test_result(BASE_PATH + r'\test_result1\start_time_report')
