import sys

from PySide6 import QtWidgets, QtCore, QtGui


class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(SettingsDialog, self).__init__(*args, **kwargs)
        self.setWindowTitle("Select GUI library")

        dialog_layout = QtWidgets.QVBoxLayout()

        # Name
        self.info_label = QtWidgets.QLabel("Saving with different than current library will restart the application", objectName="red_label")
        dialog_layout.addWidget(self.info_label)
        

        # Radio buttons
        self.radio_buttons = [QtWidgets.QRadioButton("PySide", objectName="black_button"),
                              QtWidgets.QRadioButton("Tkinter", objectName="black_button"),
                              QtWidgets.QRadioButton("Kivy", objectName="black_button")]

        for rb in self.radio_buttons:
            dialog_layout.addWidget(rb)
        self.radio_buttons[0].setChecked(True)
        

        # Buttons
        btnBox = QtWidgets.QDialogButtonBox()
        btnBox.setStandardButtons(QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel)
        btnBox.accepted.connect(self.ok_callback)
        btnBox.rejected.connect(self.cancel_callback)
        
        dialog_layout.addWidget(btnBox)
        
        self.setLayout(dialog_layout)
        dialog_layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)



    def ok_callback(self):
        index = 0
        for i, rb in enumerate(self.radio_buttons):
            if rb.isChecked():
                index = i
                break

        self.data_dict = {
            "library" : index,
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
    dialog = SettingsDialog(objectName="dialog")
    dialog.resize(500, 500)
    dialog.show()
    sys.exit(app.exec())

