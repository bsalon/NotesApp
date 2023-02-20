from PySide6 import QtWidgets, QtCore


class ClickableQLabel(QtWidgets.QLabel):
    clicked = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super(ClickableQLabel, self).__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        self.clicked.emit()
