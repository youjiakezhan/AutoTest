# coding=utf-8

from AutoTest.performancetest.app_launch_time import *
from AutoTest.performancetest.cpu_mem import *
from AutoTest.performancetest.network_data_traffic import *
from AutoTest.performancetest.power_consumption import *


# 执行各项性能测试的run方法
while True:
    try:
        run_start_time()
        time.sleep(10)
        run_cpu_mem()
        time.sleep(10)
        run_network()
        time.sleep(10)
        run_power()
        time.sleep(10)
        break
    except Exception:
        print('error! restarting...')
        continue