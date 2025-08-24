import sys

from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (
    QMainWindow,
    QApplication
)




class view(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setUrl(QUrl("http://10.187.208.136:8000"))

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle('ChatApp')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    no: view = view()
    no.show()
    sys.exit(app.exec())

