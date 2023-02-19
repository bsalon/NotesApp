from PySide6 import QtWidgets, QtCore, QtGui

import sys

class CheckableComboBox(QtWidgets.QComboBox):
    def __init__(self, parent=None):
        super(CheckableComboBox, self).__init__(parent)
        self.view().pressed.connect(self.handleItemPressed)
        self._changed = False

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)
        self._changed = True

    def hidePopup(self):
        if not self._changed:
            super(CheckableComboBox, self).hidePopup()
        self._changed = False

    def itemChecked(self, index):
        item = self.model().item(index, self.modelColumn())
        return item.checkState() == QtCore.Qt.Checked

    def setItemChecked(self, index, checked=True):
        item = self.model().item(index, self.modelColumn())
        if checked:
            item.setCheckState(QtCore.Qt.Checked)
        else:
            item.setCheckState(QtCore.Qt.Unchecked)

class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.combo = CheckableComboBox(self)
        for index in range(6):
            self.combo.addItem('Item %d' % index)
            self.combo.setItemChecked(index, False)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.combo)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 200, 100)
    window.show()
    sys.exit(app.exec_())
