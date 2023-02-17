import sys


from PySide6 import QtWidgets, QtCore, QtGui


class Dialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QDialog's Top-Level Layout Example")
        
        dlgLayout = QtWidgets.QVBoxLayout()
        
        # Create a form layout and add widgets
        formLayout = QtWidgets.QFormLayout()
        
        name_line_edit = QtWidgets.QLineEdit()
        formLayout.addRow("Name:", name_line_edit)
        
        dateTimeEdit = QtWidgets.QDateTimeEdit(QtCore.QDateTime.currentDateTime(), calendarPopup=True)
        dateTimeEdit.setDisplayFormat("dd:MM:yyyy hh:mm")
        formLayout.addRow("Date:", dateTimeEdit)
        
        formLayout.addRow("Description:", QtWidgets.QLineEdit())
        
        # priority
        priority_layout = QtWidgets.QHBoxLayout()
        priority_layout.addWidget(QtWidgets.QRadioButton("Yes"))
        priority_layout.addWidget(QtWidgets.QRadioButton("No"))

        formLayout.addRow("Assign priority:", priority_layout)
        
        self.slider_label = QtWidgets.QLabel("0")
        self.slider_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter | QtCore.Qt.AlignmentFlag.AlignCenter)
        self.slider_label.setMinimumWidth(80)

        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider.setRange(0, 100)
        slider.setSingleStep(1)
        slider.valueChanged.connect(self.update_slider_label)
        
        slider_layout = QtWidgets.QHBoxLayout()
        slider_layout.addWidget(slider)
        slider_layout.addWidget(self.slider_label)

        formLayout.addRow("Priority value:", slider_layout)

        # category
        


        # tag
        tags_names = ["default tag", "new tag", "old tag", "shop me"]
        tags_combo_box = QtWidgets.QComboBox()
        for tag_name in tags_names:
            tags_combo_box.addItem(tag_name)
            item = tags_combo_box.model().item(tags_combo_box.count() - 1, 0)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)
        formLayout.addRow("Tags:", tags_combo_box)


        # Add a button box
        btnBox = QtWidgets.QDialogButtonBox()
        btnBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel
        )
        
        # Set the layout on the dialog
        dlgLayout.addLayout(formLayout)
        dlgLayout.addWidget(btnBox)
        
        self.setLayout(dlgLayout)


    @QtCore.Slot()
    def update_slider_label(self, value):
        self.slider_label.setText(str(value))


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
    dlg = Dialog()
    dlg.show()
    sys.exit(app.exec())

