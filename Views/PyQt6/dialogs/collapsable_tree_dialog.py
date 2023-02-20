import sys

from PySide6 import QtWidgets, QtGui, QtCore


# https://stackoverflow.com/questions/32476006/how-to-make-an-expandable-collapsable-section-widget-in-qt
class CollapsableTreeDialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super(CollapsableTreeDialog, self).__init__(*args, **kwargs)
        self.tree = QtWidgets.QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setObjectName("collapsable_tree")
        
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tree)
        self.setLayout(layout)
        self.tree.setIndentation(0)

        self.sections = []
        self.define_sections(["note1", "note2", "note3"])
        self.add_sections()


    def add_sections(self):
        """adds a collapsable sections for every 
        (title, widget) tuple in self.sections
        """
        for (title, widget) in self.sections:
            button = self.add_button(title)
            section = self.add_widget(button, widget)
            button.addChild(section)


    def define_sections(self, notes):
        for note in notes:
            widget = QtWidgets.QFrame(self.tree, objectName="collapsable_widget_frame")
            layout = QtWidgets.QVBoxLayout(widget)

            description_label = QtWidgets.QLabel(f"<b>Description:</b> {note}")
            priority_label = QtWidgets.QLabel(f"<b>Priority:</b> {note}")
            category_label = QtWidgets.QLabel(f"<b>Category:</b> {note}")
            tags_string = " ".join(notes)
            tags_label = QtWidgets.QLabel(f"<b>Tags:</b> {tags_string}")

            layout.addWidget(description_label)
            layout.addWidget(priority_label)
            layout.addWidget(category_label)
            layout.addWidget(tags_label)

            self.sections.append(("", widget)) # note_name note_title


    def add_button(self, note_name, note_date=""):
        """creates a QTreeWidgetItem containing a widget 
        to expand or collapse its section
        """
        item = QtWidgets.QTreeWidgetItem()
        self.tree.addTopLevelItem(item)
        self.tree.setItemWidget(item, 0, CollapsableExpandWidget(item, objectName="collapsable_widget")) # TODO note_name note_title
        return item


    def add_widget(self, button, widget):
        """creates a QWidgetItem containing the widget,
        as child of the button-QWidgetItem
        """
        section = QtWidgets.QTreeWidgetItem(button)
        section.setDisabled(True)
        self.tree.setItemWidget(section, 0, widget)
        return section



class CollapsableExpandWidget(QtWidgets.QWidget):
    def __init__(self, section, text = "", *args, **kwargs):
        super(CollapsableExpandWidget, self).__init__(*args, **kwargs) # text

        note_name_label = QtWidgets.QLabel("Note name", objectName="collapsable_note_name")
        note_date_label = QtWidgets.QLabel("Note date & time", objectName="collapsable_note_date")
        self.checkbox = QtWidgets.QCheckBox()
        self.checkbox.stateChanged.connect(self.toggle_check_state)

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(note_name_label,  0, 0, alignment=QtCore.Qt.AlignLeft)
        layout.addWidget(note_date_label, 0, 1, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.checkbox, 0, 2, alignment=QtCore.Qt.AlignRight)
        
        self.section = section

    
    def mousePressEvent(self, event):
        """toggle expand/collapse of section by clicking
        """
        if self.section.isExpanded():
            self.section.setExpanded(False)
        else:
            self.section.setExpanded(True)


    @QtCore.Slot()
    def toggle_check_state(self):
        self.setObjectName("collapsable_widget_checked" if self.checkbox.isChecked() else "collapsable_widget")
        self.setStyleSheet('''
        QWidget#collapsable_widget_checked {
            border: 1px solid black;
            background-color: #d7eb5a;
        }''')
    

    # issue explained here - https://stackoverflow.com/questions/7276330/qt-stylesheet-for-custom-widget
    def paintEvent(self, event):
        option = QtWidgets.QStyleOption()
        option.initFrom(self)
        painter = QtGui.QPainter(self)
        style = self.style()
        style.drawPrimitive(QtWidgets.QStyle.PE_Widget, option, painter, self)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet('''
QTreeWidget#collapsable_tree {
    background-color: #f7fade;
}

QWidget#collapsable_widget_frame {
    background-color: #f7fade;
}

QWidget#collapsable_widget {
    background-color: #e9f29b;
    border: 1px solid black;
}

QWidget#collapsable_widget_checked {
    border: 1px solid black;
    background-color: #d7eb5a;
}

    ''')
    window = CollapsableTreeDialog()
    window.show()
    sys.exit(app.exec())


