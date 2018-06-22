# coding=utf-8
import unittest

from FunctionTest.func_script.func_lib import *


class AddTestcase(unittest.TestCase, AppiumInit, ScreenShot, GetInfo, UserOperation, FindElement,
                  Waiting, PhoneSetting, AppOperation, PopupHandle, CreateThread, Logcat):
    # 以下为用例编写方法和规范,如有不清楚的地方可询问作者(@eternalsunshine)
    # 请按照 test_template 测试用例模板的格式编写测试用例(本架构会自动识别所有以 test 开头的函数并添加为测试用例)
    # 断言设置标准为:完成一个操作后就顺便为该操作添加断言
    # 用户操作已封装在 func_script 目录下的 func_lib.py 内,可在测试用例内部使用self.method(paramater)
    # 编写测试用例前先简单了解下 func_lib.py 内用户操作和其他类方法(不需要全部记下),编写用例过程中可随时翻阅
    # 用例流程:被测功能(对象)--->测试步骤(预期结果)--->用户操作(最好加以注释)--->操作后等待--->操作结果断言(output输出结果)
    # 操作后等待的一点说明:现阶段请使用 self.wait_for() 方法执行等待,其他等待方法(更科学,高效)需完善测试用例编写方案后启用
    def test_template(self):
        """
        导航栏自动展示
        1.清除数据后启动app(启动成功)
        2.等待导航图片自动展示(3秒自动展示下一张,直到第三张为止)
        3.点击“立即体验”按钮(跳转至添加引导页)
        """
        # 点击立即体验按钮
        self.wait_explicit_ele('com.excelliance.dualaid:id/bt_explore', 30, 1)
        self.find_element('com.excelliance.dualaid:id/bt_explore').click()
        self.wait_for(5)
        try:
            self.assertIn('com.excelliance.dualaid:id/first_start_ok', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error001.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/first_start_ok', self.get_xml(), "点击立即体验后页面未跳转")

        """test_template 是一条完整的测试用例,可作为编写用例的模板使用(如有好的意见或建议请联系作者进行沟通完善,谢谢!)"""
