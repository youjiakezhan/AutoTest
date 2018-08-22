# coding=utf-8
import os


def get_latest_file(file_path, postfix=''):
    """获取指定目录下(不含子目录)按改动时间排序最新文件"""
    # 列出目标目录下所有文件和文件夹并将其保存到列表
    lists = os.listdir(file_path)
    # 将所有文件按其最后修改时间排序
    lists.sort(key=lambda x: os.path.getmtime(file_path + "\\" + x))
    # 获取最新的文件保存到latest
    latest = os.path.join(file_path, lists[-1])
    if os.path.isdir(latest):
        print('目录中不能包含子目录')
    else:
        if latest.endswith(postfix):
            print(latest)
            return latest
        else:
            print('没有后缀名为%s的最新文件' % postfix)


if __name__ == '__main__':
    get_latest_file(r'C:\Users\BAIWAN\PycharmProjects\AutoTest\myfunction')