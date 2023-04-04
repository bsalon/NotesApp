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
