import re
import time
from termcolor import *

# import xlwt

# workbook = xlwt.Workbook()
pkgName = "com.excelliance.dualaid"
pkgActName = "com.excelliance.kxqp.ui.HelloActivity"
while 1:
    while 1:
        try:
            ver1, ti = map(str, input('请输入版本号和执行次数，空格隔开：').split())
            break
        except ValueError:
            print(colored('请检查输入内容是否完整或版本号与执行次数间是否加了空格！', 'red'))
    if int(ti) >= 3:
        break
    else:
        print(colored('执行次数不能小于3！', 'red'))
times = int(ti)
path = time.strftime('%Y%m%d%H%M%S-', time.localtime(time.time()))

try:
    os.makedirs(r'd:/testTime/back/')
    os.makedirs(r'd:/testTime/home/')
    os.makedirs(r'd:/testTime/force/')
    print('测试文件夹已创建')
except FileExistsError:
    pass


class StartTest(object):
    def test_device(self):
        t = os.popen('adb devices').read()
        try:
            t_device = re.search(r'^([a-zA-Z0-9]+)\s+device', t, re.M).group(1)
        except AttributeError:
            t_device = None
            print(colored("设备未连接，请检查……", "red"))
            time.sleep(3)
            self.test_device()
        return t_device

    def testback(self):
        bpath = 'd:/testTime/back/'
        sum = 0
        i = 1
        list1 = []
        self.test_device()
        os.popen('adb shell am start -W ' + pkgName + '/' + pkgActName)
        time.sleep(2)
        self.test_device()
        os.popen('adb shell input keyevent 4')

        while i <= times:
            time.sleep(2)
            j = "第" + str(i) + "次："
            print(j)
            self.test_device()
            p = os.popen('adb shell am start -W ' + pkgName + '/' + pkgActName)
            s = p.read()
            time.sleep(3)
            self.test_device()
            os.popen('adb shell input keyevent 4')
            b = re.search(r'(TotalTime:)\s(\d+)', s)
            try:
                resu = b.group(2)
                if int(resu) > 1000:
                    print(colored('此次数据异常', "red"))
                else:
                    i = i + 1
            except AttributeError:
                print('此次未获取到启动数据！')
                continue
            print("启动时间为：", colored(resu, "red"))
            with open(bpath + path + ver1 + '.txt', 'a') as f:
                f.write(j + resu + '\n')
            result = int(resu)
            if result < 1000:
                list1.append(result)
                sum = sum + result
            print("总计：" + str(sum))
        else:
            print("最大值为：", colored(max(list1), "green"), "最小值为：", colored(min(list1), "magenta"))
            avg = round((sum - max(list1) - min(list1)) / (i - 3), 3)
            print("平均值为：", colored(avg, "cyan"))
            with open(bpath + path + ver1 + '.txt', 'a') as y:
                y.write("最大值为：" + str(max(list1)) + " 最小值为：" + str(min(list1)) + "\n")
                y.write("平均值：" + str(avg) + '\n')

    def testhome(self):
        hpath = 'D:/testTime/home/'
        i = 1
        sum = 0
        list1 = []
        time.sleep(2)
        self.test_device()
        os.popen('adb shell am start -W ' + pkgName + '/' + pkgActName)
        time.sleep(2)
        self.test_device()
        os.popen('adb shell input keyevent 3')
        time.sleep(1)
        self.test_device()
        os.popen('adb shell am start -W ' + pkgName + '/' + pkgActName)
        time.sleep(2)
        self.test_device()
        os.popen('adb shell input keyevent 3')

        while i <= times:
            time.sleep(2)
            j = "第" + str(i) + "次："
            print(j)
            self.test_device()
            p = os.popen('adb shell am start -W ' + pkgName + '/' + pkgActName)
            s = p.read()
            time.sleep(3)
            self.test_device()
            os.popen('adb shell input keyevent 3')
            b = re.search(r'(TotalTime:)\s(\d+)', s)
            try:
                resu = b.group(2)
                if int(resu) > 800:
                    print(colored('此次数据异常', "red"))
                else:
                    i = i + 1
            except AttributeError:
                print('此次未获取到启动数据！')
                continue
            print("启动时间为：", colored(resu, "red"))
            with open(hpath + path + ver1 + '.txt', 'a') as f:
                f.write(j + '\t' + resu + '\t\n')
            result = int(resu)
            # worksheet.write(i, 0, i, )
            # worksheet.write(i, 1, result)
            if result < 800:
                list1.append(result)
                sum = sum + result
            print("总计：" + str(sum))
            # i = i + 1
        else:
            print("最大值为：", colored(max(list1), "green"), "最小值为：", colored(min(list1), "magenta"))
            avg = round((sum - max(list1) - min(list1)) / (i - 3), 3)
            print("平均值为：", colored(avg, "cyan"))
            with open(hpath + path + ver1 + '.txt', 'a') as y:
                y.write("最大值为：" + str(max(list1)) + " 最小值为：" + str(min(list1)) + "\n")
                y.write("平均值：" + str(avg) + '\n')
        # workbook.save('d:/testTime/' + path + ver1 + '.xlsx')

    def testforce(self):
        fpath = 'd:/testTime/force/'
        i = 1
        sum = 0
        list1 = []
        time.sleep(2)
        self.test_device()
        os.popen('adb shell am start -W ' + pkgName + '/' + pkgActName)
        time.sleep(2)
        self.test_device()
        os.popen('adb shell am force-stop ' + pkgName)

        while i <= times:
            time.sleep(2)
            j = "第" + str(i) + "次："
            print(j)
            self.test_device()
            time.sleep(1)
            p = os.popen('adb shell am start -W ' + pkgName + '/' + pkgActName)
            s = p.read()
            # print(s)
            time.sleep(2)
            b = re.search(r'(TotalTime:)\s(\d+)', s)
            self.test_device()
            os.popen('adb shell am force-stop ' + pkgName)
            try:
                resu = b.group(2)
                if int(resu) > 1800:
                    print(colored('此次数据异常', "red"))
                else:
                    i = i + 1
            except AttributeError:
                print('此次未获取到启动数据！')
                continue
            print("启动时间为：", colored(resu, "red"))
            with open(fpath + path + ver1 + '.txt', 'a') as f:
                f.write(j + resu + '\n')
            result = int(resu)
            # worksheet.write(i, 0, i, )
            # worksheet.write(i, 1, result)
            if result < 1800:
                list1.append(result)
                sum = sum + result
            print("总计：" + str(sum))
            # i = i + 1
        else:
            print("最大值为：", colored(max(list1), "green"), "最小值为：", colored(min(list1), "magenta"))
            avg = round((sum - max(list1) - min(list1)) / (i - 3), 3)
            print("平均值为：", colored(avg, "cyan"))
            with open(fpath + path + ver1 + '.txt', 'a') as y:
                y.write("最大值为：" + str(max(list1)) + " 最小值为：" + str(min(list1)) + "\n")
                y.write("平均值：" + str(avg) + '\n')
        # workbook.save('d:/testTime/' + path + ver1 + '.xlsx')


if __name__ == '__main__':
    s = StartTest()
    s.test_device()
    choose = int(input("输入要测项前面数字：1.back 2.home 3.冷启动"))
    print("——测试开始——")
    if choose == 1:
        s.testback()
    elif choose == 2:
        s.testhome()
    elif choose == 3:
        s.testforce()
    elif choose == 12 or choose == 21:
        s.testback()
        s.testhome()
    elif choose == 13 or choose == 31:
        s.testback()
        s.testforce()
    elif choose == 23 or choose == 32:
        s.testhome()
        s.testforce()
    else:
        s.testback()
        s.testhome()
        s.testforce()
