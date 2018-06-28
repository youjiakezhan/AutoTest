# _*_ coding:utf-8 _*_
import _tkinter
import os
import threading
import time
import tkinter
import winreg  # windows API
from tkinter import *
from tkinter.messagebox import showinfo

from requests_html import HTMLSession


class APP(object):

    def quit(self):
        """退出应用"""
        root.destroy()

    def clear_one(self):
        """清空文本框"""
        text.delete(0.0, tkinter.END)

    def clear_two(self):
        """清空listbox"""
        listbox.delete(0, END)

    def clear(self):
        """清空所有"""
        text.delete(0.0, tkinter.END)
        listbox.delete(0, END)


class GetInfo(object):
    """信息获取"""

    def check_wechart_version(self):
        session = HTMLSession()
        r = session.get('https://weixin.qq.com/')
        news = r.html.find('div.update_diary ul li a')
        for new in news:
            if new.html.find('Android') != -1:
                text.insert(END, new.text + '\n')
                text.see(END)
                text.update()

    def get_device_info(self):
        """获取安卓设备信息"""
        list = []
        data = os.popen('adb devices').read()
        if 'device' in data.split():
            list.append('手机品牌：' + os.popen('adb shell getprop ro.product.brand').read().strip())
            list.append('手机型号：' + os.popen('adb shell getprop ro.product.model').read().strip())
            list.append('安卓版本：' + os.popen('adb shell getprop ro.build.version.release').read().strip())
            list.append('序列号：' + os.popen('adb get-serialno').read().strip())
            list.append('CPU位数：' + os.popen('adb shell getprop ro.zygote').read().strip())
            list.append('屏幕分辨率：' + os.popen('adb shell wm size').read().replace('Physical size:', '').strip())
            list.append('像素密度：' + os.popen('adb shell wm density').read().replace('Physical density:', '').strip())
        else:
            text.insert(END, '请检查USB是否已连接或是否已开启调试模式')
        for line in list:
            text.insert(END, line + '\n')
            text.see(END)
            text.update()
        b11.configure(text='获取设备信息', bg='green')

    def get_time(self):
        """获取当前时间"""
        now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        return now

    def get_desktop_path(self):
        """获取系统桌面路径"""
        global path
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        path = winreg.QueryValueEx(key, "Desktop")[0]
        return path


class MyThread(threading.Thread):
    """多线程处理"""

    def __init__(self, func=None):
        threading.Thread.__init__(self)
        self.func = func

    def run(self):
        self.func()


class Log(object):
    """日志处理"""

    def catch_log(self):
        """抓取日志到电脑上"""
        b32.configure(text='抓取中...', bg='grey')
        os.popen('adb logcat -v time > ' + get_info.get_desktop_path() + '/%s.txt' % get_info.get_time())

    def stop_log(self):
        """停止log"""
        b32.configure(text='抓取log', bg='blue')
        data = os.popen('adb shell ps | findstr "logcat"')
        for logcat_uid in data.readlines():
            if "shell" in logcat_uid:
                os.popen('adb shell kill ' + logcat_uid.split()[1])


class ScreenOperation(object):
    """屏幕操作"""

    def check_adb(self):
        list = []
        adb_pid = os.popen('tasklist | findstr "adb.exe"')
        for i in adb_pid:
            adb_pid_host = i.split()[1]
            list.append(adb_pid_host)
        return list

    def screen_shot(self):
        """截屏"""
        os.popen('adb shell screencap /sdcard/1.png')
        time.sleep(2)
        os.popen('adb pull /sdcard/1.png ' + desktop_path + '\%s.png' % get_info.get_time())
        time.sleep(2)
        os.popen('adb shell rm sdcard/1.png')
        b31.configure(text='手机截图')

    def record_command(self):
        os.popen('adb shell screenrecord /sdcard/1.mp4')

    def recording(self):
        global record_pid, record_thread
        """录制屏幕"""
        adb_pid_list1 = self.check_adb()
        print(adb_pid_list1)
        record_thread = MyThread(self.record_command)
        record_thread.start()
        time.sleep(1)
        adb_pid_list2 = self.check_adb()
        print(adb_pid_list2)
        for i in adb_pid_list2:
            if i not in adb_pid_list1:
                print(i)
                record_pid = i
                return record_pid
            else:
                continue

    def pull_record(self):
        time.sleep(5)
        os.popen('adb pull /sdcard/1.mp4 ' + desktop_path + '\%s.mp4' % get_info.get_time())
        # time.sleep(3)
        # os.popen('adb shell rm /sdcard/1.mp4')

    def stop_recording(self):
        """停止并导出录制的视频"""
        global record_pid
        b36.configure(text='停止录制并导出', bg='blue')
        os.popen('taskkill /f /pid ' + record_pid)
        self.pull_record()


class PackageManage(object):
    """安装包管理"""
    app = APP()

    def pull_app(self):
        """导出手机安装包"""
        try:
            app_path = os.popen('adb shell pm path ' + listbox.get(listbox.curselection())).readline()

            os.popen('adb pull ' + app_path.replace('package:', '').strip() + ' ' + desktop_path
                     + '\%s.apk' % get_info.get_time())
        except _tkinter.TclError:
            text.insert(END, '请先选择一个包名\n')
            text.see(END)
            text.update()

    def display_installed_app(self):
        """列出已安装的第三方app（按照：应用图标+应用名+包名 方式展示）"""
        data = os.popen('adb devices').read()
        if 'device' in data.split():
            pck_names = os.popen('adb shell pm list packages -3 | sort')
        else:
            text.insert(END, '请检查USB是否已连接或是否已开启调试模式')
        b14.configure(text='本机应用列表', bg='green')
        for pck_name in pck_names:
            listbox.insert(END, pck_name.replace('package:', ''))
            listbox.see(END)
            listbox.update()

    def uninstall_app(self):
        """卸载选中的app（按包名）"""
        try:
            os.popen('adb uninstall ' + listbox.get(listbox.curselection()))
            self.app.clear_two()
            self.display_installed_app()
        except Exception:
            text.insert(END, '请先选择一个包名\n')
            text.see(END)
            text.update()


class AppOperation(object):
    """app相关操作"""

    def force_stop_app(self):
        try:
            os.popen('adb shell am force-stop ' + listbox.get(listbox.curselection()))
        except Exception:
            text.insert(END, '请先选择一个包名\n')
            text.see(END)
            text.update()

    def clear_app_data(self):
        try:
            os.popen('adb shell pm clear ' + listbox.get(listbox.curselection()))
        except Exception:
            text.insert(END, '请先选择一个包名\n')
            text.see(END)
            text.update()


class BatteryTest(object):

    def start_app(self):
        os.popen('adb shell am start com.excelliance.dualaid/com.excelliance.kxqp.ui.HelloActivity')

    def get_uid(self):
        content = os.popen('adb shell ps | findstr ' + 'com.excelliance.dualaid').read()
        UID = content.split()[0].replace('_', '')
        return UID

    def reset_battery(self):
        os.popen('adb shell dumpsys batterystats --reset')

    def set_usb(self):
        showinfo(title='提示窗', message='点击OK开始电量测试')
        os.popen('adb shell dumpsys battery unplug')
        os.popen('adb shell dumpsys battery set status 1')

    def rec_usb(self):
        os.popen('adb shell dumpsys battery reset')

    def get_batteryinfo(self):
        content = os.popen('adb shell dumpsys batterystats|findstr ' + self.get_uid()).read()
        batteryinfo = (str(re.findall('(?<=[(])[^()]+\.[^()]+(?=[)])', content)).replace('[', '')).replace(']', '')
        return batteryinfo

    def stop_app(self):
        showinfo(title='提示窗', message='测试结束\n点击OK退出应用')
        os.popen('adb shell am force-stop ' + 'com.excelliance.dualaid')

    def run(self):
        # file = open(path + '\\耗电量测试数据.xlsx', 'a')
        # time.sleep(1)
        self.start_app()
        time.sleep(2)
        self.get_uid()
        time.sleep(1)
        self.reset_battery()
        time.sleep(1)
        self.set_usb()
        time.sleep(20)
        self.rec_usb()
        time.sleep(2)
        self.get_batteryinfo()
        time.sleep(1)
        # file.write(self.get_batteryinfo() + '\n')
        self.stop_app()
        text.insert(END, self.get_batteryinfo().replace("'", "") + '\n')
        text.see(END)
        text.update()
        # file.close()
        b22.configure(text='耗电量测试')


def catch_log_pck(event):
    b32.configure(text='过滤抓取中...', bg='grey')
    os.popen(
        'adb logcat -v time | find "com.excelliance.dualaid" > ' + get_info.get_desktop_path() +
        '/%s.txt' % get_info.get_time())


def b22_state(event):
    b22.configure(text='正在测试...')


def b11_state(event):
    b11.configure(text='获取中...')


def b14_state(event):
    b14.configure(text='正在拉取')


def b31_state(event):
    b31.configure(text='正在导出')


def b35_state(event):
    b35.configure(text='正在录制...', bg='grey')
    b35.flash()


def b36_state(event):
    b35.configure(text='录制视频', bg='blue')
    b36.configure(text='正在导出...')


def create_window():
    global root
    root = Tk()
    root.title('AndroidTestTool')
    root.geometry('800x600')
    root.resizable(width=False, height=False)


app = APP()
get_info = GetInfo()
log = Log()
screen_operate = ScreenOperation()
pck_manage = PackageManage()
app_operate = AppOperation()
battery = BatteryTest()
desktop_path = get_info.get_desktop_path()
BASE_PATH = os.path.abspath(os.path.dirname('__file__'))
record_pid = ''
stop_thread_flag = True

create_window()
# 左右显示屏
frm1 = Frame(root)
text = Text(frm1, width=39, height='22', bg='sky blue', fg='green', font=('宋体', 14))
text.pack(side=LEFT, fill=Y, padx=2)
listbox = Listbox(frm1, width=39, height='22', bg='sky blue', fg='green', font=('宋体', 14))
listbox.pack(side=RIGHT, fill=Y, padx=2)
frm1.pack(padx=3, pady=3)

frm2 = Frame(root)
b11 = Button(frm2, text='获取设备信息', activebackground='grey', width='15', height='1', bg='green', fg='gold',
             command=get_info.get_device_info)
b11.grid(row=0, column=0)
b11.bind('<ButtonPress-1>', b11_state)

b12 = Button(frm2, text='启动时间测试', width='15', height='1', bg='green', fg='gold').grid(row=0, column=1)
b13 = Button(frm2, text='内存/CPU查看', width='15', height='1', bg='green', fg='gold').grid(row=0, column=2)
# 图片
img0 = PhotoImage(file=os.path.abspath(os.path.join(BASE_PATH, '1.gif')))
label0 = Label(frm2, image=img0, width=97, height=50, bg='sky blue')
label0.grid(row=0, column=3, rowspan=2, sticky=N + S)

b14 = Button(frm2, text='本机应用列表', activebackground='grey', width='15', height='1', bg='green', fg='gold',
             command=pck_manage.display_installed_app)
b14.grid(row=0, column=4)
b14.bind('<ButtonPress-1>', b14_state)

b15 = Button(frm2, text='强行停止', width='15', height='1', bg='green', fg='gold', command=app_operate.force_stop_app) \
    .grid(row=0, column=5)
b16 = Button(frm2, text='清除数据', width='15', height='1', bg='green', fg='gold', command=app_operate.clear_app_data) \
    .grid(row=0, column=6)
b21 = Button(frm2, text='微信官网版本', activebackground='grey', width='15', height='1', bg='green', fg='gold',
             command=get_info.check_wechart_version).grid(row=1, column=0)

b22 = Button(frm2, text='耗电量测试', activebackground='grey', width='15', height='1', bg='green', fg='gold',
             command=battery.run)
b22.grid(row=1, column=1)
b22.bind('<ButtonPress-1>', b22_state)

b23 = Button(frm2, text='清理左屏', width='15', height='1', bg='sky blue', fg='red', command=app.clear_one).grid(row=1,
                                                                                                             column=2)
b24 = Button(frm2, text='清理右屏', width='15', height='1', bg='sky blue', fg='red', command=app.clear_two).grid(row=1,
                                                                                                             column=4)
b25 = Button(frm2, text='导出安装包', width='15', height='1', bg='green', fg='gold', command=pck_manage.pull_app) \
    .grid(row=1, column=6)
b26 = Button(frm2, text='卸载应用', width='15', height='1', bg='green', fg='gold', command=pck_manage.uninstall_app)
b26.grid(row=1, column=5)
frm2.pack(side=TOP, fill=BOTH, padx=3)

frm3 = Frame(root)
b31 = Button(frm3, text='手机截图', activebackground='grey', width='15', height='1', bg='blue', fg='white',
             command=screen_operate.screen_shot)
b31.grid(row=0, column=0)
b31.bind('<ButtonPress-1>', b31_state)

b32 = Button(frm3, text='抓取log', activebackground='grey', width='15', height='1', bg='blue', fg='white',
             command=log.catch_log)
b32.grid(row=0, column=1)
b32.bind('<ButtonPress-3>', catch_log_pck)

b33 = Button(frm3, text='停止log', activebackground='grey', width='15', height='1', bg='blue', fg='white',
             command=log.stop_log).grid(row=0, column=2)
b34 = Button(frm3, text='清屏', width='13', height='1', bg='sky blue', fg='red', command=app.clear) \
    .grid(row=0, column=3)
b35 = Button(frm3, text='录制屏幕', width='15', height='1', bg='blue', fg='white', command=screen_operate.recording)
b35.grid(row=0, column=4)
b35.bind('<ButtonPress-1>', b35_state)

b36 = Button(frm3, text='停止录制并导出', activebackground='grey', width='15', height='1', bg='blue', fg='white',
             command=screen_operate.stop_recording)
b36.grid(row=0, column=5)
b36.bind('<ButtonPress-1>', b36_state)

b37 = Button(frm3, text='退出', width='15', height='1', bg='red', fg='black', command=app.quit).grid(row=0, column=6)
frm3.pack(side=TOP, fill=BOTH, padx=3, pady=3)

frm = Frame(root)
label1 = Label(frm, text='Auth:EternalSunshine', height='2', font=('粗体', 18), bg='orchid', fg='gold')
label1.pack(fill=BOTH)
frm.pack(side=TOP, fill=BOTH, padx=3, pady=3)

root.mainloop()
