import htmlPy

web_app = htmlPy.WebAppGUI(title=u"Python Website", maximized=True)
web_app.url = u"http://www.douban.com/"

web_app.start()