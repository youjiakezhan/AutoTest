# coding=utf-8
from matplotlib import pyplot as plt
import numpy as np
from AutoTest.myfunction.matplotlib_setting import __init__


def max_minus_min(lists):
    print(max(lists)-min(lists))


def create_image():
    # 初始化数据可视化类
    __init__()
    plt.figure(1, dpi=120)
    plt.title('honor9测试数据')
    my_y_ticks = np.arange(0, 1200, 50)
    plt.yticks(my_y_ticks)
    plt.xlabel('样本数(200组)')
    plt.ylabel('启动时间(ms)')
    plt.plot(list1, 'r', label='back_306')
    plt.plot(list2, 'g', label='home_306')
    plt.plot(list3, 'b', label='force_306')
    plt.legend()
    plt.grid(color='skyblue')
    plt.show()


# honor9的600组启动时间数据（3.0.6版本）
# 差值 [52 52 82] 在90ms之内
list1 = [166, 169, 168, 181, 185, 181, 152, 185, 157, 160, 170, 194, 158, 155, 153, 165, 161, 180, 163, 160, 179, 161,
         176, 162, 147, 142, 155, 152, 152, 171, 167, 154, 166, 159, 154, 160, 174, 183, 159, 184, 181, 149, 149, 153,
         188, 162, 144, 152, 168, 150, 167, 142, 161, 174, 189, 174, 180, 158, 156, 187, 154, 159, 159, 153, 163, 178,
         186, 185, 179, 153, 164, 187, 157, 163, 178, 177, 168, 157, 171, 188, 153, 169, 187, 156, 147, 168, 152, 187,
         164, 153, 166, 163, 157, 158, 176, 150, 147, 152, 157, 174, 175, 162, 154, 179, 162, 151, 180, 143, 149, 158,
         182, 150, 172, 155, 161, 154, 152, 183, 158, 163, 158, 162, 172, 159, 179, 156, 146, 169, 175, 150, 148, 152,
         172, 166, 161, 145, 146, 172, 147, 153, 151, 148, 151, 158, 153, 159, 157, 148, 146, 155, 172, 153, 179, 182,
         173, 166, 171, 166, 184, 168, 153, 166, 150, 183, 150, 163, 161, 176, 185, 152, 172, 156, 161, 153, 155, 155,
         172, 173, 159, 161, 155, 168, 186, 179, 151, 158, 151, 157, 152, 158, 161, 190, 157, 158, 182, 144, 154, 156,
         157, 172]
list2 = [101, 105, 98, 101, 108, 95, 99, 102, 102, 92, 101, 101, 89, 101, 100, 97, 103, 95, 100, 98, 105, 107, 95, 99,
         88, 99, 92, 133, 94, 104, 96, 91, 97, 102, 104, 108, 107, 113, 97, 93, 111, 90, 99, 96, 91, 93, 98, 90, 108,
         97, 115, 110, 97, 107, 102, 95, 102, 102, 106, 96, 108, 99, 99, 104, 99, 103, 104, 97, 100, 96, 101, 98, 97,
         98, 100, 97, 93, 92, 100, 91, 94, 93, 101, 127, 95, 93, 106, 92, 108, 92, 95, 140, 91, 96, 100, 109, 107, 104,
         104, 99, 99, 100, 99, 102, 97, 102, 99, 99, 109, 99, 99, 99, 90, 103, 96, 92, 97, 101, 100, 104, 113, 114, 105,
         95, 98, 93, 93, 98, 96, 101, 96, 109, 100, 103, 103, 108, 102, 102, 106, 102, 94, 106, 92, 96, 97, 91, 96, 100,
         101, 109, 102, 101, 99, 105, 98, 98, 102, 111, 138, 97, 102, 97, 92, 94, 104, 104, 95, 100, 90, 100, 105, 109,
         105, 102, 102, 108, 102, 99, 106, 102, 100, 105, 102, 99, 99, 103, 101, 109, 110, 109, 99, 140, 113, 105, 109,
         107, 100, 107, 103, 108]
list3 = [561, 564, 566, 559, 549, 554, 551, 579, 605, 600, 554, 593, 562, 566, 553, 553, 548, 553, 580, 587, 556, 544,
         547, 558, 546, 559, 559, 559, 570, 568, 593, 558, 553, 563, 583, 564, 564, 554, 555, 552, 553, 546, 528, 561,
         542, 542, 574, 539, 553, 537, 557, 535, 579, 554, 541, 535, 564, 558, 548, 555, 558, 599, 539, 580, 551, 568,
         523, 543, 547, 567, 549, 553, 560, 558, 554, 545, 557, 544, 542, 555, 554, 531, 551, 580, 581, 551, 561, 539,
         558, 562, 552, 560, 567, 555, 596, 555, 540, 555, 547, 563, 542, 553, 542, 555, 560, 549, 549, 563, 556, 546,
         545, 601, 555, 553, 555, 585, 553, 564, 562, 552, 555, 539, 564, 563, 536, 552, 561, 577, 551, 568, 563, 548,
         548, 604, 535, 553, 555, 549, 557, 552, 553, 549, 581, 579, 552, 567, 547, 598, 542, 552, 532, 551, 537, 541,
         578, 553, 536, 542, 563, 559, 573, 532, 546, 568, 564, 589, 556, 589, 544, 543, 536, 552, 554, 571, 552, 579,
         593, 543, 570, 574, 546, 566, 555, 541, 552, 548, 539, 595, 551, 531, 554, 557, 542, 555, 556, 559, 557, 586,
         601]

# 每组数据的最大值和最小值做差（反应测试时手机的稳定程度）
# max_minus_min(list1)
# max_minus_min(list2)
# max_minus_min(list3)

# 306版本数据（数据整理自honor9的600组启动时间测试数据）
# back  home  force      场景
# 163   101   558        均值
# avg_back = sum(list1)/len(list1)
# avg_home = sum(list2)/len(list2)
# avg_force = sum(list3)/len(list3)
# print(round(avg_back), round(avg_home), round(avg_force))

if __name__ == '__main__':
    create_image()