# coding=utf-8
import unittest

from FunctionTest.func_script.func_lib import *


class Cases(unittest.TestCase, AppiumInit, ScreenShot, GetInfo, UserOperation, FindElement,
            Waiting, PhoneSetting, AppOperation, PopupHandle, CreateThread, Logcat, Delete):

    def setUp(self):
        self.wait_for(2)
        print("用例开始时间:", self.get_time())
        self.start_logcat(log_path)
        self.start_app()

    def tearDown(self):
        print("用例结束时间:", self.get_time())
        self.kill_adb(arg=1)
        self.clear_app()

    def test001(self):
        """
        导航栏自动展示
        1.清除数据后启动app
        2.等待导航图片自动展示
        3.点击“立即体验”按钮
        """
        # 对点击立即体验后的结果断言
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

    def test002(self):
        """
        添加引导页选择微信,进入主界面,启动双开微信
        1.启动app至添加引导页
        2.只选择微信复选框
        3.点击“开启”按钮
        4.点击back
        5.点击微信图标启动微信
        """
        try:
            self.set_app_status1()
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'settingerror002.png')

        # 对操作复选框后的结果断言
        self.find_elements('com.excelliance.dualaid:id/check_box_01')[1].click()
        try:
            self.assertTrue(self.find_elements('com.excelliance.dualaid:id/check_box_01')[1])
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error002_1.png')
        finally:
            self.assertTrue(self.find_elements('com.excelliance.dualaid:id/check_box_01')[1], '复选框操作失败')

        # 对点击开启按钮后的结果断言
        self.find_element('com.excelliance.dualaid:id/first_start_ok').click()
        self.wait_for(5)
        try:
            self.assertIn('com.excelliance.dualaid:id/tv_app_add', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error002_2.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/tv_app_add', self.get_xml(), '点击开启按钮后跳转失败')

        # 对启动双开微信操作的结果断言
        self.back()
        self.wait_for(1)
        self.find_elements('com.excelliance.dualaid:id/root')[0].click()
        self.wait_for(5)
        try:
            self.assertIn('登录', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error002_3.png')
        finally:
            self.assertIn('登录', self.get_xml(), "启动双开微信失败")

    def test003(self):
        """
        从主界面点击添加推荐应用(微信)并启动
        1.启动app至主界面
        2.点击主界面上的推荐添加应用微信
        3.选择微信并点击启动
        """
        try:
            self.set_app_status2()
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'settingerror003.png')

        # 对添加推荐微信的操作结果断言
        self.find_elements('com.excelliance.dualaid:id/root')[0].click()
        self.wait_for(5)
        try:
            self.assertIn('com.excelliance.dualaid:id/tv_app_add', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error003_1.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/tv_app_add', self.get_xml(), '添加推荐微信失败')

        # 对启动双开微信操作的结果断言
        self.back()
        self.wait_for(1)
        self.find_elements('com.excelliance.dualaid:id/root')[0].click()
        self.wait_for(5)
        try:
            self.assertIn('注册', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error003_2.png')
        finally:
            self.assertIn('注册', self.get_xml(), "启动双开微信失败")

    def test004(self):
        """
        从主界面添加按钮进入添加应用列表页添加一款应用(微信)并从主界面启动
        1.启动app至主界面
        2.点击添加按钮
        3.选择微信并点击添加
        4.点击微信图标启动微信
        """
        try:
            self.set_app_status2()
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'settingerror004.png')

        # 对点击添加按钮的结果断言
        self.find_element('com.excelliance.dualaid:id/add_but').click()
        self.wait_for(5)
        try:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/add_game_tv_back').is_displayed())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error004_1.png')
        finally:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/add_game_tv_back').is_displayed(),
                            '点击添加按钮跳转失败')

        # 对点击添加微信的结果断言
        self.find_elements('com.excelliance.dualaid:id/add_game_btn')[0].click()
        self.wait_for(5)
        try:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/tv_app_add').is_displayed())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error004_2.png')
        finally:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/tv_app_add').is_displayed(),
                            '点击添加微信失败')

        # 对点击启动微信的结果断言
        self.back()
        self.wait_for(2)
        self.find_elements('com.excelliance.dualaid:id/root')[0].click()
        self.wait_for(3)
        try:
            self.assertIn('登录', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'settingerror004_3.png')
        finally:
            self.assertIn('登录', self.get_xml(), '点击启动微信失败')

    def test005(self):
        """
        非VIP账号登录
        1.启动app至添加引导页
        2.点击登录/注册
        3.输入正确的非VIP账号
        4.点击下一步
        5.输入正确的密码
        6.点击登录
        7.点击back
        """
        try:
            self.set_app_status1()
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'test/settingerror005.png')

        # 对点击登录/注册按钮后的结果断言
        self.find_element('com.excelliance.dualaid:id/tv_login_in').click()
        self.wait_for(5)
        try:
            self.assertIn('com.excelliance.dualaid:id/btn_next_step', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error005_1.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/btn_next_step', self.get_xml(), '点击登录/注册跳转失败')

        # 对输入账号后的下一步按钮状态断言
        self.user_input('18501701705')
        try:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/btn_next_step').is_enabled())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error005_2.png')
        finally:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/btn_next_step').is_enabled(),
                            '下一步按钮状态未改变')

        # 对点击下一步后的结果断言
        self.find_element('com.excelliance.dualaid:id/btn_next_step').click()
        self.wait_for(5)
        try:
            self.assertIn('com.excelliance.dualaid:id/tv_login', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error005_3.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/tv_login', self.get_xml(), '点击下一步跳转失败')

        # 对输入密码后的登录按钮状态断言
        self.user_input('000000')
        try:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/tv_login').is_enabled())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error005_4.png')
        finally:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/tv_login').is_enabled(),
                            '登录按钮状态未改变')

        # 对点击登录按钮的结果断言
        self.find_element('com.excelliance.dualaid:id/tv_login').click()
        self.wait_for(5)
        try:
            self.assertTrue(
                self.get_current_activity() == 'com.excelliance.kxqp.ui.MainActivity')
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error005_5.png')
        finally:
            self.assertTrue(
                self.get_current_activity() == 'com.excelliance.kxqp.ui.MainActivity', '登录失败')

    def test006(self):
        """
        退出登录
        1.启动app至已登陆状态的主界面
        2.点击个人中心图标
        3.点击头像图标
        4.点击退出按钮
        5.选择确认退出并点击
        """
        try:
            self.set_app_status6()
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'settingerror006.png')

        # 对点击个人中心按钮的结果断言
        self.find_element('com.excelliance.dualaid:id/iv_icon').click()
        self.wait_for(3)
        try:
            self.assertIn('com.excelliance.dualaid:id/rl_update', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error006_1.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/rl_update', self.get_xml(), '点击个人中心按钮跳转失败')

        # 对点击个人中心头像按钮的结果断言
        self.find_element('com.excelliance.dualaid:id/iv_icon').click()
        self.wait_for(3)
        try:
            self.assertIn('com.excelliance.dualaid:id/tv_login_out', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error006_2.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/tv_login_out', self.get_xml(), '点击个人中心头像按钮跳转失败')

        # 对点击退出登录按钮的结果断言
        self.find_element('com.excelliance.dualaid:id/tv_login_out').click()
        self.wait_for(2)
        try:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/bt_sure').is_displayed())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error006_3.png')
        finally:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/bt_sure').is_displayed(),
                            '点击退出登录按钮弹窗失败')

        # 对点确认退出按钮的结果断言
        self.find_element('com.excelliance.dualaid:id/bt_sure').click()
        self.wait_for(2)
        try:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/btn_next_step').is_displayed())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error006_4.png')
        finally:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/btn_next_step').is_displayed(),
                            '点击确认退出按钮跳转失败')

    def test007(self):
        """
        登录VIP账户
        1.启动app至添加引导页
        2.点击登录/注册
        3.输入正确的VIP账号
        4.点击下一步
        5.输入正确的密码
        6.点击登录
        7.点击back
        """
        try:
            self.set_app_status1()
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'settingerror007.png')

        # 对点击登录/注册按钮后的结果断言
        self.find_element('com.excelliance.dualaid:id/tv_login_in').click()
        self.wait_for(5)
        try:
            self.assertIn('com.excelliance.dualaid:id/btn_next_step', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error007_1.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/btn_next_step', self.get_xml(), '点击登录/注册跳转失败')

        # 对输入账号后的下一步按钮状态断言
        self.user_input('123456789')
        try:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/btn_next_step').is_enabled())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error007_2.png')
        finally:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/btn_next_step').is_enabled(),
                            '下一步按钮状态未改变')

        # 对点击下一步后的结果断言
        self.find_element('com.excelliance.dualaid:id/btn_next_step').click()
        self.wait_for(5)
        try:
            self.assertIn('com.excelliance.dualaid:id/tv_login', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error007_3.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/tv_login', self.get_xml(), '点击下一步跳转失败')

        # 对输入密码后的登录按钮状态断言
        self.user_input('111111')
        try:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/tv_login').is_enabled())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error007_4.png')
        finally:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/tv_login').is_enabled(),
                            '登录按钮状态未改变')

        # 对点击登录按钮后页面跳转的断言
        self.find_element('com.excelliance.dualaid:id/tv_login').click()
        self.wait_for(5)
        try:
            self.assertTrue(
                self.get_current_activity() == 'com.excelliance.kxqp.ui.MainActivity')
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error007_5.png')
        finally:
            self.assertTrue(
                self.get_current_activity() == 'com.excelliance.kxqp.ui.MainActivity',
                '登录失败')

        self.back()
        self.wait_for(1)

    def test008(self):
        """
        登录VIP账户后,单独添加应用(微信)至第二空间并启动
        1.启动app至状态（登陆VIP账号后的主界面）
        2.点击添加按钮
        3.选择微信并点击添加
        4.选择添加至第二空间
        5.点击微信图标启动微信
        """
        try:
            self.set_app_status6()
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'settingerror008.png')

        # 对点击添加按钮的结果断言
        self.find_element('com.excelliance.dualaid:id/add_but').click()
        self.wait_for(5)
        try:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/add_game_tv_back').is_displayed())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error008_1.png')
        finally:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/add_game_tv_back').is_displayed(),
                            '点击添加按钮跳转失败')

        # 对点击添加微信的结果断言
        self.find_elements('com.excelliance.dualaid:id/add_game_btn')[0].click()
        self.wait_for(3)
        try:
            self.assertIn('请选择空间添加', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error008_2.png')
        finally:
            self.assertIn('请选择空间添加', self.get_xml(), '点击添加微信失败')

        # 对选择添加微信的结果断言
        self.find_elements('com.excelliance.dualaid:id/root')[3].click()
        self.wait_for(3)
        try:
            self.assertIn('微信', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error008_3.png')
        finally:
            self.assertIn('微信', self.get_xml(), '选择添加第二空间微信失败')

        # 对点击启动微信的结果断言
        self.find_elements('com.excelliance.dualaid:id/root')[2].click()
        self.wait_for(3)
        try:
            self.assertIn('登录', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error008_4.png')
        finally:
            self.assertIn('登录', self.get_xml(), '点击启动微信失败')

    def test009(self):
        """
        登录VIP账户后,在平铺界面添加一款应用(微信)并启动
        1.首次启动app至状态（登录VIP账号后的平铺界面）
        2.点击添加按钮
        3.选择微信并点击添加
        4.点击微信图标启动微信
        """
        try:
            self.set_app_status7()
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'settingerror009.png')

        # 对点击添加按钮的结果断言
        self.find_element('com.excelliance.dualaid:id/add_but').click()
        self.wait_for(5)
        try:
            self.assertIn('com.excelliance.dualaid:id/add_game_tv_back', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error009_1.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/add_game_tv_back', self.get_xml(), '点击添加按钮跳转失败')

        # 对点击添加微信结果的断言
        self.find_elements('com.excelliance.dualaid:id/add_game_btn')[0].click()
        self.wait_for(3)
        try:
            self.assertIn('微信', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error009_2.png')
        finally:
            self.assertIn('微信', self.get_xml(), '点击添加微信失败')

        # 对点击启动微信的结果断言
        self.find_elements('com.excelliance.dualaid:id/root')[1].click()
        self.wait_for(5)
        try:
            self.assertIn('登录', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error009_3.png')
        finally:
            self.assertIn('登录', self.get_xml(), '点击启动微信失败')

    def test010(self):
        """
        登录VIP账户,先后添加一款应用(微信)至第一,第二空间,再启动第二空间内的应用
        1.启动app至状态（登录VIP账号后的主界面）
        2.点击空间切换按钮
        3.点击添加按钮
        4.选择微信并点击添加
        5.点击添加按钮
        6.选择微信并点击添加
        7.点击第二空间微信图标启动微信
        """
        try:
            self.set_app_status7()
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'settingerror010.png')

        # 对点击空间切换按钮的结果断言
        self.find_element('com.excelliance.dualaid:id/ib_lock').click()
        self.wait_for(5)
        try:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/tv_bt_add').is_displayed())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error010_1.png')
        finally:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/tv_bt_add').is_displayed(),
                            '点击空间切换按钮跳转失败')

        # 对点击添加按钮的结果断言
        self.back()
        self.wait_for(3)

        self.find_element('com.excelliance.dualaid:id/add_but').click()
        self.wait_for(5)
        try:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/add_game_tv_back').is_displayed())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error010_2.png')
        finally:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/add_game_tv_back').is_displayed(),
                            '点击添加按钮跳转失败')

        # 对点击添加微信的结果断言
        self.find_elements('com.excelliance.dualaid:id/add_game_btn')[0].click()
        self.wait_for(5)

        self.find_elements('com.excelliance.dualaid:id/root')[1].click()
        self.wait_for(5)
        try:
            self.assertIn('com.excelliance.dualaid:id/tv_app_add', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error010_3.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/tv_app_add', self.get_xml(), '点击添加微信失败')

        # 对点击添加按钮的结果断言
        self.back()
        self.wait_for(3)
        self.find_element('com.excelliance.dualaid:id/add_but').click()
        self.wait_for(5)
        try:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/add_game_tv_back').is_displayed())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error010_4.png')
        finally:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/add_game_tv_back').is_displayed(),
                            '点击添加按钮跳转失败')

        # 对点击添加微信的结果断言
        self.find_elements('com.excelliance.dualaid:id/add_game_btn')[0].click()
        self.wait_for(5)
        try:
            self.assertTrue(self.get_xml().count('微信') == 2)
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error010_5.png')
        finally:
            self.assertTrue(self.get_xml().count('微信') == 2, '点击添加微信失败')

        # 对点击启动微信的结果断言
        self.find_elements('com.excelliance.dualaid:id/root')[3].click()
        self.wait_for(5)
        try:
            self.assertIn('登录', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error010_6.png')
        finally:
            self.assertIn('登录', self.get_xml(), '点击启动微信失败')

    def test011(self):
        """
        登录VIP账户,在平铺界面先后添加一款应用(微信)至第一,第二空间,再启动第二空间内的应用
        1.首次启动app至状态（登录VIP账号后的平铺界面）
        2.点击添加按钮
        3.选择微信并点击添加
        4.点击添加按钮
        5.选择微信并点击添加
        6.点击微信2图标启动微信
        """
        try:
            self.set_app_status7()
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'settingerror011.png')

        # 对点击添加按钮的结果断言
        self.find_element('com.excelliance.dualaid:id/add_but').click()
        self.wait_for(5)
        try:
            self.assertIn('com.excelliance.dualaid:id/add_game_tv_back', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error011_1.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/add_game_tv_back', self.get_xml(), '点击添加按钮跳转失败')

        # 对点击添加微信的结果断言
        self.find_elements('com.excelliance.dualaid:id/add_game_btn')[0].click()
        self.wait_for(5)
        try:
            self.assertTrue(self.get_xml().count('微信') == 1)
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error011_2.png')
        finally:
            self.assertTrue(self.get_xml().count('微信') == 1, '点击添加微信失败')

        # 对点击添加按钮的结果断言
        self.find_element('com.excelliance.dualaid:id/add_but').click()
        self.wait_for(5)
        try:
            self.assertIn('com.excelliance.dualaid:id/add_game_tv_back', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error011_3.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/add_game_tv_back', self.get_xml(), '点击添加按钮跳转失败')

        # 对点击添加微信的结果断言
        self.find_elements('com.excelliance.dualaid:id/add_game_btn')[0].click()
        self.wait_for(5)
        try:
            self.assertTrue(self.get_xml().count('微信') == 2)
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error011_4.png')
        finally:
            self.assertTrue(self.get_xml().count('微信') == 2, '点击添加微信失败')

        # 对点击启动微信的结果断言
        self.find_elements('com.excelliance.dualaid:id/root')[2].click()
        self.wait_for(5)
        try:
            self.assertIn('登录', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error011_5.png')
        finally:
            self.assertIn('登录', self.get_xml(), '点击启动微信失败')

    def test012(self):
        """
        主界面添加一款应用(微信),长按弹出菜单的遍历
        1.首次启动app至状态(未登录账号的主界面)
        2.点击推荐添加应用微信图标
        3.点击back
        4.长按微信图标
        5.选择删除应用按钮并点击
        6.选择删除按钮并点击
        """
        try:
            self.set_app_status2()
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'settingerror012.png')

        # 对添加推荐微信的操作结果断言
        self.find_elements('com.excelliance.dualaid:id/root')[0].click()
        self.wait_for(5)
        try:
            self.assertIn('com.excelliance.dualaid:id/tv_app_add', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error012_1.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/tv_app_add', self.get_xml(), '添加推荐微信失败')

        # 对长按操作的结果断言
        self.back()
        self.wait_for(1)
        self.long_press(self.find_elements('com.excelliance.dualaid:id/root')[0])
        self.wait_for()
        try:
            self.assertIn('com.excelliance.dualaid:id/rootView', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error012_2.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/rootView', self.get_xml(), '主界面长按应用图标弹出菜单失败')

        # 点击桌面图标按钮
        self.find_element('com.excelliance.dualaid:id/item_pop_icon_relative').click()
        self.wait_for()
        try:
            self.assertIn('com.excelliance.dualaid:id/dialog_main', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error012_3.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/dialog_main', self.get_xml(), '点击桌面图标按钮未弹窗')

        # 点击弹窗右上角“X”号
        self.find_element('com.excelliance.dualaid:id/dialog_image_back').click()
        self.wait_for()
        try:
            self.assertNotIn('com.excelliance.dualaid:id/dialog_main', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error012_4.png')
        finally:
            self.assertNotIn('com.excelliance.dualaid:id/dialog_main', self.get_xml(), '点击弹窗右上角“X”号，弹窗未消失')

        # 点击移动位置按钮
        self.long_press(self.find_elements('com.excelliance.dualaid:id/root')[0])
        self.wait_for()
        self.find_element('com.excelliance.dualaid:id/item_pop_move_relative').click()
        try:
            self.assertTrue(self.is_toast_exist('长按拖动图标'))
            self.assertIn('完成', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error012_5.png')
        finally:
            self.assertTrue(self.is_toast_exist('长按拖动图标'), '点击位置移动未起作用')
            self.assertIn('完成', self.get_xml(), '点击位置移动未起作用')

        # 点击完成按钮
        self.find_element('com.excelliance.dualaid:id/ib_menuorcontent').click()
        self.wait_for(1)
        try:
            self.assertNotIn('完成', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error012_6.png')
        finally:
            self.assertNotIn('完成', self.get_xml(), '点击完成按钮未起作用')

        # 点击图标伪装按钮
        self.long_press(self.find_elements('com.excelliance.dualaid:id/root')[0])
        self.wait_for()
        self.find_element('com.excelliance.dualaid:id/item_pop_custom_relative').click()
        self.wait_for()
        try:
            self.assertIn('com.excelliance.dualaid:id/dialog_main', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error012_7.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/dialog_main', self.get_xml(), '点击图标伪装未弹窗')

        # 点击弹窗右上角“X”号
        self.find_element('com.excelliance.dualaid:id/dialog_image_back').click()
        self.wait_for()
        try:
            self.assertNotIn('com.excelliance.dualaid:id/dialog_main', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error012_8.png')
        finally:
            self.assertNotIn('com.excelliance.dualaid:id/dialog_main', self.get_xml(), '关闭弹窗失败')

        # 点击一键修复
        self.long_press(self.find_elements('com.excelliance.dualaid:id/root')[0])
        self.wait_for()
        self.find_element('com.excelliance.dualaid:id/item_pop_repair_relative').click()

        try:
            self.assertTrue(self.is_toast_exist('修复成功'))
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error012_9.png')
        finally:
            self.assertTrue(self.is_toast_exist('修复成功'), '一键修复失败')

        # 点击删除应用按钮
        self.long_press(self.find_elements('com.excelliance.dualaid:id/root')[0])
        self.wait_for()
        self.find_element('com.excelliance.dualaid:id/item_pop_delete_relative').click()
        self.wait_for()
        try:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/tv_left').is_displayed())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error012_10.png')
        finally:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/tv_left').is_displayed(),
                            '点击删除应用按钮操作失败')

        # 对删除双开微信的结果断言
        self.find_element('com.excelliance.dualaid:id/tv_left').click()
        self.wait_for(3)
        try:
            self.assertTrue(self.get_xml().count('微信') == 0)
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error012_11.png')
        finally:
            self.assertTrue(self.get_xml().count('微信') == 0, '删除双开微信失败')

    def test013(self):
        """
        登录VIP账户后,在平铺界面添加一款应用(微信),长按该应用图标并拖动以遍历顶部三个隐藏功能区域
        1.首次启动app至状态(登录VIP账号后的平铺界面)
        2.长按微信图标
        3.拖动微信图标至删除区域
        4.选择删除
        """
        try:
            self.set_app_status7()
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'settingerror013.png')

        # 对点击添加按钮的结果断言
        self.find_element('com.excelliance.dualaid:id/add_but').click()
        self.wait_for(5)
        try:
            self.assertIn('com.excelliance.dualaid:id/add_game_tv_back', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error013_1.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/add_game_tv_back', self.get_xml(), '点击添加按钮跳转失败')

        # 对点击添加微信的结果断言
        self.find_elements('com.excelliance.dualaid:id/add_game_btn')[0].click()
        self.wait_for(5)
        try:
            self.assertTrue(self.get_xml().count('微信') == 1)
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error013_2.png')
        finally:
            self.assertTrue(self.get_xml().count('微信') == 1, '点击添加微信失败')

        # 拖动微信至伪装区域
        self.drag_and_drop(self.find_elements('com.excelliance.dualaid:id/root')[1],
                           self.find_element('//*[@text="双开助手"]'))
        self.wait_for()
        try:
            self.assertIn('com.excelliance.dualaid:id/dialog_main', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error013_3.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/dialog_main', self.get_xml(), '拖动图标至伪装区域操作失败')

        # 点击弹窗右上角的“x”关闭弹窗
        self.find_element('com.excelliance.dualaid:id/dialog_image_back').click()
        self.wait_for()
        try:
            self.assertNotIn('com.excelliance.dualaid:id/dialog_main', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error013_4.png')
        finally:
            self.assertNotIn('com.excelliance.dualaid:id/dialog_main', self.get_xml(), '关闭弹窗失败')

        # 拖动微信图标至添加桌面区域
        self.drag_and_drop(self.find_elements('com.excelliance.dualaid:id/root')[1],
                           self.find_element('com.excelliance.dualaid:id/ib_lock'))
        self.wait_for()
        try:
            self.assertIn('com.excelliance.dualaid:id/dialog_main', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error013_5.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/dialog_main', self.get_xml(), '拖动图标至添加桌面区域操作失败')

        # 点击弹窗右上角的“x”关闭弹窗
        self.find_element('com.excelliance.dualaid:id/dialog_image_back').click()
        self.wait_for()
        try:
            self.assertNotIn('com.excelliance.dualaid:id/dialog_main', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error013_6.png')
        finally:
            self.assertNotIn('com.excelliance.dualaid:id/dialog_main', self.get_xml(), '关闭弹窗失败')

        # 对拖动删除微信的结果断言
        self.drag_and_drop(self.find_elements('com.excelliance.dualaid:id/root')[1],
                           self.find_elements('com.excelliance.dualaid:id/root')[0])
        self.wait_for()
        try:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/tv_left').is_displayed())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error013_7.png')
        finally:
            self.assertTrue(self.find_element('com.excelliance.dualaid:id/tv_left').is_displayed(),
                            '拖动删除微信按钮操作失败')

        # 对删除双开微信的结果断言
        self.find_element('com.excelliance.dualaid:id/tv_left').click()
        self.wait_for()
        try:
            self.assertTrue(self.get_xml().count('微信') == 0)
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error013_4.png')
        finally:
            self.assertTrue(self.get_xml().count('微信') == 0, '删除双开微信失败')

    def test014(self):
        """
        主界面长按数据迁移图标并在弹出框内选择删除该图标
        1.启动app至状态（未登录账号的主界面）
        2.长按换机数据迁移图标
        3.选择删除按钮并点击
        """
        try:
            self.set_app_status2()
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'settingerror014.png')

        # 对长按换机数据迁移图标的结果断言
        self.long_press(self.find_element('//*[@text="换机数据迁移"]'))
        self.wait_for(3)
        try:
            self.assertIn('com.excelliance.dualaid:id/ll_dialog', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error0114_1.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/ll_dialog', self.get_xml(), '长按换机数据迁移图标弹窗失败')

        # 对点击删除按钮的结果断言
        self.find_element('com.excelliance.dualaid:id/tv_left').click()
        self.wait_for(3)
        try:
            self.assertNotIn('数据迁移', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error0114_2.png')
        finally:
            self.assertNotIn('数据迁移', self.get_xml(), '点击删除按钮操作失败')

    def test015(self):
        """
        支付宝支付前提下,点击确认支付按钮
        1.启动app至状态（登录非VIP账号的个人中心界面）
        2.点击开通VIP会员按钮
        3.点击确认支付按钮
        """
        try:
            self.set_app_status5()
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'settingerror015.png')

        # 对点击开通VIP会员按钮结果断言
        self.find_element('com.excelliance.dualaid:id/rl_open_vip').click()
        self.wait_for(3)
        try:
            self.assertIn('com.excelliance.dualaid:id/pay_nat_title', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error015_1.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/pay_nat_title', self.get_xml(), '点击开通VIP会员按钮跳转失败')

        # 对点击确认支付的结果断言
        self.find_element('com.excelliance.dualaid:id/tv_sure_for_pay').click()
        self.wait_for(10)
        try:
            self.assertTrue(self.get_current_activity() != 'com.excelliance.kxqp.pay.ali.PayMoreCountsActivity')
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error015_2.png')
        finally:
            self.assertTrue(self.get_current_activity() != 'com.excelliance.kxqp.pay.ali.PayMoreCountsActivity',
                            '点击确认支付跳转失败')

    def test016(self):
        """
        选择微信支付,点击确认支付按钮
        1.启动app至状态（登录非VIP账号的个人中心界面）
        2.点击开通VIP会员按钮
        3.下滑找到微信支付并选择该支付方式
        4.点击确认支付按钮
        """
        try:
            self.set_app_status5()
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'settingerror016.png')

        # 对点击开通VIP会员按钮结果断言
        self.find_element('com.excelliance.dualaid:id/rl_open_vip').click()
        self.wait_for(3)
        try:
            self.assertIn('com.excelliance.dualaid:id/pay_nat_title' or '确认付款', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error016_1.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/pay_nat_title' or '确认付款', self.get_xml(), '点击开通VIP会员按钮跳转失败')

        # 对上滑查找并选择微信支付方式的结果断言
        self.swipe_up()
        self.wait_for(2)
        self.find_elements('com.excelliance.dualaid:id/iv_item')[1].click()
        self.wait_for(1)
        try:
            self.assertTrue(self.find_elements('com.excelliance.dualaid:id/iv_item')[1].is_displayed())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error016_2.png')
        finally:
            self.assertTrue(self.find_elements('com.excelliance.dualaid:id/iv_item')[1].is_displayed(),
                            '切换支付方式失败')

        # 对点击确认支付的结果断言
        self.find_element('com.excelliance.dualaid:id/tv_sure_for_pay').click()
        self.wait_for(10)
        try:
            self.assertIn('登录' or '立即支付', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error016_3.png')
        finally:
            self.assertIn('登录' or '立即支付', self.get_xml(), '点击确认支付跳转失败')

    def test017(self):
        """
        免注册登录按钮
        1.启动app至状态（添加引导页）
        2.点击登录/注册按钮
        3.点击免注册登录
        """
        try:
            self.set_app_status1()
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'settingerror017.png')

        # 对点击登录/注册按钮后的结果断言
        self.find_element('com.excelliance.dualaid:id/tv_login_in').click()
        self.wait_for(5)
        try:
            self.assertIn(
                'com.excelliance.dualaid:id/btn_next_step' and 'com.excelliance.dualaid:id/tv_quick_login',
                self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error017_1.png')
        finally:
            self.assertIn(
                'com.excelliance.dualaid:id/btn_next_step' and 'com.excelliance.dualaid:id/tv_quick_login',
                self.get_xml(), '点击登录/注册跳转失败')

        # 对点击免注册登录按钮的结果断言
        self.find_element('com.excelliance.dualaid:id/tv_quick_login').click()
        self.wait_for(5)
        try:
            self.assertIn('com.excelliance.dualaid:id/umcsdk_smscode_btn' or '本机号码一键登录', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error017_2.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/umcsdk_smscode_btn' or '本机号码一键登录', self.get_xml(),
                          '点击免注册登录跳转失败（可能没安装手机卡）')

    def test018(self):
        """
        未登录情况下的个人中心按钮遍历
        1.启动app至状态（未登录时的个人中心页）
        2.点击消息按钮
        3.点击返回按钮
        4.点击开通VIP会员
        5.点击返回
        6.点击我的优惠券
        7.点击back
        8.点击邀请与兑奖
        9.点击返回
        10.点击应用加锁
        11.点击返回
        12.点击内存管理
        13.点击返回
        14.点击一键全部修复
        15.点击确认
        16.点击一键全部修复
        17.点击暂不
        18.点击更多高级设置
        19.点击返回
        20.点击主题换肤
        21.选择其他主题
        22.点击返回
        23.点击版本更新
        24.点击返回
        25.点击帮助与反馈
        26.点击返回
        27.点击关于
        28.点击返回
        """
        try:
            self.set_app_status2()
            self.find_element('com.excelliance.dualaid:id/iv_icon').click()
            self.wait_for(3)
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'settingerror018.png')

        # 点击消息中心的断言
        self.find_element('com.excelliance.dualaid:id/iv_notification_center').click()
        self.wait_for(2)
        try:
            self.assertIn('com.excelliance.dualaid:id/iv_edit', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error018_1.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/iv_edit', self.get_xml(), '点击消息中心跳转失败')

        # 点击返回按钮的断言
        self.find_element('com.excelliance.dualaid:id/iv_back').click()
        self.wait_for(2)
        try:
            self.assertIn('com.excelliance.dualaid:id/iv_icon', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error018_2.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/iv_icon', self.get_xml(), '点击返回按钮跳转失败')

        # 点击开通VIP会员的断言
        self.find_element('com.excelliance.dualaid:id/rl_open_vip').click()
        self.wait_for(2)
        try:
            self.assertIn('com.excelliance.dualaid:id/tv_free_trial', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error018_3.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/tv_free_trial', self.get_xml(), '点击开通VIP会员跳转失败')

        # 点击返回按钮的断言
        self.find_element('com.excelliance.dualaid:id/pay_nav_back').click()
        self.wait_for(2)
        try:
            self.assertIn('com.excelliance.dualaid:id/iv_icon', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error018_4.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/iv_icon', self.get_xml(), '点击返回按钮跳转失败')

        # 点击我的优惠券断言
        self.find_element('com.excelliance.dualaid:id/rl_my_ticket').click()
        self.wait_for(2)
        try:
            self.assertIn('com.excelliance.dualaid:id/ll_dialog', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error018_5.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/ll_dialog', self.get_xml(), '点击我的优惠券跳转失败')

        # back操作的断言
        self.back()
        self.wait_for(2)
        try:
            self.assertIn('com.excelliance.dualaid:id/iv_icon', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error018_6.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/iv_icon', self.get_xml(), '点击back跳转失败')

        # 点击邀请与兑奖的断言
        self.find_element('com.excelliance.dualaid:id/rl_share_prize').click()
        self.wait_for(2)
        try:
            self.assertIn('请先登录/注册', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error018_7.png')
        finally:
            self.assertIn('请先登录/注册', self.get_xml(), '点击邀请与兑奖跳转失败')

        # 点击返回按钮的断言
        self.find_element('com.excelliance.dualaid:id/share_nav_back').click()
        self.wait_for(2)
        try:
            self.assertIn('com.excelliance.dualaid:id/iv_icon', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error018_8.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/iv_icon', self.get_xml(), '点击back跳转失败')

        # 点击应用加锁的断言
        self.find_element('com.excelliance.dualaid:id/rl_lock_manager').click()
        self.wait_for(2)
        try:
            self.assertIn('com.excelliance.dualaid:id/tv_free_trial', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error018_9.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/tv_free_trial', self.get_xml(), '点击应用加锁跳转失败')

        # 点击返回按钮的断言
        self.find_element('com.excelliance.dualaid:id/pay_nav_back').click()
        self.wait_for(2)
        try:
            self.assertIn('com.excelliance.dualaid:id/iv_icon', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error018_10.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/iv_icon', self.get_xml(), '点击返回按钮跳转失败')

        # 点击内存管理的断言
        self.find_element('com.excelliance.dualaid:id/rl_task_manager').click()
        self.wait_for(2)
        try:
            self.assertIn('com.excelliance.dualaid:id/task_whiteList', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error018_11.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/task_whiteList', self.get_xml(), '点击内存管理跳转失败')

        # 点击返回按钮的断言
        self.find_element('com.excelliance.dualaid:id/ib_back').click()
        self.wait_for(2)
        try:
            self.assertIn('com.excelliance.dualaid:id/iv_icon', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error018_12.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/iv_icon', self.get_xml(), '点击返回按钮跳转失败')

        # 点击一键全部修复的断言
        self.find_element('com.excelliance.dualaid:id/rl_one_key_repair').click()
        self.wait_for(2)
        try:
            self.assertIn('com.excelliance.dualaid:id/tv_right', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error018_13.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/tv_right', self.get_xml(), '点击一键全部修复操作失败')

        # 点击暂不按钮的断言
        self.find_element('com.excelliance.dualaid:id/tv_right').click()
        self.wait_for(2)
        try:
            self.assertIn('com.excelliance.dualaid:id/iv_icon', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error018_14.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/iv_icon', self.get_xml(), '点击暂不按钮操作失败')

        # 点击更多高级设置的断言
        self.find_element('com.excelliance.dualaid:id/rl_more_settings').click()
        self.wait_for(2)
        try:
            self.assertIn('com.excelliance.dualaid:id/set_private', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error018_15[%s].png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/set_private', self.get_xml(), '点击更多高级设置跳转失败')

        # 点击返回按钮的断言
        self.find_element('com.excelliance.dualaid:id/more_setting_iv_back').click()
        self.wait_for(2)
        try:
            self.assertIn('com.excelliance.dualaid:id/iv_icon', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error018_16.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/iv_icon', self.get_xml(), '点击暂不按钮操作失败')

        # 点击主题换肤的断言
        self.find_element('com.excelliance.dualaid:id/rl_switch_style').click()
        self.wait_for(2)
        try:
            self.assertIn('com.excelliance.dualaid:id/iv_selected', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error018_17.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/iv_selected', self.get_xml(), '点击主题换肤跳转失败')

        # 换肤+返回操作的断言
        self.find_elements('com.excelliance.dualaid:id/textName')[1].click()
        self.wait_for(1)
        self.find_element('com.excelliance.dualaid:id/more_setting_iv_back').click()
        self.wait_for(2)
        try:
            self.assertIn('灵霄紫', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error018_18.png')
        finally:
            self.assertIn('灵霄紫', self.get_xml(), '主题换肤失败')

        # 点击版本更新的断言
        self.find_element('com.excelliance.dualaid:id/rl_update').click()
        self.wait_for(10)
        try:
            self.assertIn('版本号', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error018_19.png')
        finally:
            self.assertIn('版本号', self.get_xml(), '点击版本更新跳转失败')

        # 点击返回按钮的断言
        self.find_element('com.excelliance.dualaid:id/web_back').click()
        self.wait_for(2)
        try:
            self.assertIn('com.excelliance.dualaid:id/iv_icon', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error018_20.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/iv_icon', self.get_xml(), '点击返回按钮跳转失败')

        # 点击帮助与反馈的断言
        self.swipe_find_element('com.excelliance.dualaid:id/rl_help_feedback', 800, 'U')
        self.wait_for(2)
        self.swipe_up()
        self.wait_for(2)
        try:
            self.assertIn('com.excelliance.dualaid:id/tv_feedback', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error018_21.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/tv_feedback', self.get_xml(), '点击帮助与反馈跳转失败')

        # 点击返回按钮的断言
        self.find_element('com.excelliance.dualaid:id/ib_back').click()
        self.wait_for(2)
        try:
            self.assertIn('com.excelliance.dualaid:id/iv_icon', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error018_22.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/iv_icon', self.get_xml(), '点击返回按钮跳转失败')

        # 点击关于的断言
        self.swipe_find_element('com.excelliance.dualaid:id/rl_about_multi')
        self.wait_for(2)
        try:
            self.assertIn('com.excelliance.dualaid:id/tv_version', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error018_23.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/tv_version', self.get_xml(), '点击关于跳转失败')

        # 点击返回按钮的断言
        self.find_element('com.excelliance.dualaid:id/iv_back').click()
        self.wait_for(2)
        try:
            self.assertIn('com.excelliance.dualaid:id/iv_icon', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error018_24.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/iv_icon', self.get_xml(), '点击返回按钮跳转失败')

    def test019(self):
        """
        非VIP用户添加多开应用弹窗提示
        1.启动app至状态（三无主界面）
        2.点击推荐添加微信
        3.back退出引导
        4.点击添加按钮
        5.点击微信进行添加
        6.点击弹窗上的左按钮
        7.点击返回按钮
        8.点击微信进行添加
        9.点击弹窗上的右按钮
        """
        try:
            self.set_app_status2()
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'settingerror019.png')

        self.find_elements('com.excelliance.dualaid:id/root')[0].click()
        self.wait_for(5)
        self.back()
        self.wait_for(1)
        self.find_element('com.excelliance.dualaid:id/add_but').click()
        self.wait_for(5)

        # 非VIP用户添加多开应用弹窗提示断言
        self.find_elements('com.excelliance.dualaid:id/add_game_btn')[0].click()
        self.wait_for()
        try:
            self.assertIn('com.excelliance.dualaid:id/ll_dialog', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error019_1.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/ll_dialog', self.get_xml(), '非VIP用户添加多开应用未弹窗')

        # 点击弹窗左按钮断言
        self.find_element('com.excelliance.dualaid:id/tv_left').click()
        self.wait_for()
        try:
            self.assertIn('免注册登录', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error019_2.png')
        finally:
            self.assertIn('免注册登录', self.get_xml(), '点击弹窗的左按钮跳转失败')

        # 点击返回按钮断言
        self.find_element('com.excelliance.dualaid:id/iv_back').click()
        self.wait_for()
        try:
            self.assertIn('添加双开应用', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error019_3.png')
        finally:
            self.assertIn('添加双开应用', self.get_xml(), '点击输入账号页的返回按钮跳转失败')

        # 点击弹窗右按钮断言
        self.find_elements('com.excelliance.dualaid:id/add_game_btn')[0].click()
        self.wait_for()
        self.find_element('com.excelliance.dualaid:id/tv_right').click()
        self.wait_for(3)
        try:
            self.assertIn('支付开通', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error019_4.png')
        finally:
            self.assertIn('支付开通', self.get_xml(), '点击弹窗的右按钮跳转失败')

    def test020(self):
        """
        登录非VIP账户情况下的个人中心按钮遍历
        1.
        2.
        """
        try:
            self.set_app_status5()
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'settingerror020.png')

        # 点击头像按钮
        self.find_element('com.excelliance.dualaid:id/iv_icon_edit_bg').click()
        self.wait_for()
        try:
            self.assertIn('编辑个人信息', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error020_1.png')
        finally:
            self.assertIn('编辑个人信息', self.get_xml(), '点击头像按钮跳转失败')

        # 点击返回
        self.back()
        self.wait_for()

        # 点击我的优惠券断言
        self.find_element('com.excelliance.dualaid:id/rl_my_ticket').click()
        self.wait_for(2)
        try:
            self.assertIn('我的优惠券', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error020_2.png')
        finally:
            self.assertIn('我的优惠券', self.get_xml(), '点击我的优惠券跳转失败')

        # 点击返回
        self.back()
        self.wait_for()

        # 点击邀请与兑奖
        self.find_element('com.excelliance.dualaid:id/rl_share_prize').click()
        self.wait_for(2)
        try:
            self.assertIn('com.excelliance.dualaid:id/invitation_code_tv', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error020_3.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/invitation_code_tv', self.get_xml(), '点击邀请与兑奖跳转失败')

        # 点击返回
        self.back()
        self.wait_for()

    def test021(self):
        """
        登录VIP账户情况下的个人中心按钮遍历
        1.
        2.
        """
        try:
            self.set_app_status7()
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'settingerror021.png')

        # 点击个人中心按钮
        self.find_element('com.excelliance.dualaid:id/iv_icon').click()
        self.wait_for()

        # 点击我的VIP
        self.find_element('com.excelliance.dualaid:id/rl_my_vip').click()
        self.wait_for()
        try:
            self.assertIn('我的VIP' and '会员有效期至', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error021_1.png')
        finally:
            self.assertIn('我的VIP' and '会员有效期至', self.get_xml(), '点击我的VIP跳转失败')

        # 点击返回
        self.back()
        self.wait_for()

        # 点击应用加锁
        self.find_element('com.excelliance.dualaid:id/rl_lock_manager').click()
        self.wait_for()
        try:
            self.assertIn('com.excelliance.dualaid:id/iv_lock_app_img', self.get_xml())
        except Exception as e:
            print(e)
            self.screenshot(img_path + 'error021_2.png')
        finally:
            self.assertIn('com.excelliance.dualaid:id/iv_lock_app_img', self.get_xml(), '点击应用加锁跳转失败')

