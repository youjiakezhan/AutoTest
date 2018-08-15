# coding=utf-8
import time

from AutoTest.performancetest.app_launch_time import run_start_time
from AutoTest.performancetest.comman import d
from AutoTest.performancetest.cpu_mem import run_cpu_mem
from AutoTest.performancetest.network_data_traffic import run_network
from AutoTest.performancetest.power_consumption import run_power


def unlock():
    if d.info['screenOn']:
        print('亮屏，不操作')
    else:
        print('黑屏，点亮屏幕并解锁')
        d.screen_on()
        d.unlock()
        d.press('home')


def run(state):
    try:
        d.healthcheck()
    except Exception:
        d.service('uiautomator').stop()
        time.sleep(2)
        d.healthcheck()
    unlock()
    run_start_time(state)
    time.sleep(30)
    run_cpu_mem(state)
    time.sleep(30)
    run_network(state)
    time.sleep(30)
    run_power(state)
    time.sleep(5)
    d.service('uiautomator').stop()


# 执行各项性能测试的run方法
run(state='debug')
