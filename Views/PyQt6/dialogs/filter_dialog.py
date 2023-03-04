import sys

from PySide6 import QtWidgets, QtCore, QtGui

from dialogs import reg_exp_validator


class FilterDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(FilterDialog, self).__init__(*args, **kwargs)
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
        
        self.note_text_lineedit = QtWidgets.QLineEdit()
        form_layout.addRow("Note text:", self.note_text_lineedit)

        note_priority_layout = QtWidgets.QHBoxLayout()
        note_priority_layout.setContentsMargins(0, 0, 0, 0)
        note_priority_layout.setAlignment(QtCore.Qt.AlignTop)
        self.note_min_priority_lineedit = QtWidgets.QLineEdit()
        min_priority_validator = reg_exp_validator.RegExpValidator(r"1?\d{1,2}", self)
        min_priority_validator.validationChanged.connect(self.handle_min_priority_validation)
        self.note_min_priority_lineedit.setValidator(min_priority_validator)
        self.note_max_priority_lineedit = QtWidgets.QLineEdit()
        max_priority_validator = reg_exp_validator.RegExpValidator(r"1?\d{1,2}", self)
        max_priority_validator.validationChanged.connect(self.handle_max_priority_validation)
        self.note_max_priority_lineedit.setValidator(max_priority_validator)
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


    def handle_min_priority_validation(self, state):
        color = "lime" if state == QtGui.QValidator.Acceptable else "red"
        self.note_min_priority_lineedit.setStyleSheet("border: 3px solid %s" % color)
        QtCore.QTimer.singleShot(1000, lambda: self.note_min_priority_lineedit.setStyleSheet(''))
    

    def handle_max_priority_validation(self, state):
        color = "lime" if state == QtGui.QValidator.Acceptable else "red"
        self.note_max_priority_lineedit.setStyleSheet("border: 3px solid %s" % color)
        QtCore.QTimer.singleShot(1000, lambda: self.note_max_priority_lineedit.setStyleSheet(''))



    def fill_dialog(self, fast_filter): 
        self.filter_name_lineedit.setText(fast_filter.name)
        self.filter_order_lineedit.setText(str(fast_filter.order))
        self.note_name_lineedit.setText(fast_filter.note_name)
        self.note_min_priority_lineedit.setText(str(fast_filter.note_min_priority))
        self.note_max_priority_lineedit.setText(str(fast_filter.note_max_priority))
        self.note_from_datetime_edit.setDate(fast_filter.note_min_time)
        self.note_to_datetime_edit.setDate(fast_filter.note_max_time)
        self.note_text_lineedit.setText(fast_filter.note_text)
        self.tag_name_lineedit.setText(fast_filter.tag_name)
        self.tag_description_lineedit.setText(fast_filter.tag_description)
        self.category_name_lineedit.setText(fast_filter.category_name)
        self.category_description_lineedit.setText(fast_filter.category_description)


    def ok_callback(self):
        self.data_dict = {
            "name": self.filter_name_lineedit.text(),
            "order": self.filter_order_lineedit.text(),
            "note_name": self.note_name_lineedit.text(),
            "note_min_priority": self.note_min_priority_lineedit.text(),
            "note_max_priority": self.note_max_priority_lineedit.text(),
            "note_from_time": self.note_from_datetime_edit.dateTime(),
            "note_to_time": self.note_to_datetime_edit.dateTime(),
            "note_text": self.note_text_lineedit.text(),
            "tag_name": self.tag_name_lineedit.text(),
            "tag_description": self.tag_description_lineedit.text(),
            "category_name": self.category_name_lineedit.text(),
            "category_description": self.category_description_lineedit.text()
        }
        self.accept()
        self.close()


    def cancel_callback(self):
        self.close()




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet('''
QDialog {
    background: #d7eb5a;
}
    ''')
    dialog = FilterDialog(objectName="dialog")
    dialog.show()
    sys.exit(app.exec())

