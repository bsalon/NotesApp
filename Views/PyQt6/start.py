import sys
import random

import loading_bar
import time_widget
import todays_notes_row_widget

from PySide6 import QtCore, QtWidgets, QtGui



class MainWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 15 rows : 8 columns
        self.layout = QtWidgets.QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.toolbar_container_widget = QtWidgets.QWidget(objectName="toolbar_container")
        self.toolbar_layout = QtWidgets.QGridLayout(self.toolbar_container_widget)
        self.__init_toolbar_layout()
        self.layout.addWidget(self.toolbar_container_widget, 0, 0, 1, 8)
        
        self.todays_notes_container_widget = QtWidgets.QWidget(objectName="todays_notes_container")
        self.todays_notes_layout = QtWidgets.QGridLayout(self.todays_notes_container_widget)
        self.__init_todays_notes_layout()
        self.layout.addWidget(self.todays_notes_container_widget, 1, 0, 14, 1)
        
        self.tabs_content_container_widget = QtWidgets.QWidget(objectName="tabs_content_container")
        self.tabs_content_layout = QtWidgets.QGridLayout(self.tabs_content_container_widget)
        self.__init_tabs_content_layout()
        self.layout.addWidget(self.tabs_content_container_widget, 1, 1, 14, 7)

        for r in range(15):
            self.layout.setRowStretch(r, 1)
        for c in range(8):
            self.layout.setColumnStretch(c, 1)

        # self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
        # self.button = QtWidgets.QPushButton("Click me!")
        # self.text = QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)
        # self.layout.addWidget(self.text)
        # self.layout.addWidget(self.button)
        # self.button.clicked.connect(self.magic)

        self.setLayout(self.layout)




    @QtCore.Slot()
    def toggle_todays_notes_pane(self):
        if self.todays_notes_pane_visible:
            self.todays_notes_container_widget.hide()
            self.layout.addWidget(self.tabs_content_container_widget, 1, 0, 14, 8)
        else:
            self.layout.addWidget(self.tabs_content_container_widget, 1, 1, 14, 7)
            self.todays_notes_container_widget.show()
        self.todays_notes_pane_visible = not self.todays_notes_pane_visible



    def __init_toolbar_layout(self):
        col = 0

        self.icon = QtGui.QIcon()
        self.icon.addFile("/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/TodaysNotesIcon.png")
        self.today_notes_icon_button = QtWidgets.QToolButton()
        self.today_notes_icon_button.setText("Today's notes")
        self.today_notes_icon_button.setToolButtonStyle(QtGui.Qt.ToolButtonTextUnderIcon)
        self.today_notes_icon_button.setIcon(self.icon)
        self.today_notes_icon_button.setObjectName("today_notes_icon_button")
        self.toolbar_layout.addWidget(self.today_notes_icon_button, 0, col, 0, 4, alignment=QtGui.Qt.AlignCenter)
        self.today_notes_icon_button.clicked.connect(self.toggle_todays_notes_pane)
        self.todays_notes_pane_visible = True
        col += 4

        self.breadcrumb_text_links = [QtWidgets.QLabel("Notes Tab", objectName="text_link"),
                                      QtWidgets.QLabel("Page 1", objectName="text_link")]
        for breadcrumb_text_link in self.breadcrumb_text_links:
            self.toolbar_layout.addWidget(breadcrumb_text_link, 0, col, 0, 1)
            col += 1
            self.toolbar_layout.addWidget(QtWidgets.QLabel(" > "), 0, col, 0, 1)
            col += 1
        self.breadcrumb_text_links.append(QtWidgets.QLabel("", objectName="text_link"))
        self.toolbar_layout.addWidget(self.breadcrumb_text_links[-1], 0, col, 0, 1)
        col += 1

        self.fast_filters_text_links_layout = QtWidgets.QGridLayout()
        self.fast_filters_text_links_layout.addWidget(QtWidgets.QLabel("Use fast filters"), 0, 0, 1, 3)
        col_fast_filters_layout = 0
        self.fast_filters_text_links = [QtWidgets.QLabel("#1"), QtWidgets.QLabel("#2"), QtWidgets.QLabel("#3")]
        for fast_filters_text_link in self.fast_filters_text_links:
            self.fast_filters_text_links_layout.addWidget(fast_filters_text_link, 1, col_fast_filters_layout)
            col_fast_filters_layout += 1
            fast_filters_text_link.setObjectName("text_link")
        self.toolbar_layout.addLayout(self.fast_filters_text_links_layout, 0, col, 0, 4)
        col += 4

        self.time_widget = time_widget.TimeWidget()
        self.toolbar_layout.addWidget(self.time_widget, 0, col, 0, 6)
        col += 6

        self.icon2 = QtGui.QIcon()
        self.icon2.addFile("/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/AddIcon.png")
        self.add_icon_button = QtWidgets.QToolButton()
        self.add_icon_button.setIcon(self.icon2)
        self.add_icon_button.setObjectName("toolbar_icon_button")
        self.toolbar_layout.addWidget(self.add_icon_button, 0, col, 0, 2, alignment=QtGui.Qt.AlignCenter)
        col += 2
        
        self.icon3 = QtGui.QIcon()
        self.icon3.addFile("/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/EditIcon.png")
        self.edit_icon_button = QtWidgets.QToolButton()
        self.edit_icon_button.setIcon(self.icon3)
        self.edit_icon_button.setObjectName("toolbar_icon_button")
        self.toolbar_layout.addWidget(self.edit_icon_button, 0, col, 0, 2, alignment=QtGui.Qt.AlignCenter)
        col += 2
        
        self.icon4 = QtGui.QIcon()
        self.icon4.addFile("/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/DeleteIcon.png")
        self.delete_icon_button = QtWidgets.QToolButton()
        self.delete_icon_button.setIcon(self.icon4)
        self.delete_icon_button.setObjectName("toolbar_icon_button")
        self.toolbar_layout.addWidget(self.delete_icon_button, 0, col, 0, 2, alignment=QtGui.Qt.AlignCenter)
        col += 2

        self.loading_bar = loading_bar.LoadingBarWidget(barObjectName="loading_bar")
        self.toolbar_layout.addWidget(self.loading_bar, 0, col, 0, 5)
        col += 5

        self.icon5 = QtGui.QIcon()
        self.icon5.addFile("/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/SettingsIcon.png")
        
        self.settings_dropdown_button = QtWidgets.QToolButton()
        self.settings_dropdown_button.setIcon(self.icon5)
        self.settings_dropdown_button.setObjectName("toolbar_icon_button")
        self.toolbar_layout.addWidget(self.settings_dropdown_button, 0, col, 0, 2, alignment=QtGui.Qt.AlignRight)
        col += 2

        for c in range(col):
            self.toolbar_layout.setColumnStretch(c, 1)
        for time_col in range(14, 19):
            self.toolbar_layout.setColumnStretch(time_col, 2)


    
    def __init_todays_notes_layout(self):
        self.todays_notes_layout.setContentsMargins(0, 0, 0, 0)
        self.todays_notes_layout.setSpacing(0)
        
        self.todays_notes_header = QtWidgets.QLabel("Today's notes", objectName="todays_notes_header")
        self.todays_notes_header.setAlignment(QtCore.Qt.AlignHCenter)
        self.todays_notes_header.setMargin(12)
        self.todays_notes_layout.addWidget(self.todays_notes_header)

        self.todays_notes_list = QtWidgets.QListWidget(objectName="todays_notes_list")
        for i in range(50):
            item = QtWidgets.QListWidgetItem(self.todays_notes_list)
            self.todays_notes_list.addItem(item)

            row = todays_notes_row_widget.TodaysNotesRowWidget("23:00", "note with a name -- or") # title as you could or possibly would wish if there is an angle in the size")
            item.setSizeHint(row.minimumSizeHint())

            self.todays_notes_list.setItemWidget(item, row)

        self.todays_notes_layout.addWidget(self.todays_notes_list)
        # TODO - set the sizing right -> Data will come from Controller.Index(View(Model))

    

    def __init_tabs_content_layout(self):
        self.tabs = QtWidgets.QTabWidget(objectName="tabs")


        self.test_label = QtWidgets.QLabel("Bad boys bad boys whatchagonnadu when they Bad boys bad boys whatchagonnadu when theyBad boys bad boys whatchagonnadu when theyBad boys bad boys whatchagonnadu when theBad boys bad boys whatchagonnadu when theyBad boys bad boys whatchagonnadu when theyBad boys bad boys whatchagonnadu when theyBad boys bad boys whatchagonnadu when theyBad boys bad boys whatchagonnadu when theyy")
        self.test_label.setWordWrap(True)

        widget = QtWidgets.QWidget(objectName="notes_tab")
        layout = QtWidgets.QGridLayout(widget)
        layout.addWidget(self.test_label)

        self.tabs.addTab(widget, "Notes")
        self.tabs.addTab(QtWidgets.QWidget(), "Categories")
        self.tabs.addTab(QtWidgets.QWidget(), "Tags")
        self.tabs.addTab(QtWidgets.QWidget(), "Fast filters")
        
        self.tabs_content_layout.addWidget(self.tabs)

        # self.tab_content = get_notes_tab_content()
        pass



    def __init_notes_tab(self):
        pass


    def __init_categories_tab(self):
        pass


    def __init_tags_tab(self):
        pass


    def __init_fast_filters_tab(self):
        pass




if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    stylesheet="style.qss"
    with open(stylesheet, "r") as f:
        app.setStyleSheet(f.read())

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
