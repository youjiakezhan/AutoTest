from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import time

path = sys.path[0]
# options = Options()
# options.add_argument('--headless')
# options.add_argument('--no-sandbox')
print("start....\n")
driver = webdriver.Chrome()
url = r"E:\AutoTest\AutoTest\FunctionTest\test_result\report\双开助手测试报告180615171926.html"
driver.get(url)
time.sleep(1)
driver.save_screenshot(path + "\sohu.png")
print("ok!\n")