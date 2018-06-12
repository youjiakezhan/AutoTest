# coding=utf-8

import urllib
from FunctionTest.func_script.check_and_install_apk import FilePath
from FunctionTest.func_script.log_analyse import *
# from FunctionTest.func_script.send_email import *
from FunctionTest.func_script.runtest import RunTest
from FunctionTest.func_script.send_email import EmailSending
from FunctionTest.func_script.zip import Zipping
from FunctionTest.test_case.test_SKZS_daily import *

# 检测daily_review的包并安装
apk_check = FilePath()
apk_check.monitor()

# 初始化appium连接
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

# 开启弹窗监控线程
new_thread = CreateThread()
popup_handle = PopupHandle()
thread1 = new_thread.start_thread(popup_handle.sys_win_alert)
thread2 = new_thread.start_thread(popup_handle.app_alert)

# 装载测试用例
suit = unittest.TestSuite()  # 实例化TestSuite套件
suit.addTest(unittest.TestLoader().loadTestsFromTestCase(Cases))  # 装载测试用例Cases

# 设置生成测试报告路径
testReport = os.path.join(BASE_PATH, 'test_result\\report\\双开助手测试报告%s.html' % getinfo.get_time())

# 执行测试并输出测试报告
runtest = RunTest()
runtest.run_test()

# 测试用例执行完毕，分析log
log_analyse = LogAnalyse()
log_analyse.catch_anr_and_crash()

# 压缩测试结果文件夹
yasuo = Zipping()
yasuo.zip_dir()

# 发送测试邮件
send_report = EmailSending()
send_report.create_email()
