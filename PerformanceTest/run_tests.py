# coding=utf-8
import time

from AutoTest.performancetest.launch_time import run_start_time
from AutoTest.performancetest.comman import d
from AutoTest.performancetest.cpu_mem import run_cpu_mem
from AutoTest.performancetest.net_data_flow import run_network
from AutoTest.performancetest.power import run_power


def run(state):
    run_start_time(state, 22)
    time.sleep(5)
    run_cpu_mem(state, 30, 60)
    time.sleep(5)
    run_network(state, 300)
    time.sleep(5)
    run_power(state, 300)
    time.sleep(5)
    d.service('uiautomator').stop()


# 执行各项性能测试的run方法
run(state='debug')
