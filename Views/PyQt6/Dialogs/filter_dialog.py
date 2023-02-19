import sys

from PySide6 import QtWidgets, QtCore, QtGui


class FiltersDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(FiltersDialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Note dialog window")
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        dialog_layout = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()
        
        self.filter_name_lineedit = QtWidgets.QLineEdit()
        form_layout.addRow("Filter name:", self.filter_name_lineedit)
        
        self.filter_order_lineedit = QtWidgets.QLineEdit()
        form_layout.addRow("Filter order:", self.filter_order_lineedit)
        
        form_layout.addItem(QtWidgets.QSpacerItem(0, 20))
        
        self.note_name_lineedit = QtWidgets.QLineEdit()
        form_layout.addRow("Note name:", self.note_name_lineedit)
        
        note_datetime_layout = QtWidgets.QHBoxLayout()
        note_datetime_layout.setContentsMargins(0, 0, 0, 0)
        note_datetime_layout.setAlignment(QtCore.Qt.AlignTop)
        self.note_from_datetime_edit = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime())
        self.note_from_datetime_edit.setDisplayFormat("dd:MM:yyyy hh:mm")
        self.note_from_datetime_edit.setToolTip("Rewrite date and time or use ticks")
        self.note_to_datetime_edit = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime())
        self.note_to_datetime_edit.setDisplayFormat("dd:MM:yyyy hh:mm")
        self.note_to_datetime_edit.setToolTip("Rewrite date and time or use ticks")
        note_datetime_layout.addWidget(self.note_from_datetime_edit, stretch=1)
        note_datetime_layout.addWidget(QtWidgets.QLabel(" - "))
        note_datetime_layout.addWidget(self.note_to_datetime_edit, stretch=1)
        form_layout.addRow("Note date and time range:", note_datetime_layout)
        
        self.note_description_lineedit = QtWidgets.QLineEdit()
        form_layout.addRow("Note description:", self.note_description_lineedit)

        note_priority_layout = QtWidgets.QHBoxLayout()
        note_priority_layout.setContentsMargins(0, 0, 0, 0)
        note_priority_layout.setAlignment(QtCore.Qt.AlignTop)
        self.note_min_priority_lineedit = QtWidgets.QLineEdit()
        self.note_max_priority_lineedit = QtWidgets.QLineEdit()
        note_priority_layout.addWidget(self.note_min_priority_lineedit)
        note_priority_layout.addWidget(QtWidgets.QLabel(" - "))
        note_priority_layout.addWidget(self.note_max_priority_lineedit)
        form_layout.addRow("Note priority range:", note_priority_layout)

        form_layout.addItem(QtWidgets.QSpacerItem(0, 20))

        self.category_name_lineedit = QtWidgets.QLineEdit()
        form_layout.addRow("Category name:", self.category_name_lineedit)
        
        self.category_description_lineedit = QtWidgets.QLineEdit()
        form_layout.addRow("Category description:", self.category_description_lineedit)

        self.tag_name_lineedit = QtWidgets.QLineEdit()
        form_layout.addRow("Tag name:", self.tag_name_lineedit)
        
        self.tag_description_lineedit = QtWidgets.QLineEdit()
        form_layout.addRow("Tag description:", self.tag_description_lineedit)

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
            self.close()


    def cancel_callback(self):
        self.close()


    def edit_note(self):
        pass
        # get note data
        # call controller


    def save_note(self):
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
    dialog = FiltersDialog(objectName="dialog")
    dialog.show()
    sys.exit(app.exec())

