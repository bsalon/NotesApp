import sys

from PySide6 import QtCore, QtGui, QtWidgets


# Taken from: https://stackoverflow.com/questions/56806987/switch-button-in-pyqt
class ToggleSwitchButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super(ToggleSwitchButton, self).__init__(*args, **kwargs)
        self.setCheckable(True)
        self.setChecked(True)
        self.setMinimumWidth(70)
        self.setMinimumHeight(40)


    def paintEvent(self, event):
        text_label = "ON" if self.isChecked() else "OFF"
        bg_color = QtGui.QColor(146, 211, 110) if self.isChecked() else QtGui.QColor(255, 138, 132)

        radius = 12
        width = 32
        center = self.rect().center()

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.translate(center)
        painter.setBrush(QtGui.QColor(255, 255, 255))

        pen = QtGui.QPen(bg_color)
        pen.setWidth(2)
        painter.setPen(pen)

        painter.drawRoundedRect(QtCore.QRect(-width, -radius, 2*width, 2*radius), radius, radius)
        painter.setBrush(QtGui.QBrush(bg_color))
        
        sw_rect = QtCore.QRect(-radius, -radius, width + radius, 2*radius)
        if self.isChecked():
            sw_rect.moveLeft(-width)
        painter.drawRoundedRect(sw_rect, radius, radius)

        pen.setColor(QtCore.Qt.black)
        painter.setPen(pen)
        painter.drawText(sw_rect, QtCore.Qt.AlignCenter, text_label)




if __name__ == "__main__":
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    toggle = ToggleSwitchButton()
    toggle.resize(100, 100)
    toggle.show()
    app.exec()
