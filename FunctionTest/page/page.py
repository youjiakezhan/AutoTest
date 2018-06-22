# -*- coding: utf-8 -*-

from FunctionTest.page.page_create import PageCreate

pc = PageCreate()
pages = pc.traverse_yaml()


def get_locater(class_name, method_name):
    locators = pages[class_name]['locators']
    for locator in locators:
        if locator['name'] == method_name:
            return locator


class AddGuidePage:
    登录注册 = get_locater('AddGuidePage', '登录注册')
    开启 = get_locater('AddGuidePage', '开启')
    复选框 = get_locater('AddGuidePage', '复选框')

    
class AppListPage:
    添加双开应用 = get_locater('AppListPage', '添加双开应用')
    添加 = get_locater('AppListPage', '添加')

    
class EditInfoPage:
    退出登录 = get_locater('EditInfoPage', '退出登录')
    确认退出 = get_locater('EditInfoPage', '确认退出')

    
class HomePage:
    个人中心 = get_locater('HomePage', '个人中心')
    空间切换 = get_locater('HomePage', '空间切换')
    一键清理 = get_locater('HomePage', '一键清理')
    添加按钮 = get_locater('HomePage', '添加按钮')
    多开引导 = get_locater('HomePage', '多开引导')
    icon位 = get_locater('HomePage', 'icon位')
    activity = get_locater('HomePage', 'activity')
    添加引导 = get_locater('HomePage', '添加引导')
    应用菜单窗口 = get_locater('HomePage', '应用菜单窗口')
    桌面图标 = get_locater('HomePage', '桌面图标')
    移动位置 = get_locater('HomePage', '移动位置')
    图标伪装 = get_locater('HomePage', '图标伪装')
    删除应用 = get_locater('HomePage', '删除应用')
    一键修复 = get_locater('HomePage', '一键修复')
    二级菜单窗口X = get_locater('HomePage', '二级菜单窗口X')
    删除 = get_locater('HomePage', '删除')
    完成 = get_locater('HomePage', '完成')
    二级菜单窗口 = get_locater('HomePage', '二级菜单窗口')

    
class LoginPage:
    下一步 = get_locater('LoginPage', '下一步')
    登录 = get_locater('LoginPage', '登录')
    免注册登录 = get_locater('LoginPage', '免注册登录')

    
class MyPage:
    返回 = get_locater('MyPage', '返回')
    头像 = get_locater('MyPage', '头像')
    版本更新 = get_locater('MyPage', '版本更新')
    开通VIP会员 = get_locater('MyPage', '开通VIP会员')

    
class NavigationPage:
    立即体验 = get_locater('NavigationPage', '立即体验')

    
class ShrinkPage:
    个人中心 = get_locater('ShrinkPage', '个人中心')
    空间切换 = get_locater('ShrinkPage', '空间切换')
    一键清理 = get_locater('ShrinkPage', '一键清理')
    添加 = get_locater('ShrinkPage', '添加')

    
if __name__ == '__main__':
    pass
