import sys

from PySide6 import QtWidgets, QtCore, QtGui

from PySideApp.dialogs import reg_exp_validator


class FilterDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(FilterDialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Fast filter dialog")
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        dialog_layout = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()
        
        # Filter
        self.filter_name_lineedit = QtWidgets.QLineEdit()
        form_layout.addRow("Filter name:", self.filter_name_lineedit)

        order_validator = QtGui.QIntValidator(-1, 1000)
        self.filter_order_lineedit = QtWidgets.QLineEdit()
        self.filter_order_lineedit.setValidator(order_validator)
        form_layout.addRow("Filter order:", self.filter_order_lineedit)
        
        form_layout.addItem(QtWidgets.QSpacerItem(0, 20))
        
        # Note name
        self.note_name_lineedit = QtWidgets.QLineEdit()
        form_layout.addRow("Note name contains:", self.note_name_lineedit)
        
        # Note time
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
        
        # Note text
        self.note_text_lineedit = QtWidgets.QLineEdit()
        form_layout.addRow("Note text contains:", self.note_text_lineedit)

        # Note priority
        priority_validator = QtGui.QIntValidator(0, 100)

        note_priority_layout = QtWidgets.QHBoxLayout()
        note_priority_layout.setContentsMargins(0, 0, 0, 0)
        note_priority_layout.setAlignment(QtCore.Qt.AlignTop)
        
        self.note_min_priority_lineedit = QtWidgets.QLineEdit()
        self.note_min_priority_lineedit.setValidator(priority_validator)
        
        self.note_max_priority_lineedit = QtWidgets.QLineEdit()
        self.note_max_priority_lineedit.setValidator(priority_validator)
        
        note_priority_layout.addWidget(self.note_min_priority_lineedit)
        note_priority_layout.addWidget(QtWidgets.QLabel(" - "))
        note_priority_layout.addWidget(self.note_max_priority_lineedit)
        form_layout.addRow("Note priority range:", note_priority_layout)

        form_layout.addItem(QtWidgets.QSpacerItem(0, 20))

        # Category name
        self.category_name_lineedit = QtWidgets.QLineEdit()
        form_layout.addRow("Category name contains:", self.category_name_lineedit)
        
        # Category description
        self.category_description_lineedit = QtWidgets.QLineEdit()
        form_layout.addRow("Category description contains:", self.category_description_lineedit)

        # Tag name
        self.tag_name_lineedit = QtWidgets.QLineEdit()
        form_layout.addRow("Tag name contains:", self.tag_name_lineedit)
        
        # Tag description
        self.tag_description_lineedit = QtWidgets.QLineEdit()
        form_layout.addRow("Tag description contains:", self.tag_description_lineedit)

        # Buttons
        btnBox = QtWidgets.QDialogButtonBox()
        btnBox.setStandardButtons(QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel)
        btnBox.accepted.connect(self.ok_callback)
        btnBox.rejected.connect(self.cancel_callback)
        
        form_layout.addItem(QtWidgets.QSpacerItem(0, 20))
        
        dialog_layout.addLayout(form_layout)
        dialog_layout.addWidget(btnBox)
        self.setLayout(dialog_layout)



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
        if not self._validate():
            return
        self.data_dict = {
            "name": self.filter_name_lineedit.text(),
            "order": self._get_order(),
            "note_name": self.note_name_lineedit.text(),
            "note_min_priority": self._get_min_priority(),
            "note_max_priority": self._get_max_priority(),
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


    def _validate(self):
        valid = True
        valid &= self._validate_field(self.filter_name_lineedit)
        valid &= self._validate_field(self.filter_order_lineedit)
        return valid


    def _validate_field(self, field):
        if field.text() == "" or field.text().isspace():
            field.setStyleSheet("background: #ff7f7f")
            return False
        field.setStyleSheet("background: white")
        return True


    def _get_min_priority(self):
        priority_text = self.note_min_priority_lineedit.text().replace(" ", "")
        if priority_text == "":
            return 0
        num = int(priority_text)
        if num > 100:
            return 100
        if num < 0:
            return 0
        return num


    def _get_max_priority(self):
        priority_text = self.note_max_priority_lineedit.text().replace(" ", "")
        if priority_text == "":
            return 100
        num = int(priority_text)
        if num > 100:
            return 100
        if num < 0:
            return 0
        return num


    def _get_order(self):
        order_text = self.filter_order_lineedit.text().replace(" ","")
        if order_text[0] == "-":
            return -1
        num = int(order_text)
        return 1000 if num > 1000 else num




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

