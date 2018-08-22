# coding=utf-8


# 计算列表的中位数
def list_middle(lists):
    lists.sort()
    half = len(lists) // 2
    return (lists[half] + lists[~half]) / 2


# 计算列表的差值
def diff_value(list1, list2):
    import numpy as np
    return list(np.array(list1) - np.array(list2))
