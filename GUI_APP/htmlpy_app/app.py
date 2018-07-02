# coding=utf-8
import os
import htmlPy
from PySide import QtGui
from GUI_APP.htmlpy_app.back_end import BackEnd

app = htmlPy.AppGUI(title=u"安卓测试工具", maximized=False, plugins=True)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # 本文件所在位置的绝对路径
app.template_path = os.path.join(BASE_DIR, 'templates/')
app.static_path = os.path.join(BASE_DIR, 'static/')
app.window.setWindowIcon(QtGui.QIcon(BASE_DIR + "/static/img/icon.png"))  # 设置APP窗口图标
# app.web_app.setMinimumWidth(1024)
# app.web_app.setMinimumHeight(768)

app.bind(BackEnd(app))

app.template = ("template1.html", {})

if __name__ == "__main__":
    app.start()
