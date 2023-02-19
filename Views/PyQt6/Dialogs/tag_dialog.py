import sys

from PySide6 import QtWidgets, QtCore, QtGui


class TagDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(TagDialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Tag")
        
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
        if "action" == "create":
            pass
        elif "action" == "edit":
            pass
        else:
            pass
        self.close()


    def cancel_callback(self):
        print("CLOSE")
        self.close()


    def edit_tag(self):
        pass
        # get note data
        # call controller


    def save_tag(self):
        pass
        # get data
        # create class?
        # call controller



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet('''
QDialog {
    background: #d7eb5a;
}
    ''')
    dialog = TagDialog(objectName="dialog")
    dialog.show()
    sys.exit(app.exec())

