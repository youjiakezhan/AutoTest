# -*- coding: utf-8 -*-

from FunctionTest.page.page_create import PageCreate

pc = PageCreate()
pages = pc.traverse_yaml()


def get_locater(class_name, method_name):
    locators = pages[class_name]['locators']
    for locator in locators:
        if locator['name'] == method_name:
            return locator


class HomePage:
    个人中心 = get_locater('HomePage', '个人中心')
    空间切换 = get_locater('HomePage', '空间切换')
    一键清理 = get_locater('HomePage', '一键清理')
    添加 = get_locater('HomePage', '添加')

    
class MyPage:
    我的 = get_locater('MyPage', '我的')
    请点击登录 = get_locater('MyPage', '请点击登录')

    
class ShrinkPage:
    个人中心 = get_locater('ShrinkPage', '个人中心')
    空间切换 = get_locater('ShrinkPage', '空间切换')
    一键清理 = get_locater('ShrinkPage', '一键清理')
    添加 = get_locater('ShrinkPage', '添加')

    
if __name__ == '__main__':
    pass
