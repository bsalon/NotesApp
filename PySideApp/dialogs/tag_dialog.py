import sys

from PySide6 import QtWidgets, QtCore, QtGui


class TagDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        """
        Initializes tag dialog with all its widgets
        """

        super(TagDialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Tag dialog")

        dialog_layout = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()
        
        # Tag name
        self.name_lineedit = QtWidgets.QLineEdit()
        name_label = QtWidgets.QLabel("Name:", objectName="black_label")
        form_layout.addRow(name_label, self.name_lineedit)
        
        # Tag description
        self.description_lineedit = QtWidgets.QLineEdit()
        description_label = QtWidgets.QLabel("Description:", objectName="black_label")
        form_layout.addRow(description_label, self.description_lineedit)
        
        # Buttons
        btnBox = QtWidgets.QDialogButtonBox()
        btnBox.setStandardButtons(QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel)
        btnBox.button(QtWidgets.QDialogButtonBox.Save).setObjectName("black_pbutton")
        btnBox.button(QtWidgets.QDialogButtonBox.Cancel).setObjectName("black_pbutton")
        btnBox.accepted.connect(self.ok_callback)
        btnBox.rejected.connect(self.cancel_callback)

        form_layout.addItem(QtWidgets.QSpacerItem(0, 20))

        dialog_layout.addLayout(form_layout)
        dialog_layout.addWidget(btnBox)
        self.setLayout(dialog_layout)
        dialog_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)


    def fill_dialog(self, tag):
        """
        Fills dialog widgets with tag values

        :param tag: Tag object
        """

        self.name_lineedit.setText(tag.name)
        self.description_lineedit.setText(tag.description)


    def ok_callback(self):
        """
        Fills data_dict property with field values and closes the dialog
        """

        if not self._validate():
            return
        self.data_dict = {
            "name" : self.name_lineedit.text(),
            "description" : self.description_lineedit.text(),
        }
        self.accept()
        self.close()


    def _validate(self):
        """
        Validates name field
        """

        return self._validate_field(self.name_lineedit)


    def _validate_field(self, field):
        """
        Validates field value by testing if its empty

        :param field: Field to be validated

        :return: True if field value is not empty False otherwise
        """

        if field.text() == "" or field.text().isspace():
            field.setStyleSheet("background: #ff7f7f")
            return False
        field.setStyleSheet("background: white")
        return True


    def cancel_callback(self):
        """
        Closes the dialog
        """

        self.close()



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

