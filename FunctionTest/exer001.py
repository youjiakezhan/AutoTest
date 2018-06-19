from selenium import webdriver
import sys
import time


def screen_shot(self):
    path = sys.path[0]
    driver = webdriver.Chrome()
    url = r"C:\Users\BAIWAN\PycharmProjects\AutoTest\FunctionTest\test_result\report\双开助手测试报告180615171926.html"
    driver.get(url)
    time.sleep(1)
    driver.save_screenshot(path + "\sohu.png")
