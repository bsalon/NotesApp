import sys

from PySide6 import QtWidgets, QtCore, QtGui


class NoteDialog(QtWidgets.QDialog):
    def __init__(self, categories, tags, *args, **kwargs):
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
        
        self.text_lineedit = QtWidgets.QLineEdit()
        form_layout.addRow("Text:", self.text_lineedit)
        
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
        self.priority_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.priority_slider.setRange(0, 100)
        self.priority_slider.setSingleStep(1)
        self.priority_slider.valueChanged.connect(self.update_slider_label)
        priority_slider_layout = QtWidgets.QHBoxLayout()
        priority_slider_layout.setContentsMargins(0, 8, 0, 0)
        priority_slider_layout.setAlignment(QtCore.Qt.AlignTop)
        priority_slider_layout.addWidget(self.priority_slider)
        priority_slider_layout.addWidget(self.priority_slider_label)
        form_layout.addRow("Priority value:", priority_slider_layout)

        form_layout.addItem(QtWidgets.QSpacerItem(0, 20))

        self.categories_listwidget = QtWidgets.QListWidget()
        self.categories_listwidget.setMaximumHeight(60)
        self.categories_listwidget.setToolTip("Select one category from the list")
        self.fill_categories_listwidget(categories) # from the constructor
        form_layout.addRow("Category:", self.categories_listwidget)

        self.tags_listwidget = QtWidgets.QListWidget()
        self.tags_listwidget.setMaximumHeight(60)
        self.tags_listwidget.setToolTip("Select zero or more tags from the list")
        self.fill_tags_listwidget(tags) # from the constructor
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


    def fill_dialog(self, note):
        self.name_lineedit.setText(note.name)
        self.datetime_lineedit.setDateTime(note.time)
        self.text_lineedit.setText(note.text)
        self.yes_radiobutton.setChecked(True)
        self.priority_slider.setValue(note.priority)
        self.select_category(note.category.name)
        self.select_tags(note.tags)


    def select_category(self, category):
        for i in range(self.categories_listwidget.count()):
            category_item = self.categories_listwidget.item(i)
            category_item_widget = self.categories_listwidget.itemWidget(category_item)
            if category_item_widget.text() == category:
                category_item_widget.setChecked(True)


    def select_tags(self, tags):
        for i in range(self.tags_listwidget.count()):
            tag_item = self.tags_listwidget.item(i)
            if tag_item.text() in tags:
                tag_item.setCheckState(QtCore.Qt.Checked)


    def ok_callback(self):
        self.data_dict = {
            "name" : self.name_lineedit.text(),
            "time" : self.datetime_lineedit.dateTime(),
            "text" : self.text_lineedit.text(),
            "priority" : self.priority_slider.value(),
            "category" : self.get_selected_category_name(),
            "tags" : self.get_selected_tags_names()
        }
        self.accept()
        self.close()


    def cancel_callback(self):
        self.close()


    def get_selected_category_name(self):
        for i in range(self.categories_listwidget.count()):
            category_item = self.categories_listwidget.item(i)
            category_item_widget = self.categories_listwidget.itemWidget(category_item)
            if category_item_widget.isChecked():
                return category_item_widget.text()


    def get_selected_tags_names(self):
        return [self.tags_listwidget.item(index).text() for index in range(self.tags_listwidget.count()) if self.tags_listwidget.item(index).checkState() == QtCore.Qt.Checked]


    @QtCore.Slot()
    def update_slider_label(self, value):
        self.priority_slider_label.setText(str(value))


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

