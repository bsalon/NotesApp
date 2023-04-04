# importing required librarie

import sys

from PySide6 import QtCore, QtWidgets, QtGui


class TimeWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(TimeWidget, self).__init__(*args, **kwargs)

        layout = QtWidgets.QVBoxLayout()
        
        self.label = QtWidgets.QLabel()
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        
        layout.addWidget(self.label)
        self.setLayout(layout)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)


    # method called by timer
    def showTime(self):
        current_time = QtCore.QDateTime.currentDateTime()
        label_time = current_time.toString('dd.MM.yyyy\nhh:mm:ss')
        self.label.setText(label_time)


if __name__ == "__main__":
    App = QtWidgets.QApplication(sys.argv)
    window = TimeWidget()
    window.show()
    App.exit(App.exec())
