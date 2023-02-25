import sys

from PySide6 import QtWidgets, QtGui, QtCore


class InfoAlertWidget(QtWidgets.QWidget):
    def __init__(self, text, *args, **kwargs):
        super(InfoAlertWidget, self).__init__(*args, **kwargs)

        alert_icon = QtGui.QIcon()
        alert_icon.addFile("/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/InfoIcon.png")
        alert_icon_button = QtWidgets.QToolButton(objectName="alert_icon_button")
        alert_icon_button.setIcon(alert_icon)
        alert_icon_button.setIconSize(QtCore.QSize(28, 28))
        alert_icon_button.setEnabled(False)
        
        alert_label = QtWidgets.QLabel(text, objectName="alert_text")
        
        alert_cross_icon = QtGui.QIcon(objectName="alert_cross_icon")
        alert_cross_icon.addFile("/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/CrossIcon.png")
        alert_cross_button = QtWidgets.QToolButton(objectName="alert_cross_button")
        alert_cross_button.setIcon(alert_cross_icon)
        alert_cross_button.setIconSize(QtCore.QSize(20, 20))
        alert_cross_button.clicked.connect(self.remove_alert)

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(alert_icon_button,  0, 0, alignment=QtCore.Qt.AlignLeft)
        layout.addWidget(alert_label, 0, 1, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(alert_cross_button, 0, 2, alignment=QtCore.Qt.AlignRight)


    # issue explained here - https://stackoverflow.com/questions/7276330/qt-stylesheet-for-custom-widget
    def paintEvent(self, event):
        option = QtWidgets.QStyleOption()
        option.initFrom(self)
        painter = QtGui.QPainter(self)
        style = self.style()
        style.drawPrimitive(QtWidgets.QStyle.PE_Widget, option, painter, self)


    def remove_alert(self):
        self.setParent(None)
        self.deleteLater()
        self = None



if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setStyleSheet('''
    QToolButton#alert_icon_button {
        background-color: #ffc957;
        border-style: outset;
        border-width: 0px;
    }

    QWidget#info_alert_widget {
        background-color: #ffc957;
        border: 1px solid black;
    }
    
    QToolButton#alert_cross_button {
        background-color: #ffc957;
        border-style: outset;
        border-width: 0px;
    }

    QToolButton#alert_cross_button:hover {
        background-color: #efb947;
    }
    ''')
    alert = InfoAlertWidget("This table is empty", objectName="info_alert_widget")
    alert.show()
    sys.exit(app.exec())
