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
    换机数据迁移 = get_locater('HomePage', '换机数据迁移')
    弹出窗 = get_locater('HomePage', '弹出窗')
    弹出窗左按钮 = get_locater('HomePage', '弹出窗左按钮')
    弹出窗右按钮 = get_locater('HomePage', '弹出窗右按钮')
    防封号不再提醒 = get_locater('HomePage', '防封号不再提醒')
    防封号暂不 = get_locater('HomePage', '防封号暂不')

    
class LoginPage:
    下一步 = get_locater('LoginPage', '下一步')
    登录 = get_locater('LoginPage', '登录')
    免注册登录 = get_locater('LoginPage', '免注册登录')
    免注册获取验证码 = get_locater('LoginPage', '免注册获取验证码')

    
class MoreSettingPage:
    返回 = get_locater('MoreSettingPage', '返回')
    私密空间开关 = get_locater('MoreSettingPage', '私密空间开关')

    
class MyPage:
    返回 = get_locater('MyPage', '返回')
    头像 = get_locater('MyPage', '头像')
    消息中心 = get_locater('MyPage', '消息中心')
    消息中心编辑 = get_locater('MyPage', '消息中心编辑')
    开通VIP会员 = get_locater('MyPage', '开通VIP会员')
    我的优惠券 = get_locater('MyPage', '我的优惠券')
    邀请与兑奖 = get_locater('MyPage', '邀请与兑奖')
    应用加锁 = get_locater('MyPage', '应用加锁')
    内存管理 = get_locater('MyPage', '内存管理')
    一键全部修复 = get_locater('MyPage', '一键全部修复')
    更多高级设置 = get_locater('MyPage', '更多高级设置')
    主题换肤 = get_locater('MyPage', '主题换肤')
    当前选中的主题 = get_locater('MyPage', '当前选中的主题')
    主题名称 = get_locater('MyPage', '主题名称')
    版本更新 = get_locater('MyPage', '版本更新')
    版本更新返回按钮 = get_locater('MyPage', '版本更新返回按钮')
    帮助与反馈 = get_locater('MyPage', '帮助与反馈')
    意见反馈按钮 = get_locater('MyPage', '意见反馈按钮')
    关于 = get_locater('MyPage', '关于')
    关于页版本号 = get_locater('MyPage', '关于页版本号')
    我的VIP = get_locater('MyPage', '我的VIP')
    安全锁页锁图标 = get_locater('MyPage', '安全锁页锁图标')

    
class NavigationPage:
    立即体验 = get_locater('NavigationPage', '立即体验')

    
class PaymentPage:
    返回 = get_locater('PaymentPage', '返回')
    支付开通标题 = get_locater('PaymentPage', '支付开通标题')
    确认支付 = get_locater('PaymentPage', '确认支付')
    支付方式选择 = get_locater('PaymentPage', '支付方式选择')
    免费试用 = get_locater('PaymentPage', '免费试用')

    
class SharePage:
    返回 = get_locater('SharePage', '返回')
    请先登录注册 = get_locater('SharePage', '请先登录注册')
    邀请码 = get_locater('SharePage', '邀请码')

    
class ShrinkPage:
    个人中心 = get_locater('ShrinkPage', '个人中心')
    空间切换 = get_locater('ShrinkPage', '空间切换')
    一键清理 = get_locater('ShrinkPage', '一键清理')
    添加 = get_locater('ShrinkPage', '添加')

    
class TaskManagePage:
    返回 = get_locater('TaskManagePage', '返回')
    白名单 = get_locater('TaskManagePage', '白名单')
    一键清理 = get_locater('TaskManagePage', '一键清理')

    
if __name__ == '__main__':
    pass
