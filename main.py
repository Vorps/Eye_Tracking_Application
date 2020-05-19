import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
import Models

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("Resources/Images/icon.png"))
    Models.registerTypes()
    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    engine.load('View/EyeTrackingWindow.qml')

    win = engine.rootObjects()[0]
    win.show()
    sys.exit(app.exec_())