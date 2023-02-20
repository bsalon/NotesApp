import sys
from PyQt5 import QtCore, QtGui, QtWidgets


# https://stackoverflow.com/questions/58278508/get-visual-feedback-from-qvalidator

class RegExpValidator(QtGui.QRegularExpressionValidator): # TODO
    validationChanged = QtCore.pyqtSignal(QtGui.QValidator.State)

    def validate(self, input, pos):
        state, input, pos = super().validate(input, pos)
        self.validationChanged.emit(state)
        return state, input, pos


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        regexp = QtCore.QRegularExpression(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
        validator = RegExpValidator(regexp, self) # TODO
        
        validator.validationChanged.connect(self.handleValidationChange) # TODO
        
        self.edit = QtWidgets.QLineEdit()
        self.edit.setValidator(validator)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.edit)

    def handleValidationChange(self, state): # TODO
        if state == QtGui.QValidator.Invalid:
            colour = 'red'
        elif state == QtGui.QValidator.Intermediate:
            colour = 'gold'
        elif state == QtGui.QValidator.Acceptable:
            colour = 'lime'
        self.edit.setStyleSheet('border: 3px solid %s' % colour)
        QtCore.QTimer.singleShot(1000, lambda: self.edit.setStyleSheet(''))


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
