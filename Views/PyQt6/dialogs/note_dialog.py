import sys

from PySide6 import QtWidgets, QtCore, QtGui


class NoteDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(NoteDialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Note dialog window")
        
        dialog_layout = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()
        
        self.name_lineedit = QtWidgets.QLineEdit()
        form_layout.addRow("Name:", self.name_lineedit)
        
        self.datetime_lineedit = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime())
        self.datetime_lineedit.setDisplayFormat("dd:MM:yyyy hh:mm")
        self.datetime_lineedit.setToolTip("Rewrite date and time or use ticks")
        form_layout.addRow("Date and time:", self.datetime_lineedit)
        
        self.description_lineedit = QtWidgets.QLineEdit()
        form_layout.addRow("Description:", self.description_lineedit)
        
        form_layout.addItem(QtWidgets.QSpacerItem(0, 20))

        priority_layout = QtWidgets.QHBoxLayout()
        self.yes_radiobutton = QtWidgets.QRadioButton("Yes")
        self.no_radiobutton = QtWidgets.QRadioButton("No")
        priority_layout.addWidget(self.yes_radiobutton)
        priority_layout.addWidget(self.no_radiobutton)
        priority_layout.addStretch()
        form_layout.addRow("Assign priority:", priority_layout)
        
        self.priority_slider_label = QtWidgets.QLabel("0")
        self.priority_slider_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignCenter)
        self.priority_slider_label.setMinimumWidth(80)
        priority_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        priority_slider.setRange(0, 100)
        priority_slider.setSingleStep(1)
        priority_slider.valueChanged.connect(self.update_slider_label)
        priority_slider_layout = QtWidgets.QHBoxLayout()
        priority_slider_layout.setContentsMargins(0, 8, 0, 0)
        priority_slider_layout.setAlignment(QtCore.Qt.AlignTop)
        priority_slider_layout.addWidget(priority_slider)
        priority_slider_layout.addWidget(self.priority_slider_label)
        form_layout.addRow("Priority value:", priority_slider_layout)

        form_layout.addItem(QtWidgets.QSpacerItem(0, 20))

        self.categories_listwidget = QtWidgets.QListWidget()
        self.categories_listwidget.setMaximumHeight(60)
        self.categories_listwidget.setToolTip("Select one category from the list")
        categories = ["default category", "new category", "old category", "shop me"] # FIXME
        self.fill_categories_listwidget(categories)
        form_layout.addRow("Category:", self.categories_listwidget)

        self.tags_listwidget = QtWidgets.QListWidget()
        self.tags_listwidget.setMaximumHeight(60)
        self.tags_listwidget.setToolTip("Select zero or more tags from the list")
        tags = ["default tag", "new tag", "old tag", "shop me"] # FIXME
        self.fill_tags_listwidget(tags)
        form_layout.addRow("Tags:", self.tags_listwidget)

        btnBox = QtWidgets.QDialogButtonBox()
        btnBox.setStandardButtons(QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel)
        btnBox.accepted.connect(self.ok_callback)
        btnBox.rejected.connect(self.cancel_callback)
        
        form_layout.addItem(QtWidgets.QSpacerItem(0, 10))
        
        dialog_layout.addLayout(form_layout)
        dialog_layout.addWidget(btnBox)
        self.setLayout(dialog_layout)


    def fill_categories_listwidget(self, categories):
        for category in categories:
            category_item = QtWidgets.QListWidgetItem(self.categories_listwidget)
            self.categories_listwidget.addItem(category_item)
            self.categories_listwidget.setItemWidget(category_item, QtWidgets.QRadioButton(category))


    def fill_tags_listwidget(self, tags):
        for tag in tags:
            tag_item = QtWidgets.QListWidgetItem(tag)
            tag_item.setCheckState(QtCore.Qt.Unchecked)
            self.tags_listwidget.addItem(tag_item)


    def ok_callback(self): # FIXME
        print("ACCEPTED")
        if "action" == "create":
            pass
        elif "action" == "edit":
            pass
        else:
            pass

        name = self.name_lineedit.text()
        date_time = self.datetime_lineedit.dateTime()
        description = self.description_lineedit.text()
        priority = self.priority_slider_label.text()
        category = self.categories_listwidget.selectedItems()[0].text()
        tags = [self.tags_listwidget.item(index).text() for index in range(self.tags_listwidget.count()) if self.tags_listwidget.item(index).checkState() == QtCore.Qt.Checked]
        print(f"Name={name} Date={date_time} Description={description} Priority={priority} Category={category} Tags={tags}")
        # self.close()


    def cancel_callback(self):
        self.close()


    @QtCore.Slot()
    def update_slider_label(self, value):
        self.priority_slider_label.setText(str(value))


    def edit_note(self): # FIXME
        pass
        # get note data
        # call controller


    def save_note(self): # FIXME
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
    dialog = NoteDialog(objectName="dialog")
    dialog.resize(500, 500)
    dialog.show()
    sys.exit(app.exec())

