import sys
from PySide6 import QtCore, QtGui


# https://stackoverflow.com/questions/58278508/get-visual-feedback-from-qvalidator

class RegExpValidator(QtGui.QRegularExpressionValidator):
    validationChanged = QtCore.Signal(QtGui.QValidator.State)

    def validate(self, input, pos):
        state, input, pos = super().validate(input, pos)
        self.validationChanged.emit(state)
        return state, input, pos
