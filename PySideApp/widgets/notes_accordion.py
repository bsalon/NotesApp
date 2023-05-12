import sys

from PySide6 import QtWidgets, QtGui, QtCore


# https://stackoverflow.com/questions/32476006/how-to-make-an-expandable-collapsable-section-widget-in-qt
class NotesAccordion(QtWidgets.QDialog):
    """
    Accordion widget displaying notes

    Methods are used for CRUD operations
    """

    selection_changed = QtCore.Signal()
    
    def __init__(self, notes, *args, **kwargs):
        super(NotesAccordion, self).__init__(*args, **kwargs)

        self.tree = QtWidgets.QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setObjectName("collapsable_tree")
        
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tree)
        self.setLayout(layout)
        self.tree.setIndentation(0)

        self.replace_sections(notes)


    def replace_sections(self, notes):
        self.tree.clear()
        self.notes = notes
        
        self.sections = []
        for note in self.notes:
            section = self.create_note_section(note)
            self.sections.append(section)
        self.add_sections()


    def add_sections(self):
        self.widgets = []
        for (index, (name, date, widget)) in enumerate(self.sections):
            item, tree_widget = self.add_expand_widget(name, date)
            section = self.add_widget(item, widget)
            item.addChild(section)
            self.widgets.append(tree_widget)


    def create_note_section(self, note):
        widget = QtWidgets.QFrame(self.tree, objectName="collapsable_widget_frame")
        layout = QtWidgets.QVBoxLayout(widget)

        text_label = QtWidgets.QLabel(f"<b>Text:</b> {note.text}", objectName="black_label")
        text_label.setWordWrap(True)
        priority_label = QtWidgets.QLabel(f"<b>Priority:</b> {note.priority}", objectName="black_label")
        category_label = QtWidgets.QLabel(f"<b>Category:</b> {note.category.name}", objectName="black_label")
        tags_string = " ".join(note.tags)
        tags_label = QtWidgets.QLabel(f"<b>Tags:</b> {tags_string}", objectName="black_label")
        tags_label.setWordWrap(True)

        layout.addWidget(text_label)
        layout.addWidget(priority_label)
        layout.addWidget(category_label)
        layout.addWidget(tags_label)

        return note.name, note.time, widget


    def add_expand_widget(self, note_name, note_date):
        """creates a QTreeWidgetItem containing a widget 
        to expand or collapse its section
        """
        item = QtWidgets.QTreeWidgetItem()
        collapsable_widget = CollapsableExpandWidget(item, note_name, note_date, objectName="collapsable_widget")
        collapsable_widget.checkbox.stateChanged.connect(self.emit_signal)

        self.tree.addTopLevelItem(item)
        self.tree.setItemWidget(item, 0, collapsable_widget)
        return item, collapsable_widget


    def add_widget(self, button, widget):
        """creates a QWidgetItem containing the widget,
        as child of the button-QWidgetItem
        """
        section = QtWidgets.QTreeWidgetItem(button)
        section.setDisabled(True)
        self.tree.setItemWidget(section, 0, widget)
        return section


    @QtCore.Slot()
    def emit_signal(self):
        self.selection_changed.emit()


    def get_selected_notes(self):
        selected_notes = []
        for (index, widget) in enumerate(self.widgets):
            if widget.checkbox.isChecked():
                selected_notes.append(self.notes[index])
        return selected_notes



class CollapsableExpandWidget(QtWidgets.QWidget):
    def __init__(self, section, name, date, *args, **kwargs):
        super(CollapsableExpandWidget, self).__init__(*args, **kwargs) # text

        self.note_name_label = QtWidgets.QLabel(name, objectName="black_label")
        self.note_name_label.setWordWrap(True)
        note_date_label = QtWidgets.QLabel(date.strftime("%d/%m/%Y %H:%M"), objectName="black_label")
        self.checkbox = QtWidgets.QCheckBox()
        self.checkbox.stateChanged.connect(self.toggle_check_state)

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.note_name_label,  0, 0, alignment=QtCore.Qt.AlignLeft)
        layout.addWidget(note_date_label, 0, 1, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.checkbox, 0, 2, alignment=QtCore.Qt.AlignRight)

        for r in range(3):
            layout.setColumnStretch(r, 1)

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


