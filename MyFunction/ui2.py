# coding=utf-8
import time

import uiautomator2 as u2


class UI2(object):

    # 初始化uiautomator2
    def ui2_init(self):
        global d
        # 初始化uiautomator2
        d = u2.connect()
        time.sleep(2)
        # 启动uiautomator2的守护进程
        d.healthcheck()
        return d
