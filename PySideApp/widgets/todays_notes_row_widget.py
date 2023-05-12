import sys

from PySide6 import QtCore, QtWidgets, QtGui


class TodaysNotesRowWidget(QtWidgets.QWidget):
    """
    Note name and note time for todays notes pane
    """

    def __init__(self, note_time, note_name, parent=None):
        super(TodaysNotesRowWidget, self).__init__(parent, objectName="panel_row")

        self.note_name = note_name

        layout = QtWidgets.QVBoxLayout(self)

        note_time_label = QtWidgets.QLabel(note_time, objectName="panel_time_header")
        note_time_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(note_time_label)

        note_name_text = QtWidgets.QTextEdit(note_name, objectName="panel_note_name")
        
        # calculate the taken space -- based on the text -- to adjust the size
        text_rect = note_name_text.fontMetrics().boundingRect(note_name_text.toPlainText())
        text_rect_size = text_rect.width() * text_rect.height()
        size_hint = note_name_text.minimumSizeHint()

        # DO SOMETHING WITH MARGINS?? I don't know now
        # print("width")
        # print(f"{text_rect.width()} -> {size_hint.width()}")
        # print("height")
        # print(f"{text_rect.height()} -> {size_hint.height()}")
        # print("")
        
        adjusted_height = text_rect_size // size_hint.width()

        # size = text_W x text_H
        #
        # hint_W / text_W = coefficient
        #
        # size / hint_W = new_hint_H 

        note_name_text.setMinimumSize(QtCore.QSize(size_hint.width(), adjusted_height + 8))

        note_name_text.setAlignment(QtCore.Qt.AlignCenter)
        note_name_text.setReadOnly(True)
        note_name_text.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        note_name_text.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        note_name_text.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        note_name_text.setWordWrapMode(QtGui.QTextOption.WordWrap)
        layout.addWidget(note_name_text)
        




if __name__ == "__main__":
    app = QtWidgets.QApplication()
    stylesheet="style.qss"
    with open(stylesheet, "r") as f:
        app.setStyleSheet(f.read())

    # Create the list
    mylist = QtWidgets.QListWidget()

    # Add to list a new item (item is simply an entry in your list)
    item = QtWidgets.QListWidgetItem(mylist)
    mylist.addItem(item)

    # Instanciate a custom widget
    row = TodaysNotesRowWidget("23:00", "note with a name or a title - as you wish")
    item.setSizeHint(row.minimumSizeHint())

    # Associate the custom widget to the list entry
    mylist.setItemWidget(item, row)
    
    mylist.show()

    sys.exit(app.exec())
