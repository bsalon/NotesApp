import sys

from PySide6 import QtWidgets, QtCore, QtGui


class NoteDialog(QtWidgets.QDialog):
    def __init__(self, categories, tags, *args, **kwargs):
        """
        Initializes note dialog with all its widgets
        """

        super(NoteDialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Note dialog")

        dialog_layout = QtWidgets.QVBoxLayout()
        form_layout = QtWidgets.QFormLayout()

        # Note name
        self.name_lineedit = QtWidgets.QLineEdit()
        name_label = QtWidgets.QLabel("Name:", objectName="black_label")
        form_layout.addRow(name_label, self.name_lineedit)
        
        # Note date and time
        self.datetime_lineedit = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime())
        self.datetime_lineedit.setDisplayFormat("dd:MM:yyyy hh:mm")
        self.datetime_lineedit.setToolTip("Rewrite date and time or use ticks")
        datetime_label = QtWidgets.QLabel("Date and time:", objectName="black_label")
        form_layout.addRow(datetime_label, self.datetime_lineedit)
        
        # Note text
        self.text_lineedit = QtWidgets.QLineEdit()
        text_label = QtWidgets.QLabel("Text:", objectName="black_label")
        form_layout.addRow(text_label, self.text_lineedit)
        
        form_layout.addItem(QtWidgets.QSpacerItem(0, 20))

        # Note priority radio buttons
        priority_layout = QtWidgets.QHBoxLayout()
        self.yes_radiobutton = QtWidgets.QRadioButton("Yes", objectName="black_button")
        self.yes_radiobutton.setChecked(True)
        self.no_radiobutton = QtWidgets.QRadioButton("No", objectName="black_button")
        self.no_radiobutton.toggled.connect(self.slider_enabling)
        priority_layout.addWidget(self.yes_radiobutton)
        priority_layout.addWidget(self.no_radiobutton)
        priority_layout.addStretch()
        priority_label = QtWidgets.QLabel("Assign priority:", objectName="black_label")
        form_layout.addRow(priority_label, priority_layout)
        
        # Note priority value label and slider
        self.priority_slider_label = QtWidgets.QLabel("0", objectName="black_label")
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
        priority_value_label = QtWidgets.QLabel("Priority value:", objectName="black_label")
        form_layout.addRow(priority_value_label, priority_slider_layout)

        form_layout.addItem(QtWidgets.QSpacerItem(0, 20))

        # Note categories
        self.categories_listwidget = QtWidgets.QListWidget()
        self.categories_listwidget.setMaximumHeight(60)
        self.categories_listwidget.setToolTip("Select one category from the list")
        self.fill_categories_listwidget(categories) # from the constructor
        category_label = QtWidgets.QLabel("Category:", objectName="black_label")
        form_layout.addRow(category_label, self.categories_listwidget)

        # Note tags
        self.tags_listwidget = QtWidgets.QListWidget()
        self.tags_listwidget.setMaximumHeight(60)
        self.tags_listwidget.setToolTip("Select zero or more tags from the list")
        self.fill_tags_listwidget(tags) # from the constructor
        tags_label = QtWidgets.QLabel("Tags:", objectName="black_label")
        form_layout.addRow(tags_label, self.tags_listwidget)

        # Buttons
        btnBox = QtWidgets.QDialogButtonBox()
        btnBox.setStandardButtons(QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel)
        btnBox.button(QtWidgets.QDialogButtonBox.Save).setObjectName("black_pbutton")
        btnBox.button(QtWidgets.QDialogButtonBox.Cancel).setObjectName("black_pbutton")
        btnBox.accepted.connect(self.ok_callback)
        btnBox.rejected.connect(self.cancel_callback)
        
        form_layout.addItem(QtWidgets.QSpacerItem(0, 10))
        
        dialog_layout.addLayout(form_layout)
        dialog_layout.addWidget(btnBox)
        self.setLayout(dialog_layout)
        dialog_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)


    def fill_categories_listwidget(self, categories):
        """
        Fills categories listwidget with all available categories

        :param categories: Available categories
        """

        for category in categories:
            category_item = QtWidgets.QListWidgetItem(self.categories_listwidget)
            self.categories_listwidget.addItem(category_item)
            self.categories_listwidget.setItemWidget(category_item, QtWidgets.QRadioButton(category, objectName="black_button"))

        # Selecting the first available cateogry
        if len(categories) > 0:
            category_item = self.categories_listwidget.item(0)
            category_item_widget = self.categories_listwidget.itemWidget(category_item)
            category_item_widget.setChecked(True)


    def fill_tags_listwidget(self, tags):
        """
        Fills tags listwidget with all available tags

        :param tags: Available tags
        """

        for tag in tags:
            tag_item = QtWidgets.QListWidgetItem(tag)
            tag_item.setCheckState(QtCore.Qt.Unchecked)
            self.tags_listwidget.addItem(tag_item)


    def slider_enabling(self, event):
        """
        Toggle slide visibility

        :param event: Event causing this method
        """

        if event:
            self.priority_slider_label.setText("0")
            self.priority_slider.setValue(0)
            self.priority_slider.hide()
        else:
            self.priority_slider.show()


    def fill_dialog(self, note):
        """
        Fills dialog widgets with note values

        :param note: Note object
        """

        self.name_lineedit.setText(note.name)
        self.datetime_lineedit.setDateTime(note.time)
        self.text_lineedit.setText(note.text)
        self.yes_radiobutton.setChecked(True)
        self.priority_slider.setValue(note.priority)
        self.select_category(note.category.name)
        self.select_tags(note.tags)


    def select_category(self, category):
        """
        Select category in the widget

        :param category: Category to be selected
        """

        for i in range(self.categories_listwidget.count()):
            category_item = self.categories_listwidget.item(i)
            category_item_widget = self.categories_listwidget.itemWidget(category_item)
            if category_item_widget.text() == category:
                category_item_widget.setChecked(True)


    def select_tags(self, tags):
        """
        Select tags in the widget

        :param tags: Tags to be selected
        """

        for i in range(self.tags_listwidget.count()):
            tag_item = self.tags_listwidget.item(i)
            if tag_item.text() in tags:
                tag_item.setCheckState(QtCore.Qt.Checked)


    def get_selected_category_name(self):
        """
        Gets selected category name

        :return: Selected category name
        """

        for i in range(self.categories_listwidget.count()):
            category_item = self.categories_listwidget.item(i)
            category_item_widget = self.categories_listwidget.itemWidget(category_item)
            if category_item_widget.isChecked():
                return category_item_widget.text()


    def get_selected_tags_names(self):
        """
        Gets selected tags names

        :return: Selected tags names
        """

        return [self.tags_listwidget.item(index).text() for index in range(self.tags_listwidget.count()) if self.tags_listwidget.item(index).checkState() == QtCore.Qt.Checked]


    @QtCore.Slot()
    def update_slider_label(self, value):
        """
        Updates slider label

        :param value: New value of the label
        """

        self.priority_slider_label.setText(str(value))


    def ok_callback(self):
        """
        Fills data_dict property with field values and closes the dialog
        """

        if not self._validate():
            return
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
    dialog = NoteDialog(objectName="dialog")
    dialog.resize(500, 500)
    dialog.show()
    sys.exit(app.exec())

