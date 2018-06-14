import htmlPy


class BackEnd(htmlPy.Object):

    def __init__(self, app):
        super(BackEnd, self).__init__()
        self.app = app

    @htmlPy.Slot()
    def func1(self):
        self.app.html = u"111111111111111111111111"
