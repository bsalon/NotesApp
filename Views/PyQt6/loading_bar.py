import sys
import random
import time

from PySide6 import QtCore, QtWidgets, QtGui


class LoadingBarWidget(QtWidgets.QWidget):
    def __init__(self, barObjectName, *args, **kwargs):
        super(LoadingBarWidget, self).__init__(*args, **kwargs)
        layout = QtWidgets.QVBoxLayout(self)

        self.loading_bar = QtWidgets.QProgressBar(self, objectName=barObjectName)
        self.loading_bar.setRange(0, 1)

        layout.addWidget(self.loading_bar)
        
#        button = QtWidgets.QPushButton("Start", self)
#        layout.addWidget(button)
#        button.clicked.connect(self.onStart)
#
#        self.myLongTask = TaskThread()
#        self.myLongTask.taskFinished.connect(self.onFinished)
#
#    def onStart(self): 
#        self.loading_bar.setRange(0,0)
#        self.myLongTask.start()
#
#    def onFinished(self):
#        self.loading_bar.setRange(0,1)
#
#
#class TaskThread(QtCore.QThread):
#    taskFinished = QtCore.Signal()
#
#    def run(self):
#        time.sleep(3)
#        self.taskFinished.emit()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setStyleSheet('''
#GreenProgressBar {
    min-height: 24px;
    max-height: 24px;
    border-radius: 12px;
    border: 1px solid black;
}

#GreenProgressBar::chunk {
    border-radius: 6px;
    background-color: #92d36e;
}

    ''')

    widget = LoadingBarWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
