import sys

from PySide6 import QtWidgets, QtCore, QtGui


class CategoryDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(CategoryDialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Tag")
        
        self.action = action

        dialog_layout = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()
        
        self.name_lineedit = QtWidgets.QLineEdit()
        form_layout.addRow("Name:", self.name_lineedit)
        
        self.description_lineedit = QtWidgets.QLineEdit()
        form_layout.addRow("Description:", self.description_lineedit)
        
        btnBox = QtWidgets.QDialogButtonBox()
        btnBox.setStandardButtons(QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel)
        btnBox.accepted.connect(self.ok_callback)
        btnBox.rejected.connect(self.cancel_callback)

        form_layout.addItem(QtWidgets.QSpacerItem(0, 20))

        dialog_layout.addLayout(form_layout)
        dialog_layout.addWidget(btnBox)
        self.setLayout(dialog_layout)


    def ok_callback(self):
        print("ACCEPTED")
        self.close()


    def cancel_callback(self):
        print("CLOSE")
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet('''
QDialog {
    background: #d7eb5a;
}
    ''')
    dialog = CategoryDialog(objectName="dialog")
    dialog.show()
    sys.exit(app.exec())

