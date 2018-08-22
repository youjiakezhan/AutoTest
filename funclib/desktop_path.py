# coding=utf-8
import winreg


def get_desktop_path():
    """获取系统桌面路径"""
    global path
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    path = winreg.QueryValueEx(key, "Desktop")[0]
    print(path)
    return path


if __name__ == '__main__':
    get_desktop_path()