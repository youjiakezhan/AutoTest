# _*_ coding:utf-8 _*_
import _tkinter
import os
import threading
import time
import tkinter
import winreg  # windows API
from tkinter import *
from tkinter.messagebox import askyesno

from requests_html import HTMLSession


def disable_btn():
    b11.configure(bg='#eeeeee', state=DISABLED)
    b12.configure(bg='#eeeeee', state=DISABLED)
    b13.configure(bg='#eeeeee', state=DISABLED)
    b14.configure(bg='#eeeeee', state=DISABLED)
    b15.configure(bg='#eeeeee', state=DISABLED)
    b16.configure(bg='#eeeeee', state=DISABLED)
    b21.configure(bg='#eeeeee', state=DISABLED)
    b22.configure(bg='#eeeeee', state=DISABLED)
    b25.configure(bg='#eeeeee', state=DISABLED)
    b26.configure(bg='#eeeeee', state=DISABLED)
    b31.configure(bg='#eeeeee', state=DISABLED)
    b32.configure(bg='#eeeeee', state=DISABLED)
    b33.configure(bg='#eeeeee', state=DISABLED)
    b34.configure(bg='#eeeeee', state=DISABLED)
    b35.configure(bg='#eeeeee', state=DISABLED)
    b36.configure(bg='#eeeeee', state=DISABLED)


def enable_btn():
    b11.configure(bg='green', state=NORMAL)
    b12.configure(bg='green', state=NORMAL)
    b13.configure(bg='green', state=NORMAL)
    b14.configure(bg='green', state=NORMAL)
    b15.configure(bg='green', state=NORMAL)
    b16.configure(bg='green', state=NORMAL)
    b21.configure(bg='green', state=NORMAL)
    b22.configure(bg='green', state=NORMAL)
    b25.configure(bg='green', state=NORMAL)
    b26.configure(bg='green', state=NORMAL)
    b31.configure(bg='blue', state=NORMAL)
    b32.configure(bg='blue', state=NORMAL)
    b33.configure(bg='blue', state=NORMAL)
    b34.configure(bg='sky blue', state=NORMAL)
    b35.configure(bg='blue', state=NORMAL)
    b36.configure(bg='blue', state=NORMAL)


def usb_change_handle():
    global monitor_flag, record_pid, user_input
    flag = 1
    while True:
        if flag == 1:
            if 'device' not in os.popen('adb devices').read().split():
                text.insert(END, 'USB连接已断开，请重新连接...\n')
                monitor_flag = 0
                record_pid = None
                user_input = None
                flag = 0
                disable_btn()
        else:
            if 'device' in os.popen('adb devices').read().split():
                text.insert(END, 'USB已重新连接\n')
                enable_btn()
                flag = 1


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
            # text.insert(END, '正在获取,请稍等...')
            b11.configure(text='获取中...', bg='sky blue', state=DISABLED)
            info_list.append('手机品牌：' + os.popen('adb shell getprop ro.product.brand').read().strip())
            info_list.append('手机型号：' + os.popen('adb shell getprop ro.product.model').read().strip())
            info_list.append('安卓版本：' + os.popen('adb shell getprop ro.build.version.release').read().strip())
            info_list.append('序列号：' + os.popen('adb get-serialno').read().strip())
            info_list.append('CPU位数：' + os.popen('adb shell getprop ro.zygote').read().strip())
            info_list.append('屏幕分辨率：' + os.popen('adb shell wm size').read().replace('Physical size:', '').strip())
            info_list.append('像素密度：' + os.popen('adb shell wm density').read().replace('Physical density:', '').strip())
            # text.insert(END, 'ok!\n')
            for line in info_list:
                text.insert(END, line + '\n')
                text.see(END)
                text.update()
            b11.configure(text='设备信息', bg='green', state=NORMAL)

        info_list = []
        if 'device' in os.popen('adb devices').read().split():
            get_device_info_thread = MyThread(device_info)
            get_device_info_thread.start()
        else:
            text.insert(END, '请检查USB连接或是否已开启调试模式\n')

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
            text.insert(END, '导出apk文件失败')

    def get_launchable_activity(self):
        """获取选中包名的启动入口"""
        activity = ''
        launch_activity = ''
        if len(listbox.curselection()) > 0:
            pck_name = listbox.get(listbox.curselection())
            data = os.popen('adb shell monkey -v -v -v 0').readlines()
            for i in data:
                if pck_name.strip() in i:
                    activity = i.split()[5]
            if activity is not None:
                launch_activity = pck_name.strip() + '/' + activity
                print(launch_activity)
            return launch_activity
        else:
            text.insert(END, '请先选择一个包名\n')
            text.see(END)
            text.update()

    def get_apk_name(self):
        pass

    # 启动时间测试入口
    def app_start_time_test(self):
        def input_start_time_test_info():
            if len(listbox.curselection()) > 0:
                b12.configure(text='环境准备中', state=DISABLED, bg='#dddddd')
                input_dialog = StartTimeDialog()
                Tk.wait_window(input_dialog)
                if start_time_test_off == 0:
                    text.insert(END, '测试已取消\n')
                else:
                    text.insert(END, '测试开始...\n')
                    b12.configure(text='正在测试', state=DISABLED, bg='#dddddd')
                    start = StartTimeTest()
                    start.start_time_test()
            else:
                text.insert(END, '请先选择一个包名\n')
            b12.configure(text='启动时间', state=NORMAL, bg='green')

        if 'device' in os.popen('adb devices').read().split():
            start_time_test_thread = MyThread(input_start_time_test_info)
            start_time_test_thread.start()
        else:
            text.insert(END, '请检查USB连接或是否已开启调试模式\n')

    # 性能监控
    def mem_cpu_monitor(self):
        global monitor_flag
        monitor_flag = 1

        def get_mem_cpu_info():
            if len(listbox.curselection()) > 0:
                text.insert(END, '性能监控已开启\n')
                b13.configure(text='右键停止', bg='red')
                pkg_name = listbox.get(listbox.curselection())
                while True:
                    # print(threading.current_thread())
                    if monitor_flag == 1:
                        mem = 0
                        cpu = 0
                        mem_datas = os.popen('adb shell dumpsys meminfo | findstr ' + pkg_name).readlines()
                        cpu_datas = os.popen('adb shell dumpsys cpuinfo | findstr ' + pkg_name).readlines()
                        for data in cpu_datas:
                            n = round(float(data.split()[0].replace('%', '')), 1)
                            cpu += n
                        for data in mem_datas[:int(len(mem_datas) / 2)]:
                            m = int(data.split()[0].replace('K:', '').replace(',', ''))
                            mem += m
                        text.insert(END, '内存：%s, cpu：%s\n' % (mem, cpu))
                        text.update()
                        text.see(END)
                    else:
                        text.insert(END, '性能监控已关闭\n')
                        break
            else:
                text.insert(END, '请先选择一个包名\n')

        if 'device' in os.popen('adb devices').read().split():
            thread = threading.Thread(target=get_mem_cpu_info)
            thread.start()
        else:
            text.insert(END, '请检查USB连接或是否已开启调试模式\n')


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
        """录制屏幕"""
        global record_pid
        adb_count = len(os.popen('tasklist | findstr "adb.exe"').readlines())

        def record_command():
            os.popen('adb shell screenrecord /sdcard/record.mp4')

        adb_pid_list1 = self.check_adb()
        if 'device' in os.popen('adb devices').read().split():
            record_thread = MyThread(record_command)
            record_thread.start()
            time.sleep(1)
            if len(os.popen('tasklist | findstr "adb.exe"').readlines()) == adb_count:
                text.insert(END, '该手机型号不支持录屏\n')
            else:
                b35.configure(text='录制中...', state=DISABLED, bg='red')
        else:
            text.insert(END, '请检查USB连接或是否已开启调试模式\n')
        # time.sleep(path)
        adb_pid_list2 = self.check_adb()
        for i in adb_pid_list2:
            if i not in adb_pid_list1:
                record_pid = i
                return record_pid

    def pull_record(self):
        time.sleep(1)
        os.popen('adb pull /sdcard/record.mp4 ' + desktop_path + '\%s.mp4' % get_info.get_time())
        time.sleep(5)
        os.popen('adb shell rm /sdcard/record.mp4')

    def stop_recording(self):
        """停止并导出录制的视频"""
        global record_pid
        b35.configure(text='录制屏幕', state=NORMAL, bg='blue')

        def stop_record():
            b36.configure(text='正在导出...', bg='sky blue', state=DISABLED)
            os.popen('taskkill /f /pid ' + record_pid)
            text.insert(END, '已停止录制，正在导出...')
            self.pull_record()
            text.insert(END, 'ok!\n视频已导出至桌面\n')
            b36.configure(text='停止录制并导出', bg='blue', state=NORMAL)

        if len(record_pid) != 0:
            stop_record_thread = MyThread(stop_record)
            stop_record_thread.start()
        else:
            text.insert(END, '请先进行录制\n')


class PackageManage(object):
    """安装包管理"""
    app = APP()

    def pull_app(self):
        """导出手机安装包"""

        def pull():
            app_path = ''
            pck_name = ''
            try:
                pck_name = listbox.get(listbox.curselection())
                app_path = os.popen('adb shell pm path ' + pck_name).read().replace('package:', '').strip()
                # print(app_path)
                text.insert(END, '正在导出,请稍等...')
                flag = 1
            except _tkinter.TclError:
                flag = 0
                text.insert(END, '请先选择一个包名\n')
                text.see(END)
                text.update()
            if flag == 1:
                try:
                    os.popen('adb pull ' + app_path + ' ' + desktop_path + '\\%s.apk' % pck_name.strip())
                    time.sleep(5)  # 需要优化（科学判断是否已导出完毕）
                    text.insert(END, 'ok!\n已导出至桌面\n')
                except Exception:
                    text.insert(END, '导出apk失败,请重新尝试\n')

        pull_app_thread = MyThread(pull)
        pull_app_thread.start()

    def display_installed_app(self):
        """列出已安装的第三方app（按照：应用图标+应用名+包名 方式展示）"""

        def display_app():
            b14.configure(text='获取中...', bg='sky blue', state=DISABLED)
            listbox.delete(first=0, last=END)
            # text.insert(END, '正在获取,请稍等...')
            pck_names = os.popen('adb shell pm list packages -3 | sort')
            for pck_name in pck_names:
                listbox.insert(END, pck_name.replace('package:', ''))
                listbox.see(END)
                listbox.update()
            # text.insert(END, 'ok!\n应用列表已加载完毕\n')
            b14.configure(text='应用列表', bg='green', state=NORMAL)

        data = os.popen('adb devices').read()
        if 'device' in data.split():
            display_app_thread = MyThread(display_app)
            display_app_thread.start()
        else:
            text.insert(END, '请检查USB连接或是否已开启调试模式\n')
        b14.configure(text='本机应用列表', bg='green')

    def uninstall_app(self):
        """卸载选中的app（按包名）"""
        if len(listbox.curselection()) > 0:
            try:
                if askyesno('提示', '是否确认删除该应用？') is True:
                    text.insert(END, '卸载成功,已重新加载应用列表\n')
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
        os.popen('adb shell dumpsys battery set status path')
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

    def battery_test(self):
        data = os.popen('adb devices').read()
        if 'device' in data.split():
            if len(listbox.curselection()) > 0:
                b22.configure(text='环境准备中...', bg='#dddddd', state=DISABLED)
                ask_info()
                if test_time is not None:
                    battery_test_thread = MyThread(self.run)
                    battery_test_thread.start()
                else:
                    text.insert(END, '已取消测试\n')
                    b22.configure(text='功耗测试', state=NORMAL, bg='green')
            else:
                text.insert(END, '请先选择一个包名\n')
        else:
            text.insert(END, '请检查USB连接或是否已开启调试模式\n')


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
        Label(frm1, text='测试时间(s)：', bg='sky blue', font=('楷体', 12)).grid(row=0, column=0, padx=5, pady=8)
        user_input = IntVar()
        user_input.set('')
        e1 = Entry(frm1, textvariable=user_input, bg='pink', width=20)
        e1.grid(row=0, column=1, padx=5, pady=8)
        btn1 = Button(frm1, text="取消", width=12, bg='green', fg='gold', activebackground='sky blue',
                      command=self.cancel)
        btn1.grid(row=1, column=1, padx=5, pady=8, sticky=NE)
        btn2 = Button(frm1, text="确定", width=12, bg='green', fg='gold', activebackground='sky blue', command=self.ok)
        btn2.grid(row=1, column=0, padx=5, pady=8, sticky=NW)
        e1.focus()

    def ok(self):
        global test_time
        try:
            test_time = user_input.get()
            flag = 1
        except _tkinter.TclError:
            flag = 0
            text.insert(END, '请输入测试时间并点击确定按钮开始测试\n')
        if flag == 1:
            self.destroy()  # 销毁窗口

    def cancel(self):
        global test_time
        test_time = None
        self.destroy()


class StartTimeDialog(Toplevel):
    def __init__(self):
        super().__init__()
        self.title('测试配置')
        # self.geometry('250x73')
        # self.resizable(width=False, height=False)
        # 弹窗界面
        self.setup_UI()

    def setup_UI(self):
        frm1 = Frame(self, bg='sky blue')
        frm1.pack(fill=BOTH)

        Label(frm1, text='版本号：', bg='sky blue', font=('楷体', 12)).grid(row=0, column=0, padx=5, pady=5, sticky=W)
        var_version = StringVar
        self.e_version = Entry(frm1, textvariable=var_version, bg='pink', width=15)
        self.e_version.grid(row=0, column=1, padx=5, pady=5)
        self.e_version.focus()

        Label(frm1, text='测试次数：', bg='sky blue', font=('楷体', 12)).grid(row=1, column=0, padx=5, pady=5, sticky=W)
        var_nums = IntVar
        self.e_test_num = Entry(frm1, bg='pink', textvariable=var_nums, width=15)
        self.e_test_num.grid(row=1, column=1, padx=5, pady=5)

        frm2 = Frame(self, bg='sky blue')
        frm2.pack(fill=BOTH)

        self.var_back = BooleanVar()
        self.var_home = BooleanVar()
        self.var_force = BooleanVar()
        c1_test_state = Checkbutton(frm2, text='back', variable=self.var_back, bg='sky blue', font=('楷体', 12))
        c1_test_state.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        c2_test_state = Checkbutton(frm2, text='home', variable=self.var_home, bg='sky blue', font=('楷体', 12))
        c2_test_state.grid(row=0, column=1, padx=5, pady=5, sticky=W)
        c3_test_state = Checkbutton(frm2, text='冷启动', variable=self.var_force, bg='sky blue', font=('楷体', 12))
        c3_test_state.grid(row=0, column=2, padx=5, pady=5, sticky=W)

        frm3 = Frame(self, bg='sky blue')
        frm3.pack(fill=BOTH)

        btn1 = Button(frm3, text="取消", bg='green', fg='gold', activebackground='sky blue', command=self.cancel)
        btn1.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        btn2 = Button(frm3, text="确定", bg='green', fg='gold', activebackground='sky blue', command=self.ok)
        btn2.grid(row=0, column=1, padx=5, pady=5, sticky=E)

    def ok(self):
        global test_data_list
        test_data_list = [self.e_version.get(), self.e_test_num.get(), self.var_back.get(), self.var_home.get(),
                          self.var_force.get()]
        # print(test_data_list)
        # print(len(test_data_list[0]), len(test_data_list[path]))
        if len(test_data_list[0]) > 0 and len(test_data_list[1]) > 0:
            self.destroy()
            return test_data_list
        else:
            text.insert(END, '请输入测试数据并点击确定按钮开始测试\n')

    def cancel(self):
        global start_time_test_off
        start_time_test_off = 0
        self.destroy()


# 启动时间测试类
class StartTimeTest(object):
    def __init__(self):
        self.pck_name = listbox.get(listbox.curselection())
        self.launchable_activity = get_info.get_launchable_activity()

    def test_back(self):
        text.insert(END, '场景一：back\n')
        text.see(END)
        text.update()
        sum = 0
        i = 1
        list1 = []
        os.popen('adb shell am start -W ' + self.launchable_activity)
        time.sleep(2)
        os.popen('adb shell input keyevent 4')

        while i <= int(test_data_list[1]):
            time.sleep(2)
            j = "第" + str(i) + "次："
            text.insert(END, j)
            text.see(END)
            text.update()
            p = os.popen('adb shell am start -W ' + self.launchable_activity)
            s = p.read()
            time.sleep(3)
            os.popen('adb shell input keyevent 4')
            b = re.search(r'(TotalTime:)\s(\d+)', s)
            try:
                resu = b.group(2)
                if int(resu) > 1000:
                    text.insert(END, '此次数据异常\n')
                    text.see(END)
                    text.update()
                else:
                    i = i + 1
            except AttributeError:
                text.insert(END, '此次未获取到启动数据！\n')
                text.see(END)
                text.update()
                continue
            text.insert(END, resu + '\n')
            text.see(END)
            text.update()
            result = int(resu)
            if result < 1000:
                list1.append(result)
                sum = sum + result
        else:
            text.insert(END, "最大值为：" + str(max(list1)) + '\n')
            text.insert(END, "最小值为：" + str(min(list1)) + '\n')
            avg = round((sum - max(list1) - min(list1)) / (i - 3), 3)
            text.insert(END, "平均值为：" + str(avg) + '\n')
            text.update()
            # print("平均值为：", colored(avg, "cyan"))

    def test_home(self):
        text.insert(END, '\n场景二：home\n')
        text.see(END)
        text.update()
        i = 1
        sum = 0
        list1 = []
        time.sleep(2)
        os.popen('adb shell am start -W ' + self.launchable_activity)
        time.sleep(2)
        os.popen('adb shell input keyevent 3')
        time.sleep(1)
        os.popen('adb shell am start -W ' + self.launchable_activity)
        time.sleep(2)
        os.popen('adb shell input keyevent 3')
        while i <= int(test_data_list[1]):
            time.sleep(2)
            j = "第" + str(i) + "次："
            # print(j)
            text.insert(END, j)
            text.see(END)
            text.update()
            p = os.popen('adb shell am start -W ' + self.launchable_activity)
            s = p.read()
            time.sleep(3)
            os.popen('adb shell input keyevent 3')
            b = re.search(r'(TotalTime:)\s(\d+)', s)
            try:
                resu = b.group(2)
                if int(resu) > 800:
                    text.insert(END, '此次数据异常\n')
                    text.see(END)
                    text.update()
                else:
                    i = i + 1
            except AttributeError:
                text.insert(END, '此次未获取到启动数据！\n')
                text.see(END)
                text.update()
                continue
            text.insert(END, str(resu) + '\n')
            text.see(END)
            text.update()
            result = int(resu)
            if result < 800:
                list1.append(result)
                sum = sum + result
        else:
            text.insert(END, "最大值为：" + str(max(list1)) + '\n')
            text.insert(END, "最小值为：" + str(min(list1)) + '\n')
            avg = round((sum - max(list1) - min(list1)) / (i - 3), 3)
            text.insert(END, "平均值为：" + str(avg) + '\n')
            text.see(END)
            text.update()

    def test_force(self):
        text.insert(END, '\n场景三：冷启动\n')
        text.see(END)
        text.update()
        i = 1
        sum = 0
        list1 = []
        time.sleep(2)
        os.popen('adb shell am start -W ' + '/' + self.launchable_activity)
        time.sleep(2)
        os.popen('adb shell am force-stop ' + self.pck_name)
        while i <= int(test_data_list[1]):
            time.sleep(2)
            j = "第" + str(i) + "次："
            text.insert(END, j)
            text.see(END)
            text.update()
            time.sleep(1)
            p = os.popen('adb shell am start -W ' + self.launchable_activity)
            s = p.read()
            time.sleep(2)
            b = re.search(r'(TotalTime:)\s(\d+)', s)
            os.popen('adb shell am force-stop ' + self.pck_name)
            try:
                resu = b.group(2)
                if int(resu) > 1800:
                    # print(colored('此次数据异常', "red"))
                    text.insert(END, '此次数据异常' + '\n')
                    text.see(END)
                    text.update()
                else:
                    i = i + 1
            except AttributeError:
                # print('此次未获取到启动数据！')
                text.insert(END, '此次未获取到启动数据！\n')
                text.see(END)
                text.update()
                continue
            text.insert(END, str(resu) + '\n')
            text.see(END)
            text.update()
            result = int(resu)
            if result < 1800:
                list1.append(result)
                sum = sum + result
        else:
            text.insert(END, "最大值为：" + str(max(list1)) + '\n')
            text.insert(END, "最小值为：" + str(min(list1)) + '\n')
            avg = round((sum - max(list1) - min(list1)) / (i - 3), 3)
            text.insert(END, "平均值为：" + str(avg) + '\n')
            text.see(END)
            text.update()
            # print("平均值为：", colored(avg, "cyan"))

    def start_time_test(self):
        style = test_data_list[2:5]
        # print(style)
        if style[0] is True and style[1] is False and style[2] is False:
            self.test_back()
        elif style[0] is False and style[1] is True and style[2] is False:
            self.test_home()
        elif style[0] is False and style[1] is False and style[2] is True:
            self.test_force()
        elif style[0] is True and style[1] is True and style[2] is False:
            self.test_back()
            self.test_home()
        elif style[0] is True and style[1] is False and style[2] is True:
            self.test_back()
            self.test_force()
        elif style[0] is False and style[1] is True and style[2] is True:
            self.test_home()
            self.test_force()
        elif style[0] is True and style[1] is True and style[2] is True:
            self.test_back()
            self.test_home()
            self.test_force()


# 右键功能
def catch_log_pck(event):
    b32.configure(text='过滤抓取中...', state=DISABLED)
    os.popen(
        'adb logcat -v time | find "%s" > ' % listbox.get(listbox.curselection()) + get_info.get_desktop_path() +
        '/%s.txt' % get_info.get_time())


def get_current_app_name(event):
    pattern = re.compile(r"[a-zA-Z0-9\.]+/.[a-zA-Z0-9\.]+")
    out = os.popen("adb shell dumpsys input | findstr FocusedApplication").read()
    package_name = pattern.findall(out)[0].split("/")[0]
    text.insert(END, package_name + '\n')


def create_window():
    global root
    root = Tk()
    root.title('Tester')
    root.geometry('800x600')
    root.resizable(width=False, height=False)


def ask_info():
    input_dialog = MyDialog()
    Tk.wait_window(input_dialog)
    # print(test_time)
    return test_time


def hide_text(event):
    def change_label1_text():
        label1.configure(text='右键"导出安装包"可查看当前应用包名')
        time.sleep(5)
        label1.configure(text='惊不惊喜,意不意外')
        time.sleep(2)
        label1.configure(text='Auth: EtenalSunshine')

    change_label1_text_thread = MyThread(change_label1_text)
    change_label1_text_thread.start()


def stop_cpu_mem_monitor(event):
    global monitor_flag
    monitor_flag = 0
    b13.configure(text='cpu/内存监控', bg='green')


app = APP()
thread = MyThread(usb_change_handle)
get_info = GetInfo()
log = Log()
screen_operate = ScreenOperation()
pck_manage = PackageManage()
app_operate = AppOperation()
battery = BatteryTest()
desktop_path = get_info.get_desktop_path()
BASE_PATH = os.path.abspath(os.path.dirname('__file__'))
record_pid = ''
start_time_test_off = 1

create_window()
thread.start()
# 左右显示屏
frm1 = Frame(root)
text = Text(frm1, width=39, height='22', bg='sky blue', fg='green', font=('楷体', 14))
text.pack(side=LEFT, fill=BOTH, padx=2)
listbox = Listbox(frm1, width=39, height='22', bg='sky blue', fg='green', font=('楷体', 14))
listbox.pack(side=RIGHT, fill=BOTH, padx=2)
frm1.pack(padx=3, pady=3)

frm2 = Frame(root)
b11 = Button(frm2, text='设备信息', activebackground='sky blue', width='15', height='path', bg='green', fg='gold',
             command=get_info.get_device_info)
b11.grid(row=0, column=0)

b12 = Button(frm2, text='启动时间', activebackground='sky blue', width='15', height='path', bg='green', fg='gold',
             command=get_info.app_start_time_test)
b12.grid(row=0, column=1)

b13 = Button(frm2, text='cpu/内存监控', activebackground='sky blue', width='15', height='path', bg='green', fg='gold',
             command=get_info.mem_cpu_monitor)
b13.grid(row=0, column=2)
b13.bind('<ButtonPress-3>', stop_cpu_mem_monitor)
# 图片
img0 = PhotoImage(file=os.path.abspath(os.path.join(BASE_PATH, 'path.gif')))
label0 = Label(frm2, image=img0, width=97, height=50, bg='sky blue')
label0.grid(row=0, column=3, rowspan=2, sticky=N + S)

b14 = Button(frm2, text='应用列表', activebackground='sky blue', width='15', height='path', bg='green', fg='gold',
             command=pck_manage.display_installed_app)
b14.grid(row=0, column=4)

b15 = Button(frm2, text='强行停止', activebackground='sky blue', width='15', height='path', bg='green', fg='gold',
             command=app_operate.force_stop_app)
b15.grid(row=0, column=5)
b16 = Button(frm2, text='清除数据', activebackground='sky blue', width='15', height='path', bg='green', fg='gold',
             command=app_operate.clear_app_data)
b16.grid(row=0, column=6)
b21 = Button(frm2, text='官网微信版本', activebackground='sky blue', width='15', height='path', bg='green', fg='gold',
             command=get_info.check_wechart_version)
b21.grid(row=1, column=0)

b22 = Button(frm2, text='功耗测试', activebackground='sky blue', width='15', height='path', bg='green', fg='gold',
             command=battery.battery_test)
b22.grid(row=1, column=1)

b23 = Button(frm2, text='清理左屏', activebackground='sky blue', width='15', height='path', bg='sky blue', fg='red',
             command=app.clear_one)
b23.grid(row=1, column=2)
b24 = Button(frm2, text='清理右屏', activebackground='sky blue', width='15', height='path', bg='sky blue', fg='red',
             command=app.clear_two)
b24.grid(row=1, column=4)
b25 = Button(frm2, text='导出安装包', activebackground='sky blue', width='15', height='path', bg='green', fg='gold',
             command=pck_manage.pull_app)
b25.grid(row=1, column=6)
b25.bind('<ButtonPress-3>', get_current_app_name)

b26 = Button(frm2, text='卸载应用', activebackground='sky blue', width='15', height='path', bg='green', fg='gold',
             command=pck_manage.uninstall_app)
b26.grid(row=1, column=5)
frm2.pack(side=TOP, fill=BOTH, padx=3)

frm3 = Frame(root)
b31 = Button(frm3, text='手机截图', activebackground='sky blue', width='15', height='path', bg='blue', fg='white',
             command=screen_operate.screen_shot)
b31.grid(row=0, column=0)

b32 = Button(frm3, text='抓取log', activebackground='sky blue', width='15', height='path', bg='blue', fg='white',
             command=log.catch_log)
b32.grid(row=0, column=1)
b32.bind('<ButtonPress-3>', catch_log_pck)

b33 = Button(frm3, text='停止log', activebackground='sky blue', width='15', height='path', bg='blue', fg='white',
             command=log.stop_log)
b33.grid(row=0, column=2)
b34 = Button(frm3, text='清屏', activebackground='sky blue', width='13', height='path', bg='sky blue', fg='red',
             command=app.clear)
b34.grid(row=0, column=3)
b35 = Button(frm3, text='录制屏幕', activebackground='sky blue', width='15', height='path', bg='blue', fg='white',
             command=screen_operate.recording)
b35.grid(row=0, column=4)

b36 = Button(frm3, text='停止录制并导出', activebackground='sky blue', width='15', height='path', bg='blue', fg='white',
             command=screen_operate.stop_recording)
b36.grid(row=0, column=5)

b37 = Button(frm3, text='退出', width='15', height='path', bg='red', fg='black', command=app.quit).grid(row=0, column=6)
frm3.pack(side=TOP, fill=BOTH, padx=3, pady=3)

frm = Frame(root)
var_label1 = StringVar
label1 = Label(frm, text='其他功能', height='bad_path', font=('粗体', 18), bg='orchid', fg='gold')
label1.pack(fill=BOTH)
label1.bind('<ButtonPress-path>', hide_text)
frm.pack(side=TOP, fill=BOTH, padx=3, pady=3)

mainloop()
