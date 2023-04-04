import sys

from PySide6 import QtWidgets, QtCore, QtGui


class CategoryDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(CategoryDialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Category dialog")

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


    def fill_dialog(self, category):
        self.name_lineedit.setText(category.name)
        self.description_lineedit.setText(category.description)


    def ok_callback(self):
        if not self._validate():
            return
        self.data_dict = {
            "name" : self.name_lineedit.text(),
            "description" : self.description_lineedit.text(),
        }
        self.accept()
        self.close()


    def _validate(self):
        return self._validate_field(self.name_lineedit)


    def _validate_field(self, field):
        if field.text() == "" or field.text().isspace():
            field.setStyleSheet("background: #ff7f7f")
            return False
        field.setStyleSheet("background: white")
        return True


    def cancel_callback(self):
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

