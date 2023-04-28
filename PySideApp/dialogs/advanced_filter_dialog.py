import sys

from PySide6 import QtWidgets, QtCore, QtGui


class AdvancedFilterDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(AdvancedFilterDialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Advanced filter dialog")
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        dialog_layout = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()
        
        self.note_name_lineedit = QtWidgets.QLineEdit()
        note_name_label = QtWidgets.QLabel("Note name contains:", objectName="black_label")
        form_layout.addRow(note_name_label, self.note_name_lineedit)
        
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
        note_datetime_layout.addWidget(QtWidgets.QLabel(" - ", objectName="black_label"))
        note_datetime_layout.addWidget(self.note_to_datetime_edit, stretch=1)
        datetime_range_label = QtWidgets.QLabel("Note date and time range:", objectName="black_label")
        form_layout.addRow(datetime_range_label, note_datetime_layout)
        
        self.note_text_lineedit = QtWidgets.QLineEdit()
        note_text_label = QtWidgets.QLabel("Note text contains:", objectName="black_label")
        form_layout.addRow(note_text_label, self.note_text_lineedit)

        # Note priority
        note_priority_layout = QtWidgets.QHBoxLayout()
        note_priority_layout.setContentsMargins(0, 0, 0, 0)
        note_priority_layout.setAlignment(QtCore.Qt.AlignTop)
        
        self.note_min_priority_spinbox = QtWidgets.QSpinBox(minimum=0, maximum=100, value=0)
        self.note_max_priority_spinbox = QtWidgets.QSpinBox(minimum=0, maximum=100, value=100)
        
        note_priority_layout.addWidget(self.note_min_priority_spinbox)
        note_priority_layout.addWidget(QtWidgets.QLabel(" - ", objectName="black_label", alignment=QtGui.Qt.AlignCenter))
        note_priority_layout.addWidget(self.note_max_priority_spinbox)
        note_priority_range_label = QtWidgets.QLabel("Note priority range:", objectName="black_label")
        form_layout.addRow(note_priority_range_label, note_priority_layout)

        form_layout.addItem(QtWidgets.QSpacerItem(0, 20))

        self.category_name_lineedit = QtWidgets.QLineEdit()
        category_name_label = QtWidgets.QLabel("Category name contains:", objectName="black_label")
        form_layout.addRow(category_name_label, self.category_name_lineedit)
        
        self.category_description_lineedit = QtWidgets.QLineEdit()
        category_description_label = QtWidgets.QLabel("Category description contains:", objectName="black_label")
        form_layout.addRow(category_description_label, self.category_description_lineedit)

        self.tag_name_lineedit = QtWidgets.QLineEdit()
        tag_name_label = QtWidgets.QLabel("Tag name contains:", objectName="black_label")
        form_layout.addRow(tag_name_label, self.tag_name_lineedit)
        
        self.tag_description_lineedit = QtWidgets.QLineEdit()
        tag_description_label = QtWidgets.QLabel("Tag description contains:", objectName="black_label")
        form_layout.addRow(tag_description_label, self.tag_description_lineedit)

        btnBox = QtWidgets.QDialogButtonBox()
        btnBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        btnBox.accepted.connect(self.ok_callback)
        btnBox.rejected.connect(self.cancel_callback)
        
        form_layout.addItem(QtWidgets.QSpacerItem(0, 20))
        
        dialog_layout.addLayout(form_layout)
        dialog_layout.addWidget(btnBox)
        self.setLayout(dialog_layout)
        dialog_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)


    def ok_callback(self):
        self.data_dict = {
            "note_name" : self.note_name_lineedit.text(),
            "note_from_date" : self.note_from_datetime_edit.dateTime(),
            "note_to_date" : self.note_to_datetime_edit.dateTime(),
            "note_min_priority" : self.note_min_priority_spinbox.value(),
            "note_max_priority" : self.note_max_priority_spinbox.value(),
            "note_text" : self.note_text_lineedit.text(),
            "category_name" : self.category_name_lineedit.text(),
            "category_description" : self.category_description_lineedit.text(),
            "tag_name" : self.tag_name_lineedit.text(),
            "tag_description" : self.tag_description_lineedit.text()
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
    dialog = AdvancedFilterDialog(objectName="dialog")
    dialog.show()
    sys.exit(app.exec())

