# coding=utf-8
from matplotlib import pyplot as plt


def __init__():
    # 解决matplotlib显示中文问题
    plt.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
