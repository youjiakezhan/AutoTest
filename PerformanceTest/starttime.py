import re
import time
from termcolor import *
import xlwt

workbook = xlwt.Workbook()
pkgName = "com.excelliance.dualaid"
pkgActName = "com.excelliance.kxqp.ui.HelloActivity"
while 1:
    ver1, ti = map(str, input('请输入版本号和执行次数，空格隔开：').split())
    if int(ti) >= 3:
        break
    else:
        print('执行次数不能小于3！')
times = int(ti)
path = time.strftime('%Y%m%d%H%M%S-', time.localtime(time.time()))

class Starttest():
    def testtack(self):
        bpath = 'd:/testTime/back/'
        worksheet = workbook.add_sheet('back启动时间')
        worksheet.write(0, 0, '次数')
        worksheet.write(0, 1, '启动时间（ms）')
        sum = 0
        i = 1
        list1 = []
        os.popen('adb shell am start -W ' + pkgName + '/' + pkgActName)
        time.sleep(2)
        os.popen('adb shell input keyevent 4')

        while i <= times:
            time.sleep(2)
            j = "第" + str(i) + "次："
            print(j)
            p = os.popen('adb shell am start -W ' + pkgName + '/' + pkgActName)
            s = p.read()
            time.sleep(3)
            os.popen('adb shell input keyevent 4')
            b = re.search(r'(TotalTime:)\s(\d+)', s)
            resu = b.group(2)
            print("启动时间为：", colored(resu, "red"))
            with open(bpath + path + ver1 + '.txt', 'a') as f:
                f.write(j + resu + '\n')
            result = int(resu)
            worksheet.write(i, 0, i, )
            worksheet.write(i, 1, result)
            list1.append(result)
            sum = sum + result
            print("总计：" + str(sum))
            i = i + 1
        else:
            print("最大值为：", colored(max(list1), "green"), "最小值为：", colored(min(list1), "magenta"))
            avg = round((sum - max(list1) - min(list1)) / (i - 3), 3)
            print("平均值为：", colored(avg, "cyan"))
            with open(bpath + path + ver1 + '.txt', 'a') as y:
                y.write("最大值为：" + str(max(list1)) + " 最小值为：" + str(min(list1)) + "\n")
                y.write("平均值：" + str(avg) + '\n')
        workbook.save('d:/testTime/' + path + ver1 + '.xlsx')

    def testhome(self):
        hpath = 'D:/testTime/home/'
        worksheet = workbook.add_sheet('home启动时间')
        worksheet.write(0, 0, '次数')
        worksheet.write(0, 1, '启动时间（ms）')
        i = 1
        sum = 0
        list1 = []
        time.sleep(2)
        os.popen('adb shell am start -W ' + pkgName + '/' + pkgActName)
        time.sleep(2)
        os.popen('adb shell input keyevent 3')
        time.sleep(1)
        os.popen('adb shell am start -W ' + pkgName + '/' + pkgActName)
        time.sleep(2)
        os.popen('adb shell input keyevent 3')

        while i <= times:
            time.sleep(2)
            j = "第" + str(i) + "次："
            print(j)
            p = os.popen('adb shell am start -W ' + pkgName + '/' + pkgActName)
            s = p.read()
            time.sleep(3)
            os.popen('adb shell input keyevent 3')
            b = re.search(r'(TotalTime:)\s(\d+)', s)
            resu = b.group(2)
            print("启动时间为：", colored(resu, "red"))
            with open(hpath + path + ver1 + '.txt', 'a') as f:
                f.write(j + resu + '\n')
            result = int(resu)
            worksheet.write(i, 0, i, )
            worksheet.write(i, 1, result)
            list1.append(result)
            sum = sum + result
            print("总计：" + str(sum))
            i = i + 1
        else:
            print("最大值为：", colored(max(list1), "green"), "最小值为：", colored(min(list1), "magenta"))
            avg = round((sum - max(list1) - min(list1)) / (i - 3), 3)
            print("平均值为：", colored(avg, "cyan"))
            with open(hpath + path + ver1 + '.txt', 'a') as y:
                y.write("最大值为：" + str(max(list1)) + " 最小值为：" + str(min(list1)) + "\n")
                y.write("平均值：" + str(avg) + '\n')
        workbook.save('d:/testTime/' + path + ver1 + '.xlsx')

    def testforce(self):
        fpath = 'd:/testTime/force/'
        worksheet = workbook.add_sheet('冷启动时间')
        worksheet.write(0, 0, '次数')
        worksheet.write(0, 1, '启动时间（ms）')
        i = 1
        sum = 0
        list1 = []
        time.sleep(2)
        os.popen('adb shell am start -W ' + pkgName + '/' + pkgActName)
        time.sleep(2)
        os.popen('adb shell am force-stop ' + pkgName)

        while i <= times:
            time.sleep(2)
            j = "第" + str(i) + "次："
            print(j)
            p = os.popen('adb shell am start -W ' + pkgName + '/' + pkgActName)
            s = p.read()
            time.sleep(3)
            os.popen('adb shell am force-stop ' + pkgName)
            b = re.search(r'(TotalTime:)\s(\d+)', s)
            resu = b.group(2)
            print("启动时间为：", colored(resu, "red"))
            with open(fpath + path + ver1 + '.txt', 'a') as f:
                f.write(j + resu + '\n')
            result = int(resu)
            worksheet.write(i, 0, i, )
            worksheet.write(i, 1, result)
            list1.append(result)
            sum = sum + result
            print("总计：" + str(sum))
            i = i + 1
        else:
            print("最大值为：", colored(max(list1), "green"), "最小值为：", colored(min(list1), "magenta"))
            avg = round((sum - max(list1) - min(list1)) / (i - 3), 3)
            print("平均值为：", colored(avg, "cyan"))
            with open(fpath + path + ver1 + '.txt', 'a') as y:
                y.write("最大值为：" + str(max(list1)) + " 最小值为：" + str(min(list1)) + "\n")
                y.write("平均值：" + str(avg) + '\n')
        workbook.save('d:/testTime/' + path + ver1 + '.xlsx')

if __name__ == '__main__':
    choose = int(input("输入要测项前面数字：1.back 2.home 3.冷启动"))
    print("——测试开始——")
    if choose == 1:
        Starttest().testtack()
    elif choose == 2:
        Starttest().testhome()
    elif choose == 3:
        Starttest().testforce()
    elif choose == 12 or choose == 21:
        Starttest().testtack()
        Starttest().testhome()
    elif choose == 13 or choose == 31:
        Starttest().testtack()
        Starttest().testforce()
    elif choose == 23 or choose == 32:
        Starttest().testhome()
        Starttest().testforce()
    else:
        Starttest().testtack()
        Starttest().testhome()
        Starttest().testforce()

