import bisect
import random
import sys

from datetime import datetime

from Controllers import UseCases

import loading_bar
import clickable_label
import common_table_view
import pagination_widget
import searchbar_with_icon
import time_widget
import todays_notes_row_widget
import toggle_switch_button

from dialogs import advanced_filter_dialog, note_dialog, tag_dialog, category_dialog, filter_dialog, collapsable_note_tree_dialog

from PySide6 import QtCore, QtWidgets, QtGui



class MainWindow(QtWidgets.QWidget):
    def __init__(self, use_cases, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.controller = use_cases # TODO RENAME

        # get data from database for tables and accordion
        self.current_note_filter = self.create_default_filter()
        self.grid_page = 1
        self.grid_notes = [note for note in self.controller.get_filtered_notes_paged(self.current_note_filter, page=self.grid_page, size=10)]

        controller_notes = [note for note in self.controller.get_notes()]
        self.table_notes = [(note.name, note.priority, note.time.strftime("%d/%m/%Y %H:%M"), note.text) for note in controller_notes]
        self.today_notes = [(note.time.strftime("%H:%M"), note.name) for note in controller_notes if note.time.date() == datetime.today().date()]
        self.today_notes.sort(key = lambda note: note[0])

        self.table_tags = [(tag.name, tag.description) for tag in self.controller.get_tags()]

        self.table_categories = [(category.name, category.description) for category in self.controller.get_categories()]
        
        self.table_filters = [(note_filter.name, 
                               note_filter.order,
                               note_filter.note_name,
                               note_filter.category_name) for note_filter in self.controller.get_filters()]
        
        # 15 rows : 8 columns
        self.layout = QtWidgets.QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # toolbar layout on top
        self.toolbar_container_widget = QtWidgets.QWidget(objectName="toolbar_container")
        self.toolbar_layout = QtWidgets.QGridLayout(self.toolbar_container_widget)
        self.__init_toolbar_layout()
        self.layout.addWidget(self.toolbar_container_widget, 0, 0, 1, 8)
        
        # todays notes layout
        self.todays_notes_container_widget = QtWidgets.QWidget(objectName="todays_notes_container")
        self.todays_notes_layout = QtWidgets.QGridLayout(self.todays_notes_container_widget)
        self.__init_todays_notes_layout()
        self.layout.addWidget(self.todays_notes_container_widget, 1, 0, 14, 1)
        
        # content layout
        self.tabs_content_container_widget = QtWidgets.QWidget(objectName="tabs_content_container")
        self.tabs_content_layout = QtWidgets.QGridLayout(self.tabs_content_container_widget)
        self.__init_tabs_content_layout()
        self.layout.addWidget(self.tabs_content_container_widget, 1, 1, 14, 7)

        # stretch rows and columns
        for r in range(15):
            self.layout.setRowStretch(r, 1)
        for c in range(8):
            self.layout.setColumnStretch(c, 1)
        self.setLayout(self.layout)



    def __init_toolbar_layout(self):
        col = 0

        # Today's notes icon button
        todays_notes_icon = QtGui.QIcon()
        todays_notes_icon.addFile("/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/TodaysNotesIcon.png")
        self.today_notes_icon_button = QtWidgets.QToolButton()
        self.today_notes_icon_button.setText("Today's notes")
        self.today_notes_icon_button.setToolButtonStyle(QtGui.Qt.ToolButtonTextUnderIcon)
        self.today_notes_icon_button.setIcon(todays_notes_icon)
        self.today_notes_icon_button.setIconSize(QtCore.QSize(28, 28))
        self.today_notes_icon_button.setObjectName("today_notes_icon_button")
        self.toolbar_layout.addWidget(self.today_notes_icon_button, 0, col, 0, 4, alignment=QtGui.Qt.AlignCenter)
        self.today_notes_icon_button.clicked.connect(self.toggle_todays_notes_pane)
        self.todays_notes_pane_visible = True
        col += 4

        # Use fast filter section
        self.toolbar_layout.addWidget(QtWidgets.QLabel("Use fast filters:"), 0, col, 0, 3, alignment=QtGui.Qt.AlignCenter)
        col += 3
        self.fast_filters_text_links = [clickable_label.ClickableQLabel("#1"), clickable_label.ClickableQLabel("#2"), clickable_label.ClickableQLabel("#3")]
        for order, fast_filters_text_link in enumerate(self.fast_filters_text_links):
            self.toolbar_layout.addWidget(fast_filters_text_link, 0, col, 0, 2)
            fast_filters_text_link.clicked.connect(lambda o=order: self.use_fast_filter(o+1))
            col += 2
            fast_filters_text_link.setObjectName("text_link")

        # Time widget
        self.time_widget = time_widget.TimeWidget()
        self.toolbar_layout.addWidget(self.time_widget, 0, col, 0, 6)
        col += 6

        # Add icon button
        add_icon = QtGui.QIcon()
        add_icon.addFile("/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/AddIcon.png")
        self.add_icon_button = QtWidgets.QToolButton()
        self.add_icon_button.setIcon(add_icon)
        self.add_icon_button.setIconSize(QtCore.QSize(28, 28))
        self.add_icon_button.setObjectName("toolbar_icon_button")
        self.add_icon_button.clicked.connect(self.add_item)
        self.toolbar_layout.addWidget(self.add_icon_button, 0, col, 0, 2, alignment=QtGui.Qt.AlignCenter)
        col += 2
        
        # Edit icon button
        self.edit_icon = QtGui.QIcon()
        self.edit_icon.addFile("/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/EditIcon.png")
        self.edit_icon_button = QtWidgets.QToolButton()
        self.edit_icon_button.setIcon(self.edit_icon)
        self.edit_icon_button.setIconSize(QtCore.QSize(28, 28))
        self.edit_icon_button.setObjectName("toolbar_icon_button")
        self.edit_icon_button.setEnabled(False)
        self.edit_icon_button.clicked.connect(self.edit_item)
        self.toolbar_layout.addWidget(self.edit_icon_button, 0, col, 0, 2, alignment=QtGui.Qt.AlignCenter)
        col += 2
        
        # Delete icon button
        self.delete_icon = QtGui.QIcon()
        self.delete_icon.addFile("/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/DeleteIcon.png")
        self.delete_icon_button = QtWidgets.QToolButton()
        self.delete_icon_button.setIcon(self.delete_icon)
        self.delete_icon_button.setIconSize(QtCore.QSize(28, 28))
        self.delete_icon_button.setObjectName("toolbar_icon_button")
        self.delete_icon_button.setEnabled(False)
        self.delete_icon_button.clicked.connect(self.delete_items)
        self.toolbar_layout.addWidget(self.delete_icon_button, 0, col, 0, 2, alignment=QtGui.Qt.AlignCenter)
        col += 2

        # Loading bar
        self.loading_bar = loading_bar.LoadingBarWidget(barObjectName="loading_bar")
        self.toolbar_layout.addWidget(self.loading_bar, 0, col, 0, 5)
        col += 5

        # Settings icon button TODO
        self.settings_icon = QtGui.QIcon()
        self.settings_icon.addFile("/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/SettingsIcon.png")
        self.settings_dropdown_button = QtWidgets.QToolButton()
        self.settings_dropdown_button.setIcon(self.settings_icon)
        self.settings_dropdown_button.setIconSize(QtCore.QSize(28, 28))
        self.settings_dropdown_button.setObjectName("toolbar_icon_button")
        self.toolbar_layout.addWidget(self.settings_dropdown_button, 0, col, 0, 2, alignment=QtGui.Qt.AlignRight)
        col += 2

        # Stretch time widget more than other widgets
        for c in range(col):
            self.toolbar_layout.setColumnStretch(c, 1)
        for time_col in range(14, 19):
            self.toolbar_layout.setColumnStretch(time_col, 2)



    @QtCore.Slot()
    def toggle_todays_notes_pane(self):
        if self.todays_notes_pane_visible:
            self.todays_notes_container_widget.hide()
            self.layout.addWidget(self.tabs_content_container_widget, 1, 0, 14, 8)
        else:
            self.layout.addWidget(self.tabs_content_container_widget, 1, 1, 14, 7)
            self.todays_notes_container_widget.show()
        self.todays_notes_pane_visible = not self.todays_notes_pane_visible



    @QtCore.Slot()
    def use_fast_filter(self, order):
        self.current_note_filter = self.controller.find_filter_by_order(order)
        if self.current_note_filter == None:
            self.current_note_filter = self.create_default_filter()
            self.display_error_message_box(f"Fast filter with order={order} is not available")
        self.use_current_note_filter()



    def __init_todays_notes_layout(self):
        self.todays_notes_layout.setContentsMargins(0, 0, 0, 0)
        self.todays_notes_layout.setSpacing(0)
        
        self.todays_notes_header = QtWidgets.QLabel("Today's notes", objectName="todays_notes_header")
        self.todays_notes_header.setAlignment(QtCore.Qt.AlignHCenter)
        self.todays_notes_header.setMargin(12)
        self.todays_notes_layout.addWidget(self.todays_notes_header)

        self.todays_notes_list = QtWidgets.QListWidget(objectName="todays_notes_list")
        for note in self.today_notes:
            item = QtWidgets.QListWidgetItem(self.todays_notes_list)
            self.todays_notes_list.addItem(item)

            row = todays_notes_row_widget.TodaysNotesRowWidget(*note)
            item.setSizeHint(row.minimumSizeHint())

            self.todays_notes_list.setItemWidget(item, row)

        self.todays_notes_layout.addWidget(self.todays_notes_list)



    # Maybe faster algorithm here could help
    def remove_notes_from_todays_notes(self, notes):
        remove_indices = []
        for i in range(self.todays_notes_list.count()):
            item = self.todays_notes_list.item(i)
            item_widget = self.todays_notes_list.itemWidget(item)
            if item_widget.note_name in notes:
                remove_indices.append(i)

        for i in reversed(sorted(remove_indices)):
            self.todays_notes_list.takeItem(i)
            self.today_notes.pop(i)



    def add_note_to_todays_notes(self, note):
        if note.time.date() == datetime.today().date():
            note_tuple = (note.time.strftime("%H:%M"), note.name)
            bisect.insort_left(self.today_notes, note_tuple)

            new_note_index = self.today_notes.index(note_tuple)

            item = QtWidgets.QListWidgetItem()
            self.todays_notes_list.insertItem(new_note_index, item)
            row = todays_notes_row_widget.TodaysNotesRowWidget(*note_tuple)
            item.setSizeHint(row.minimumSizeHint())
            self.todays_notes_list.setItemWidget(item, row)


    
    def __init_tabs_content_layout(self):
        self.tabs = QtWidgets.QTabWidget(objectName="tabs")

        self.notes_tab_widget = QtWidgets.QWidget(objectName="notes_tab")
        self.__init_notes_tab()
        self.categories_tab_widget = QtWidgets.QWidget(objectName="categories_tab")
        self.__init_categories_tab()
        self.tags_tab_widget = QtWidgets.QWidget(objectName="tags_tab")
        self.__init_tags_tab()
        self.filters_tab_widget = QtWidgets.QWidget(objectName="filters_tab")
        self.__init_filters_tab()

        self.tabs.addTab(self.notes_tab_widget, "Notes")
        self.tabs.addTab(self.categories_tab_widget, "Categories")
        self.tabs.addTab(self.tags_tab_widget, "Tags")
        self.tabs.addTab(self.filters_tab_widget, "Fast filters")
        
        self.tabs.currentChanged.connect(self.tab_update_buttons_enabling)
        self.tabs_content_layout.addWidget(self.tabs)



    def __init_notes_tab(self):
        self.notes_tab_layout = QtWidgets.QGridLayout(self.notes_tab_widget)

        self.notes_tab_filtering_container_widget = QtWidgets.QWidget(objectName="filtering_container")
        self.notes_tab_filtering_layout = QtWidgets.QGridLayout(self.notes_tab_filtering_container_widget)
        self.notes_tab_filtering_layout.setContentsMargins(0, 0, 0, 0)

        self.notes_tab_searchbar = searchbar_with_icon.SearchBarWithIcon(objectName="search_container")
        
        self.notes_filter_button = QtWidgets.QPushButton("Filter")
        self.notes_filter_button.setToolTip("Resets fast or advanced filter")
        self.notes_filter_button.clicked.connect(lambda: self.__set_basic_text_filtering(
            self.notes_tab_table.filter_proxy_model,
            self.notes_tab_searchbar.searchbar)
        )

        self.notes_advanced_filter_button = QtWidgets.QPushButton("Advanced filter")
        self.notes_advanced_filter_button.clicked.connect(self.notes_advanced_filtering)

        self.notes_toggle_switch_label = QtWidgets.QLabel("Table view")
        self.notes_toggle_switch_button = toggle_switch_button.ToggleSwitchButton()
        self.notes_toggle_switch_button.clicked.connect(self.toggle_notes_view)

        self.notes_tab_filtering_layout.addWidget(self.notes_tab_searchbar, 0, 0, 0, 4)
        self.notes_tab_filtering_layout.addWidget(self.notes_filter_button, 0, 4, 0, 1)
        self.notes_tab_filtering_layout.addWidget(self.notes_advanced_filter_button, 0, 5, 0, 1)
        
        self.notes_toggle_layout = QtWidgets.QHBoxLayout()
        self.notes_toggle_layout.addStretch()
        self.notes_toggle_layout.addWidget(self.notes_toggle_switch_label)
        self.notes_toggle_layout.addWidget(self.notes_toggle_switch_button)
        self.notes_tab_filtering_layout.addLayout(self.notes_toggle_layout, 0, 6, 0, 2)

        self.notes_tab_table = common_table_view.CommonTableView(
            ["Name", "Priority", "Time", "Text"], self.table_notes,
            stretch_column=3,
            sort_column=1,
            order=QtCore.Qt.DescendingOrder
        )
        self.notes_tab_table.selectionModel().selectionChanged.connect(self.table_update_buttons_enabling)

        # accordion
        self.notes_tab_accordion = collapsable_note_tree_dialog.CollapsableNoteTreeDialog(self.grid_notes)
        self.notes_tab_accordion.selection_changed.connect(self.notes_accordion_buttons_enabling)
        self.notes_tab_accordion.hide()
        self.notes_tab_accordion_pagination = pagination_widget.PaginationWidget(10, len(self.table_notes))
        self.notes_tab_accordion_pagination.page_changed.connect(self.change_notes_tab_accordion_page)
        
        self.notes_tab_accordion_pagination.hide()
        self.is_table_view = True

        self.notes_tab_layout.addWidget(self.notes_tab_filtering_container_widget, 0, 0, alignment=QtCore.Qt.AlignTop)
        self.notes_tab_layout.addWidget(self.notes_tab_table, 1, 0)
        self.notes_tab_layout.addWidget(self.notes_tab_accordion, 2, 0)
        self.notes_tab_layout.addWidget(self.notes_tab_accordion_pagination, 3, 0, alignment=QtCore.Qt.AlignCenter)
        


    @QtCore.Slot()
    def notes_advanced_filtering(self):
        dialog = advanced_filter_dialog.AdvancedFilterDialog(objectName="dialog")
        if dialog.exec():
            filters = lambda: None
            filters.note_name = dialog.data_dict["note_name"]
            filters.note_min_priority = int("0" + dialog.data_dict["note_min_priority"])
            filters.note_max_priority = int("0" + dialog.data_dict["note_max_priority"])
            filters.note_min_time = dialog.data_dict["note_from_date"].toPython()
            filters.note_max_time = dialog.data_dict["note_to_date"].toPython()
            filters.note_text = dialog.data_dict["note_text"]
            filters.category_name = dialog.data_dict["category_name"]
            filters.category_description = dialog.data_dict["category_description"]
            filters.tag_name = dialog.data_dict["tag_name"]
            filters.tag_description = dialog.data_dict["tag_description"]
            
            self.current_note_filter = filters
            self.use_current_note_filter()



    def use_current_note_filter(self):
        filtered_notes = self.controller.get_filtered_notes(self.current_note_filter)
        self.table_notes = [(note.name, note.priority, note.time.strftime("%d/%m/%Y %H:%M"), note.text) for note in filtered_notes]

        self.notes_tab_table.replace_data(list(set(self.table_notes)))
        self.update_notes_tab_accordion()



    @QtCore.Slot()
    def toggle_notes_view(self, table_view):
        self.is_table_view = table_view
        if table_view:
            self.notes_tab_accordion.hide()
            self.notes_tab_accordion_pagination.hide()
            selected_rows_count = self.count_selected_rows(self.notes_tab_table)
            self.notes_tab_table.show()
        else:
            self.notes_tab_table.hide()
            selected_rows_count = self.count_selected_notes()
            self.notes_tab_accordion.show()
            self.notes_tab_accordion_pagination.show()
        self.edit_icon_button.setEnabled(selected_rows_count == 1)
        self.delete_icon_button.setEnabled(selected_rows_count >= 1)



    def __init_categories_tab(self):
        self.categories_tab_layout = QtWidgets.QGridLayout(self.categories_tab_widget)
        self.categories_tab_searchbar = searchbar_with_icon.SearchBarWithIcon(objectName="search_container")
        self.categories_filter_button = QtWidgets.QPushButton("Filter")
        self.categories_filter_button.clicked.connect(lambda: self.__set_basic_text_filtering(
            self.categories_tab_table.filter_proxy_model,
            self.categories_tab_searchbar.searchbar)
        )
        self.categories_tab_table = common_table_view.CommonTableView(
            ["Name", "Description"], self.table_categories,
            stretch_column=1
        )
        self.categories_tab_table.selectionModel().selectionChanged.connect(self.table_update_buttons_enabling)
        
        self.categories_tab_layout.setColumnStretch(0, 1)
        self.categories_tab_layout.setColumnStretch(2, 1)
        
        self.categories_tab_layout.addWidget(self.categories_tab_searchbar, 0, 0)
        self.categories_tab_layout.addWidget(self.categories_filter_button, 0, 1)
        self.categories_tab_layout.addWidget(QtWidgets.QWidget(), 0, 2)
        self.categories_tab_layout.addWidget(self.categories_tab_table, 1, 0, 1, 3)



    def __init_tags_tab(self):
        self.tags_tab_layout = QtWidgets.QGridLayout(self.tags_tab_widget)
        self.tags_tab_searchbar = searchbar_with_icon.SearchBarWithIcon(objectName="search_container")
        self.tags_filter_button = QtWidgets.QPushButton("Filter")
        self.tags_filter_button.clicked.connect(lambda: self.__set_basic_text_filtering(
            self.tags_tab_table.filter_proxy_model,
            self.tags_tab_searchbar.searchbar)
        )
        self.tags_tab_table = common_table_view.CommonTableView(
            ["Name", "Description"], self.table_tags,
            stretch_column=1
        )
        self.tags_tab_table.selectionModel().selectionChanged.connect(self.table_update_buttons_enabling)
        
        self.tags_tab_layout.setColumnStretch(0, 1)
        self.tags_tab_layout.setColumnStretch(2, 1)
        
        self.tags_tab_layout.addWidget(self.tags_tab_searchbar, 0, 0)
        self.tags_tab_layout.addWidget(self.tags_filter_button, 0, 1)
        self.tags_tab_layout.addWidget(QtWidgets.QWidget(), 0, 2)
        self.tags_tab_layout.addWidget(self.tags_tab_table, 1, 0, 1, 3)



    def __init_filters_tab(self):
        self.filters_tab_layout = QtWidgets.QGridLayout(self.filters_tab_widget)
        self.filters_tab_searchbar = searchbar_with_icon.SearchBarWithIcon(objectName="search_container")
        self.filters_filter_button = QtWidgets.QPushButton("Filter")
        self.filters_filter_button.clicked.connect(lambda: self.__set_basic_text_filtering(
            self.filters_tab_table.filter_proxy_model,
            self.filters_tab_searchbar.searchbar)
        )
        self.filters_tab_table = common_table_view.CommonTableView(
            ["Name", "Order", "Note name", "Category name"], self.table_filters,
            stretch_column=0,
            sort_column=1
        )
        self.filters_tab_table.selectionModel().selectionChanged.connect(self.table_update_buttons_enabling)
        
        self.filters_tab_layout.setColumnStretch(0, 1)
        self.filters_tab_layout.setColumnStretch(2, 1)
        
        self.filters_tab_layout.addWidget(self.filters_tab_searchbar, 0, 0)
        self.filters_tab_layout.addWidget(self.filters_filter_button, 0, 1)
        self.filters_tab_layout.addWidget(QtWidgets.QWidget(), 0, 2)
        self.filters_tab_layout.addWidget(self.filters_tab_table, 1, 0, 1, 3)



    @QtCore.Slot()
    def tab_update_buttons_enabling(self, index):
        if index == 0: # Notes tab
            if self.is_table_view:
                selected_rows_count = self.count_selected_rows(self.notes_tab_table)
            else:
                selected_rows_count = self.count_selected_notes()
        elif index == 1: # Categories tab
            selected_rows_count = self.count_selected_rows(self.categories_tab_table)
        elif index == 2: # Tags tab
            selected_rows_count = self.count_selected_rows(self.tags_tab_table)
        elif index == 3: # Filters tab
            selected_rows_count = self.count_selected_rows(self.filters_tab_table)
        else: # Error
            self.edit_icon_button.setEnabled(False)
            self.delete_icon_button.setEnabled(False)
        self.edit_icon_button.setEnabled(selected_rows_count == 1)
        self.delete_icon_button.setEnabled(selected_rows_count >= 1)
            


    def count_selected_rows(self, table):
        return len(table.selectionModel().selectedRows())



    def count_selected_notes(self):
        return len(self.notes_tab_accordion.get_selected_notes())



    @QtCore.Slot()
    def table_update_buttons_enabling(self):
        current_tab_name = self.tabs.currentWidget().objectName()
        if current_tab_name == "notes_tab":
            selected_rows_count = self.count_selected_rows(self.notes_tab_table)
        elif current_tab_name == "categories_tab":
            selected_rows_count = self.count_selected_rows(self.categories_tab_table)
        elif current_tab_name == "tags_tab":
            selected_rows_count = self.count_selected_rows(self.tags_tab_table)
        elif current_tab_name == "filters_tab":
            selected_rows_count = self.count_selected_rows(self.filters_tab_table)
        else:
            self.edit_icon_button.setEnabled(False)
            self.delete_icon_button.setEnabled(False)
        self.edit_icon_button.setEnabled(selected_rows_count == 1)
        self.delete_icon_button.setEnabled(selected_rows_count >= 1)



    @QtCore.Slot()
    def notes_accordion_buttons_enabling(self):
        if self.tabs.currentWidget().objectName() == "notes_tab" and not self.is_table_view:
            selected_notes_count = self.count_selected_notes()
            self.edit_icon_button.setEnabled(selected_notes_count == 1)
            self.delete_icon_button.setEnabled(selected_notes_count >= 1)


    
    # Operations on items

    @QtCore.Slot()
    def add_item(self):
        self.loading_bar.loading_bar.setRange(0, 0)
        self.item_action("ADD")
        self.loading_bar.loading_bar.setRange(0, 1)


    
    @QtCore.Slot()
    def edit_item(self):
        self.loading_bar.loading_bar.setRange(0, 0)
        self.item_action("EDIT")
        self.loading_bar.loading_bar.setRange(0, 1)


    
    def item_action(self, action_name):
        current_tab_name = self.tabs.currentWidget().objectName()
        if current_tab_name == "notes_tab":
            if action_name == "EDIT":
                self._edit_note()
            elif action_name == "ADD":
                self._add_note()

        elif current_tab_name == "categories_tab":
            if action_name == "EDIT":
                self._edit_category()
            elif action_name == "ADD":
                self._add_category()

        elif current_tab_name == "tags_tab":
            if action_name == "EDIT":
                self._edit_tag()
            elif action_name == "ADD":
                self._add_tag()

        elif current_tab_name == "filters_tab":
            if action_name == "EDIT":
                self._edit_filter()

            elif action_name == "ADD":
                self._add_filter()
        else:
            self.display_error_message_box("Unknown tab")
        
        self.update_notes_tab_accordion()
        self.notes_accordion_buttons_enabling()



    def display_error_message_box(self, text):
        message_box = QtWidgets.QMessageBox(self)
        message_box.setWindowTitle("Error")
        message_box.setText(text)
        message_box.exec()
        


    # CRUD operations for all items

    def _add_note(self):
        categories_names = [category.name for category in self.controller.get_categories()]
        tags_names = [tag.name for tag in self.controller.get_tags()]
        
        dialog = note_dialog.NoteDialog(categories_names, tags_names, objectName="dialog")
        if dialog.exec():
            new_note = lambda: None
            new_note.name = dialog.data_dict["name"]
            new_note.time = dialog.data_dict["time"].toPython()
            new_note.text = dialog.data_dict["text"]
            new_note.priority = int(dialog.data_dict["priority"])
            new_note.category_name = dialog.data_dict["category"]
            new_note.tags_names = dialog.data_dict["tags"]
            if self.controller.create_note(new_note):
                self.add_note_to_todays_notes(new_note)
                if self._is_note_filter_accepted(new_note):
                    new_note_row = (new_note.name, new_note.priority, new_note.time.strftime("%d/%m/%Y %H:%M"), new_note.text)
                    self.notes_tab_table.add_row(new_note_row)
            else:
                self.display_error_message_box(f"Note with {new_note.name} already exists")



    def _edit_note(self):
        categories_names = [category.name for category in self.controller.get_categories()]
        tags_names = [tag.name for tag in self.controller.get_tags()]
        selected_note = self._get_selected_note()
        
        dialog = note_dialog.NoteDialog(categories_names, tags_names, objectName="dialog")
        dialog.fill_dialog(selected_note)
        if dialog.exec():
            updated_note = lambda: None
            updated_note.name = dialog.data_dict["name"]
            updated_note.time = dialog.data_dict["time"].toPython()
            updated_note.text = dialog.data_dict["text"]
            updated_note.priority = int(dialog.data_dict["priority"])
            updated_note.category_name = dialog.data_dict["category"]
            updated_note.tags_names = dialog.data_dict["tags"]
            if self.controller.update_note(selected_note.id, updated_note):
                self.remove_notes_from_todays_notes([updated_note.name])
                self.add_note_to_todays_notes(updated_note)
                if self._is_note_filter_accepted(updated_note):
                    old_note_row = (selected_note.name, selected_note.priority, selected_note.time.strftime("%d/%m/%Y %H:%M"), selected_note.text)
                    new_note_row = (updated_note.name, updated_note.priority, updated_note.time.strftime("%d/%m/%Y %H:%M"), updated_note.text)
                    self.notes_tab_table.replace_row(old_note_row, new_note_row)
            else:
                self.display_error_message_box(f"Note with {updated_note.name} already exists")



    def _is_note_filter_accepted(self, note):
        if self.current_note_filter == None:
            return True
        return self.current_note_filter.note_name in note.name and \
               self.current_note_filter.note_min_time <= note.time and \
               self.current_note_filter.note_max_time >= note.time and \
               self.current_note_filter.note_text in note.text and \
               self.current_note_filter.note_min_priority <= note.priority and \
               self.current_note_filter.note_max_priority >= note.priority and \
               self.current_note_filter.category_name in note.category_name and \
               (len([tag for tag in note.tags_names if self.current_note_filter.tag_name in tag]) > 0 or \
                self.current_note_filter.tag_name == "")



    def _add_category(self):
        dialog = category_dialog.CategoryDialog(objectName="dialog")
        if dialog.exec():
            new_category = lambda: None
            new_category.name = dialog.data_dict["name"]
            new_category.description = dialog.data_dict["description"]
            if self.controller.create_category(new_category):
                new_category_row = (new_category.name, new_category.description)
                self.categories_tab_table.add_row(new_category_row)
            else:
                self.display_error_message_box(f"Category with {new_category.name} already exists")



    def _edit_category(self):
        selected_category = self._get_selected_category()
        
        dialog = category_dialog.CategoryDialog(objectName="dialog")
        dialog.fill_dialog(selected_category)
        if dialog.exec():
            updated_category = lambda: None
            updated_category.name = dialog.data_dict["name"]
            updated_category.description = dialog.data_dict["description"]
            if self.controller.update_category(selected_category.id, updated_category):
                old_category = self.categories_tab_table.get_selected_rows()[0]
                new_category = (updated_category.name, updated_category.description)
                self.categories_tab_table.replace_row(old_category, new_category)
            else:
                self.display_error_message_box(f"Category with {updated_category.name} already exists")


    def _add_tag(self):
        dialog = tag_dialog.TagDialog(objectName="dialog")
        if dialog.exec():
            new_tag = lambda: None
            new_tag.name = dialog.data_dict["name"]
            new_tag.description = dialog.data_dict["description"]
            if self.controller.create_tag(new_tag):
                new_tag_row = (new_tag.name, new_tag.description)
                self.tags_tab_table.add_row(new_tag_row)
            else:
                self.display_error_message_box(f"Tag with {new_tag.name} already exists")


    def _edit_tag(self):
        selected_tag = self._get_selected_tag()
        
        dialog = tag_dialog.TagDialog(objectName="dialog")
        dialog.fill_dialog(selected_tag)
        if dialog.exec():
            updated_tag = lambda: None
            updated_tag.name = dialog.data_dict["name"]
            updated_tag.description = dialog.data_dict["description"]
            if self.controller.update_tag(selected_tag.id, updated_tag):
                old_tag = self.tags_tab_table.get_selected_rows()[0]
                new_tag = (updated_tag.name, updated_tag.description)
                self.tags_tab_table.replace_row(old_tag, new_tag)
            else:
                self.display_error_message_box(f"Tag with {updated_tag.name} already exists")


    def _add_filter(self):
        dialog = filter_dialog.FilterDialog(objectName="dialog")
        if dialog.exec():
            new_filter = lambda: None
            new_filter.name = dialog.data_dict["name"]
            new_filter.note_name = dialog.data_dict["note_name"]
            new_filter.note_min_priority = int("0" + dialog.data_dict["note_min_priority"])
            new_filter.note_max_priority = int("0" + dialog.data_dict["note_max_priority"])
            new_filter.note_min_time = dialog.data_dict["note_from_time"].toPython()
            new_filter.note_max_time = dialog.data_dict["note_to_time"].toPython()
            new_filter.note_text = dialog.data_dict["note_text"]
            new_filter.tag_name = dialog.data_dict["tag_name"]
            new_filter.tag_description = dialog.data_dict["tag_description"]
            new_filter.category_name = dialog.data_dict["category_name"]
            new_filter.category_description = dialog.data_dict["category_description"]
            new_filter.order = int(dialog.data_dict["order"])

            ordered_filters = [fast_filter for fast_filter in self.controller.find_filter_by_order_listed(updated_filter.order)]
            
            if self.controller.create_filter(new_filter):
                new_filter_row = (new_filter.name,
                                  new_filter.order,
                                  new_filter.note_name,
                                  new_filter.category_name)
                self.filters_tab_table.add_row(new_filter_row)

                table_rows = [(row.name,
                               row.order,
                               row.note_name,
                               row.category_name) for row in ordered_filters if row.name != new_filter.name]
                self.filters_tab_table.delete_rows(table_rows)

                for i, row in enumerate(table_rows):
                    table_rows[i] = row[0], -1, row[2], row[3]
                    self.filters_tab_table.add_row(table_rows[i])
            else:
                self.display_error_message_box(f"Fast filter with {new_filter.name} already exists")


    def _edit_filter(self):
        selected_filter = self._get_selected_filter()
        
        dialog = filter_dialog.FilterDialog(objectName="dialog")
        dialog.fill_dialog(selected_filter)
        if dialog.exec():
            updated_filter = lambda: None
            updated_filter.name = dialog.data_dict["name"]
            updated_filter.note_name = dialog.data_dict["note_name"]
            updated_filter.note_min_priority = int("0" + dialog.data_dict["note_min_priority"])
            updated_filter.note_max_priority = int("0" + dialog.data_dict["note_max_priority"])
            updated_filter.note_min_time = dialog.data_dict["note_from_time"].toPython()
            updated_filter.note_max_time = dialog.data_dict["note_to_time"].toPython()
            updated_filter.note_text = dialog.data_dict["note_text"]
            updated_filter.tag_name = dialog.data_dict["tag_name"]
            updated_filter.tag_description = dialog.data_dict["tag_description"]
            updated_filter.category_name = dialog.data_dict["category_name"]
            updated_filter.category_description = dialog.data_dict["category_description"]
            updated_filter.order = int("0" + dialog.data_dict["order"])

            ordered_filters = [fast_filter for fast_filter in self.controller.find_filter_by_order_listed(updated_filter.order)]

            if self.controller.update_filter(selected_filter.id, updated_filter):
                old_filter = self.filters_tab_table.get_selected_rows()[0]
                new_filter = (updated_filter.name,
                              updated_filter.order,
                              updated_filter.note_name,
                              updated_filter.category_name)
                self.filters_tab_table.replace_row(old_filter, new_filter)
    
                table_rows = [(row.name,
                               row.order,
                               row.note_name,
                               row.category_name) for row in ordered_filters if row.name != updated_filter.name]
                self.filters_tab_table.delete_rows(table_rows)

                for i, row in enumerate(table_rows):
                    table_rows[i] = row[0], -1, row[2], row[3]
                    self.filters_tab_table.add_row(table_rows[i])
            else:
                self.display_error_message_box(f"Fast filter with {updated_filter.name} already exists")



    @QtCore.Slot()
    def delete_items(self):
        current_tab_name = self.tabs.currentWidget().objectName()
        if current_tab_name == "notes_tab":
            if self.is_table_view:
                selected_rows = self.notes_tab_table.get_selected_rows()
                selected_notes = [note[0] for note in selected_rows]
                self.notes_tab_table.delete_selection()
            else:
                selected_rows = self.notes_tab_accordion.get_selected_notes()
                selected_notes = [note.name for note in selected_rows]
                table_rows = [(note.name, note.priority, note.time.strftime("%d/%m/%Y %H:%M"), note.text) for note in selected_rows]
                self.notes_tab_table.delete_rows(table_rows)
            self.controller.delete_notes(selected_notes)
            self.remove_notes_from_todays_notes(selected_notes)

        elif current_tab_name == "categories_tab":
            selected_rows = self.categories_tab_table.get_selected_rows()
            selected_categories = [category[0] for category in selected_rows]
            if self.controller.delete_categories(selected_categories):
                self.categories_tab_table.delete_selection()
            else:
                self.display_error_message_box("Can not delete categories with assigned notes")
        
        elif current_tab_name == "tags_tab":
            selected_rows = self.tags_tab_table.get_selected_rows()
            selected_tags = [tag[0] for tag in selected_rows]
            self.controller.delete_tags(selected_tags)
            self.tags_tab_table.delete_selection()
        
        elif current_tab_name == "filters_tab":
            selected_rows = self.filters_tab_table.get_selected_rows()
            selected_filters = [fast_filter[0] for fast_filter in selected_rows]
            self.controller.delete_filters(selected_filters)
            self.filters_tab_table.delete_selection()
        
        else:
            self.display_error_message_box("Unknown tab")

        self.update_notes_tab_accordion()
        self.notes_accordion_buttons_enabling()



    def _get_selected_note(self):
        if self.is_table_view:
            selected_notes = self.notes_tab_table.get_selected_rows()
            if len(selected_notes) != 1:
                return None
            return self.controller.find_detailed_note_by_name(selected_notes[0][0])
        else:
            selected_notes = self.notes_tab_accordion.get_selected_notes()
            if len(selected_notes) != 1:
                return None
            return selected_notes[0]



    def _get_selected_category(self):
        selected_categories = self.categories_tab_table.get_selected_rows()
        if len(selected_categories) != 1:
            return None
        return self.controller.find_category_by_name(selected_categories[0][0])



    def _get_selected_tag(self):
        selected_tags = self.tags_tab_table.get_selected_rows()
        if len(selected_tags) != 1:
            return None
        return self.controller.find_tag_by_name(selected_tags[0][0])



    def _get_selected_filter(self):
        selected_filters = self.filters_tab_table.get_selected_rows()
        if len(selected_filters) != 1:
            return None
        return self.controller.find_filter_by_name(selected_filters[0][0])



    @QtCore.Slot()
    def change_notes_tab_accordion_page(self):
        self.grid_page = self.notes_tab_accordion_pagination.current_page
        self.update_notes_tab_accordion()
        selected_rows_count = self.count_selected_notes()
        self.edit_icon_button.setEnabled(selected_rows_count == 1)
        self.delete_icon_button.setEnabled(selected_rows_count >= 1)


    def update_notes_tab_accordion(self):
        self.grid_notes = [note for note in self.controller.get_filtered_notes_paged(self.current_note_filter, page=self.grid_page, size=10)]
        self.notes_tab_accordion.replace_sections(self.grid_notes)

        index = self.notes_tab_table.currentIndex()
        self.notes_tab_accordion_pagination.items_count = self.notes_tab_table.model.rowCount(index)
        self.notes_tab_accordion_pagination.create_labels()


    @QtCore.Slot()
    def __set_basic_text_filtering(self, model, searchbar):
        if self.tabs.currentWidget().objectName() == "notes_tab":
            self.current_note_filter = self.create_default_filter()
            self.current_note_filter.note_name = searchbar.text()
            self.use_current_note_filter()
        model.setFilterFixedString(searchbar.text())



    def create_default_filter(self):
        filters = lambda: None
        filters.note_name = ""
        filters.note_min_priority = 0
        filters.note_max_priority = 100
        filters.note_min_time = datetime.min
        filters.note_max_time = datetime.max
        filters.note_text = ""
        filters.category_name = ""
        filters.category_description = ""
        filters.tag_name = ""
        filters.tag_description = ""
        return filters



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    stylesheet="style.qss"
    with open(stylesheet, "r") as f:
        app.setStyleSheet(f.read())

    use_cases = UseCases.UseCases()
    widget = MainWindow(use_cases)
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
