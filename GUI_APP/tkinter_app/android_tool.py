# _*_ coding:utf-8 _*_
import _tkinter
import os
import threading
import time
import tkinter
import winreg  # windows API
from tkinter import *
from tkinter.messagebox import askyesno, showinfo

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

        def device_info():
            list = []
            text.insert(END, '获取中请稍等...\n')
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

        get_device_info_thread = MyThread(device_info)
        get_device_info_thread.start()

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

    def get_latest_apk(self):
        """获取指定目录下按改动时间排序最新文件"""
        apk_path = self.get_desktop_path()
        # 列出目录下所有文件和文件夹保存到lists
        lists = os.listdir(apk_path)
        # 按时间排序
        lists.sort(key=lambda x: os.path.getmtime(apk_path + "\\" + x))
        # 获取最新的文件保存到latest
        latest = os.path.join(apk_path, lists[-1])
        if '.apk' in latest:
            return latest
        else:
            print('未选择包名或导出apk文件失败')

    def get_launchable_activity(self):
        """获取选中包名的启动入口"""
        package = PackageManage()
        try:
            package.pull_app()
            flag = 1
        except Exception:
            flag = 0
        if flag == 1:
            time.sleep(5)
            apk_path = self.get_latest_apk()
            activity = os.popen(
                'aapt dump badging %s | find "launchable-activity"' % apk_path).read().split()[
                1].replace('name=', '').replace("'", '')
            launchable_activity = listbox.get(listbox.curselection()).strip() + '/' + activity
            # print(launchable_activity)
            os.popen('erase ' + apk_path)
            # os.popen('adb shell am start ' + launchable_activity)
            return launchable_activity

    def get_apk_name(self):
        pass

    def memory_cpu_monitor(self):
        text.insert(END, '尚未开发，敬请期待...' + '\n')
        text.see(END)
        text.update()

    def get_start_time(self):
        text.insert(END, '尚未开发，敬请期待...' + '\n')
        text.see(END)
        text.update()


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
        b32.configure(text='log抓取中', state=DISABLED)
        os.popen('adb logcat -v time > ' + get_info.get_desktop_path() + '/%s.txt' % get_info.get_time())

    def stop_log(self):
        """停止log"""
        b32.configure(text='抓取log', state=NORMAL)
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

        def shot():
            time_now = time.strftime('%Y%m%d%H%M%S')
            text.insert(END, '正在截图请稍等...')
            os.popen('adb shell screencap /sdcard/%s.png' % time_now)
            time.sleep(1.5)
            text.insert(END, 'ok!\n')
            time.sleep(1.5)
            os.popen('adb pull /sdcard/%s.png ' % time_now + desktop_path + '\%s.png' % time_now)
            text.insert(END, '截图已保存至桌面\n')
            text.see(END)
            text.update()
        screen_shot_thread = MyThread(shot)
        screen_shot_thread.start()

    def recording(self):
        global record_pid
        """录制屏幕"""
        b35.configure(text='录制中...', state=DISABLED, bg='sky blue')
        adb_pid_list1 = self.check_adb()
        # print(adb_pid_list1)
        def record_command():
            os.popen('adb shell screenrecord /sdcard/1.mp4')
        record_thread = MyThread(record_command)
        record_thread.start()
        time.sleep(1)
        adb_pid_list2 = self.check_adb()
        # print(adb_pid_list2)
        for i in adb_pid_list2:
            if i not in adb_pid_list1:
                record_pid = i
                # print(record_pid)
                return record_pid
            else:
                continue

    def pull_record(self):
        time.sleep(1)
        os.popen('adb pull /sdcard/1.mp4 ' + desktop_path + '\%s.mp4' % get_info.get_time())
        time.sleep(5)
        os.popen('adb shell rm /sdcard/1.mp4')

    def stop_recording(self):
        """停止并导出录制的视频"""
        global record_pid
        b35.configure(text='录制屏幕', state=NORMAL, bg='blue')

        def stop_record():
            os.popen('taskkill /f /pid ' + record_pid)
            self.pull_record()

        stop_record_thread = MyThread(stop_record)
        stop_record_thread.start()


class PackageManage(object):
    """安装包管理"""
    app = APP()

    def pull_app(self):
        """导出手机安装包"""
        text.insert(END, '正在导出...')
        def pull():
            try:
                app_path = os.popen('adb shell pm path ' + listbox.get(listbox.curselection())).readline()
                pck_name = listbox.get(listbox.curselection())
                flag = 1
            except _tkinter.TclError:
                flag = 0
                text.insert(END, '请先选择一个包名\n')
                text.see(END)
                text.update()
            if flag == 1:
                try:
                    os.popen('adb pull ' + app_path.replace('package:', '').strip() + ' ' + desktop_path
                             + '\\%s.apk' % pck_name.strip())
                    text.insert(END, 'ok!\n已保存至桌面\n')
                except Exception:
                    text.insert(END, '导出apk失败,请重新尝试')
        pull_app_thread = MyThread(pull)
        pull_app_thread.start()

    def display_installed_app(self):
        """列出已安装的第三方app（按照：应用图标+应用名+包名 方式展示）"""

        def display_app():
            listbox.delete(first=0, last=END)
            listbox.insert(END, '获取中请稍等...')
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

        display_app_thread = MyThread(display_app)
        display_app_thread.start()

    def uninstall_app(self):
        """卸载选中的app（按包名）"""
        if len(listbox.curselection()) > 0:
            try:
                if askyesno('提示', '是否确认删除该应用？') is True:
                    text.insert(END, '卸载成功,已重新加载应用列表')
                    os.popen('adb uninstall ' + listbox.get(listbox.curselection()))
                    self.app.clear_two()
                    self.display_installed_app()
                    listbox.update()
                else:
                    pass
            except Exception:
                text.insert(END, '请先选择一个包名\n')
                text.see(END)
                text.update()
        else:
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
        os.popen('adb shell am start ' + get_info.get_launchable_activity())

    def get_uid(self):
        content = os.popen('adb shell ps | findstr ' + listbox.get(listbox.curselection())).read()
        UID = content.split()[0].replace('_', '')
        return UID

    def reset_battery(self):
        os.popen('adb shell dumpsys batterystats --reset')

    def set_usb(self):
        askyesno(title='耗电量测试', message='是否开始测试')
        os.popen('adb shell dumpsys battery unplug')
        os.popen('adb shell dumpsys battery set status 1')
        b22.configure(text='正在测试...', state=DISABLED, bg='#dddddd')

    def rec_usb(self):
        os.popen('adb shell dumpsys battery reset')

    def get_batteryinfo(self):
        content = os.popen('adb shell dumpsys batterystats|findstr ' + self.get_uid()).read()
        batteryinfo = (str(re.findall('(?<=[(])[^()]+\.[^()]+(?=[)])', content)).replace('[', '')).replace(']', '')
        return batteryinfo

    def stop_app(self):
        os.popen('adb shell am force-stop ' + listbox.get(listbox.curselection()))

    def run(self):
        b22.configure(text='测试前准备...', bg='#dddddd', state=DISABLED)
        try:
            self.start_app()
            flag = 1
        except IndexError:
            flag = 0
            b22.configure(text='耗电量测试', state=NORMAL, bg='green')
        except TypeError:
            flag = 0
            b22.configure(text='耗电量测试', state=NORMAL, bg='green')

        if flag == 1:
            time.sleep(2)
            self.get_uid()
            time.sleep(1)
            self.reset_battery()
            time.sleep(1)
            self.set_usb()
            time.sleep(test_time)
            self.rec_usb()
            time.sleep(2)
            self.get_batteryinfo()
            time.sleep(1)
            self.stop_app()
            text.insert(END, '测试结束，结果如下: ' + '\n')
            text.insert(END, self.get_batteryinfo().replace("'", "") + '\n')
            text.see(END)
            text.update()
            b22.configure(text='耗电量测试', state=NORMAL, bg='green')
        else:
            b22.configure(text='耗电量测试', state=NORMAL, bg='green')

    def battery_test(self):
        ask_info()
        battery_test_thread = MyThread(self.run)
        battery_test_thread.start()


class MyDialog(Toplevel):
    def __init__(self):
        super().__init__()
        self.title('设置测试时间')
        # self.geometry('250x73')
        # self.resizable(width=False, height=False)
        # 弹窗界面
        self.setup_UI()

    def setup_UI(self):
        global user_input
        frm1 = Frame(self, bg='sky blue')
        frm1.pack(fill=BOTH)
        Label(frm1, text='时间(s)：', bg='sky blue', font=('楷体', 12)).grid(row=0, column=0, padx=5, pady=8)
        user_input = IntVar()
        user_input.set('')
        e1 = Entry(frm1, textvariable=user_input, bg='pink', width=20)
        e1.grid(row=0, column=1, padx=5, pady=8)
        btn1 = Button(frm1, text="取消", width=12, bg='green', fg='gold', activebackground='sky blue', command=self.cancel)
        btn1.grid(row=1, column=1, padx=5, pady=8, sticky=NE)
        btn2 = Button(frm1, text="确定", width=12, bg='green', fg='gold', activebackground='sky blue', command=self.ok)
        btn2.grid(row=1, column=0, padx=5, pady=8, sticky=NW)
        e1.focus()

    def ok(self):
        global test_time
        test_time = user_input.get()
        self.destroy()  # 销毁窗口

    def cancel(self):
        global test_time
        test_time = None
        self.destroy()


# 右键功能
def catch_log_pck(event):
    b32.configure(text='过滤抓取中...', state=DISABLED)
    os.popen(
        'adb logcat -v time | find "%s" > ' % listbox.get(listbox.curselection()) + get_info.get_desktop_path() +
        '/%s.txt' % get_info.get_time())


def create_window():
    global root
    root = Tk()
    root.title('测试小帮手')
    root.geometry('800x600')
    root.resizable(width=False, height=False)


def ask_info():
    input_dialog = MyDialog()
    Tk.wait_window(input_dialog)  # 这一句很重要
    return test_time


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

create_window()
# 左右显示屏
frm1 = Frame(root)
text = Text(frm1, width=39, height='22', bg='sky blue', fg='green', font=('宋体', 14))
text.pack(side=LEFT, fill=Y, padx=2)
listbox = Listbox(frm1, width=39, height='22', bg='sky blue', fg='green', font=('宋体', 14))
listbox.pack(side=RIGHT, fill=Y, padx=2)
frm1.pack(padx=3, pady=3)

frm2 = Frame(root)
b11 = Button(frm2, text='获取设备信息', activebackground='sky blue', width='15', height='1', bg='green', fg='gold',
             command=get_info.get_device_info)
b11.grid(row=0, column=0)

b12 = Button(frm2, text='启动时间测试', activebackground='sky blue', width='15', height='1', bg='green', fg='gold',
             command=get_info.get_start_time)
b12.grid(row=0, column=1)

b13 = Button(frm2, text='内存/CPU测试', activebackground='sky blue', width='15', height='1', bg='green', fg='gold',
             command=get_info.memory_cpu_monitor)
b13.grid(row=0, column=2)
# 图片
img0 = PhotoImage(file=os.path.abspath(os.path.join(BASE_PATH, '1.gif')))
label0 = Label(frm2, image=img0, width=97, height=50, bg='sky blue')
label0.grid(row=0, column=3, rowspan=2, sticky=N + S)

b14 = Button(frm2, text='本机应用列表', activebackground='sky blue', width='15', height='1', bg='green', fg='gold',
             command=pck_manage.display_installed_app)
b14.grid(row=0, column=4)

b15 = Button(frm2, text='强行停止', activebackground='sky blue', width='15', height='1', bg='green', fg='gold',
             command=app_operate.force_stop_app)
b15.grid(row=0, column=5)
b16 = Button(frm2, text='清除数据', activebackground='sky blue', width='15', height='1', bg='green', fg='gold',
             command=app_operate.clear_app_data)
b16.grid(row=0, column=6)
b21 = Button(frm2, text='微信官网版本', activebackground='sky blue', width='15', height='1', bg='green', fg='gold',
             command=get_info.check_wechart_version)
b21.grid(row=1, column=0)

b22 = Button(frm2, text='耗电量测试', activebackground='sky blue', width='15', height='1', bg='green', fg='gold',
             command=battery.battery_test)
b22.grid(row=1, column=1)

b23 = Button(frm2, text='清理左屏', activebackground='sky blue', width='15', height='1', bg='sky blue', fg='red',
             command=app.clear_one)
b23.grid(row=1, column=2)
b24 = Button(frm2, text='清理右屏', activebackground='sky blue', width='15', height='1', bg='sky blue', fg='red',
             command=app.clear_two)
b24.grid(row=1, column=4)
b25 = Button(frm2, text='导出安装包', activebackground='sky blue', width='15', height='1', bg='green', fg='gold',
             command=pck_manage.pull_app)
b25.grid(row=1, column=6)
b26 = Button(frm2, text='卸载应用', activebackground='sky blue', width='15', height='1', bg='green', fg='gold',
             command=pck_manage.uninstall_app)
b26.grid(row=1, column=5)
frm2.pack(side=TOP, fill=BOTH, padx=3)

frm3 = Frame(root)
b31 = Button(frm3, text='手机截图', activebackground='sky blue', width='15', height='1', bg='blue', fg='white',
             command=screen_operate.screen_shot)
b31.grid(row=0, column=0)

b32 = Button(frm3, text='抓取log', activebackground='sky blue', width='15', height='1', bg='blue', fg='white',
             command=log.catch_log)
b32.grid(row=0, column=1)
b32.bind('<ButtonPress-3>', catch_log_pck)

b33 = Button(frm3, text='停止log', activebackground='sky blue', width='15', height='1', bg='blue', fg='white',
             command=log.stop_log).grid(row=0, column=2)
b34 = Button(frm3, text='清屏', activebackground='sky blue', width='13', height='1', bg='sky blue', fg='red',
             command=app.clear)
b34.grid(row=0, column=3)
b35 = Button(frm3, text='录制屏幕', activebackground='sky blue', width='15', height='1', bg='blue', fg='white',
             command=screen_operate.recording)
b35.grid(row=0, column=4)

b36 = Button(frm3, text='停止录制并导出', activebackground='sky blue', width='15', height='1', bg='blue', fg='white',
             command=screen_operate.stop_recording)
b36.grid(row=0, column=5)

b37 = Button(frm3, text='退出', width='15', height='1', bg='red', fg='black', command=app.quit).grid(row=0, column=6)
frm3.pack(side=TOP, fill=BOTH, padx=3, pady=3)

frm = Frame(root)
label1 = Label(frm, text='Auth:EternalSunshine', height='2', font=('粗体', 18), bg='orchid', fg='gold')
label1.pack(fill=BOTH)
frm.pack(side=TOP, fill=BOTH, padx=3, pady=3)

mainloop()
