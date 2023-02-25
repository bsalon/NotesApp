import sys
import random

from datetime import datetime

from Controllers import UseCases

import loading_bar
import common_table_view
import pagination_widget
import searchbar_with_icon
import time_widget
import todays_notes_row_widget
import toggle_switch_button

from dialogs import advanced_filter_dialog, note_dialog, tag_dialog, category_dialog, filter_dialog, collapsable_tree_dialog

from PySide6 import QtCore, QtWidgets, QtGui

# Index -> Controller.Index() getAllNotes() -- set todays notes and the table of notes



class MainWindow(QtWidgets.QWidget):
    def __init__(self, use_cases, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.controller = use_cases # TODO RENAME

        # FIXME use controllers
        controller_notes = [note for note in self.controller.get_notes()]

        self.table_notes = [(note.name, note.priority, note.time.strftime("%d/%m/%Y %H:%M"), note.text) for note in controller_notes]
        self.today_notes = [(note.time.strftime("%H:%M"), note.name) for note in controller_notes if note.time.date() == datetime.today().date()]

        self.table_tags = [(tag.name, tag.description) for tag in self.controller.get_tags()]
        
        self.table_categories = [(category.name, category.description) for category in self.controller.get_categories()]
        
        #self.filters = [[str(note.name), str(note.priority), str(note.time), str(note.text)] for note in controller.get_filters()]
        
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

        # Today's notes icon button
        self.icon = QtGui.QIcon()
        self.icon.addFile("/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/TodaysNotesIcon.png")
        self.today_notes_icon_button = QtWidgets.QToolButton()
        self.today_notes_icon_button.setText("Today's notes")
        self.today_notes_icon_button.setToolButtonStyle(QtGui.Qt.ToolButtonTextUnderIcon)
        self.today_notes_icon_button.setIcon(self.icon)
        self.today_notes_icon_button.setIconSize(QtCore.QSize(28, 28))
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

        # Add icon button
        self.add_icon = QtGui.QIcon()
        self.add_icon.addFile("/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/AddIcon.png")
        self.add_icon_button = QtWidgets.QToolButton()
        self.add_icon_button.setIcon(self.add_icon)
        self.add_icon_button.setIconSize(QtCore.QSize(28, 28))
        self.add_icon_button.setObjectName("toolbar_icon_button")
        self.add_icon_button.clicked.connect(self.add_item) # FIXME: Use controller (selected tab)
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
        self.edit_icon_button.clicked.connect(self.edit_item) # FIXME: Use controller (selected tab, selected item)
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
        self.delete_icon_button.clicked.connect(self.delete_items) # FIXME: Use controller (selected tab, selected items)
        self.toolbar_layout.addWidget(self.delete_icon_button, 0, col, 0, 2, alignment=QtGui.Qt.AlignCenter)
        col += 2

        # FIXME: working loading bar
        self.loading_bar = loading_bar.LoadingBarWidget(barObjectName="loading_bar")
        self.toolbar_layout.addWidget(self.loading_bar, 0, col, 0, 5)
        col += 5

        # Settings icon button
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


    
    def __init_todays_notes_layout(self):
        self.todays_notes_layout.setContentsMargins(0, 0, 0, 0)
        self.todays_notes_layout.setSpacing(0)
        
        self.todays_notes_header = QtWidgets.QLabel("Today's notes", objectName="todays_notes_header")
        self.todays_notes_header.setAlignment(QtCore.Qt.AlignHCenter)
        self.todays_notes_header.setMargin(12)
        self.todays_notes_layout.addWidget(self.todays_notes_header)

        self.todays_notes_list = QtWidgets.QListWidget(objectName="todays_notes_list")
        for note in self.today_notes: # TODO remove item
            item = QtWidgets.QListWidgetItem(self.todays_notes_list)
            self.todays_notes_list.addItem(item)

            row = todays_notes_row_widget.TodaysNotesRowWidget(*note)
            item.setSizeHint(row.minimumSizeHint())

            self.todays_notes_list.setItemWidget(item, row)

        self.todays_notes_layout.addWidget(self.todays_notes_list)
        # TODO - set the sizing right -> Data will come from Controller.Index(View(Model))


    # maybe faster algorithm here
    def remove_notes_from_todays_notes(self, notes):
        remove_indices = []
        for i in range(self.todays_notes_list.count()):
            item = self.todays_notes_list.item(i)
            item_widget = self.todays_notes_list.itemWidget(item)
            if item_widget.note_name in notes:
                remove_indices.append(i)

        for i in reversed(sorted(remove_indices)):
            self.todays_notes_list.takeItem(i)
        

    
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

        self.notes_tab_accordion = collapsable_tree_dialog.CollapsableTreeDialog()
        self.notes_tab_accordion.hide()
        self.notes_tab_accordion_pagination = pagination_widget.PaginationWidget(5, len(self.table_notes)) # FIXME size
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
            filters.note_min_priority = int(dialog.data_dict["note_min_priority"])
            filters.note_max_priority = int(dialog.data_dict["note_max_priority"])
            filters.note_min_time = dialog.data_dict["note_from_date"].toPython()
            filters.note_max_time = dialog.data_dict["note_to_date"].toPython()
            filters.note_text = dialog.data_dict["note_text"]
            filters.category_name = dialog.data_dict["category_name"]
            filters.category_description = dialog.data_dict["category_description"]
            filters.tag_name = dialog.data_dict["tag_name"]
            filters.tag_description = dialog.data_dict["tag_description"]
            
            self.current_note_filter = filters

            filtered_notes = self.controller.get_filtered_notes(filters)
            self.table_notes = [(note.name, note.priority, note.time.strftime("%d/%m/%Y %H:%M"), note.text) for note in filtered_notes]
            
            # TODO self.grid_notes = [note for note in self.controller.get_filtered_notes_paged(filters, page=1, size=10)]

            print(*self.table_notes)
            self.notes_tab_table.replace_data(list(set(self.table_notes)))



    @QtCore.Slot()
    def toggle_notes_view(self, table_view):
        self.is_table_view = table_view
        if table_view:
            self.notes_tab_accordion.hide()
            self.notes_tab_accordion_pagination.hide()
            self.notes_tab_table.show()
        else:
            self.notes_tab_table.hide()
            self.notes_tab_accordion.show()
            self.notes_tab_accordion_pagination.show()


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
        # FIXME: Use Controller
        self.filters_tab_table = common_table_view.CommonTableView(
            ["Name", "Time", "Text"],
            [
                ["Note name", "12.8.2023", "This text belongs to this note"],
                ["Note name", "12.8.2023", "This text belongs to this note"],
                ["Note text", "12.8.2023", "Another text a bit shorter"],
                ["Short note", "13.8.2023", "Very short text"],
                ["Note", "14.8.2023", "This text is a medium length text"],
                ["Note name", "12.8.2023", "This text belongs to this note"],
                ["Note text", "12.8.2023", "Another text a bit shorter"],
                ["Short note", "13.8.2023", "Very short text"],
                ["Note", "14.8.2023", "This text is a medium length text"],
                ["Note text", "12.8.2023", "Another text a bit shorter"],
                ["Short note", "13.8.2023", "Very short text"],
                ["Note", "14.8.2023", "This text is a medium length text"],
                ["Note name", "12.8.2023", "This text belongs to this note"],
                ["Note text", "12.8.2023", "Another text a bit shorter"],
                ["Short note", "13.8.2023", "Very short text"],
                ["Note", "14.8.2023", "This text is a medium length text"],
            ],
            2
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
                selected_rows_count = self.count_selected_notes() # FIXME
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


    def count_selected_notes(self): # TODO
        return 0


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
    def add_item(self):
        self.loading_bar.loading_bar.setRange(0, 0)
        self.item_action("ADD")
        self.loading_bar.loading_bar.setRange(0, 1)

    
    @QtCore.Slot()
    def edit_item(self):
        self.loading_bar.loading_bar.setRange(0, 0)
        self.item_action("EDIT")
        self.loading_bar.loading_bar.setRange(0, 1)

    
    def item_action(self, action_name): # TODO fill data and retrieve them
        current_tab_name = self.tabs.currentWidget().objectName()
        if current_tab_name == "notes_tab":
            categories_names = [category.name for category in self.controller.get_categories()]
            tags_names = [tag.name for tag in self.controller.get_tags()]
            dialog = note_dialog.NoteDialog(categories_names, tags_names, objectName="dialog")
            if action_name == "EDIT":
                selected_note = self.get_selected_note()
                dialog.fill_dialog(selected_note)
                if dialog.exec():
                    updated_note = lambda: None
                    updated_note.name = dialog.data_dict["name"]
                    updated_note.time = dialog.data_dict["time"].toPython()
                    updated_note.text = dialog.data_dict["text"]
                    updated_note.priority = int(dialog.data_dict["priority"])
                    updated_note.category_name = dialog.data_dict["category"]
                    updated_note.tags_names = dialog.data_dict["tags"]
                    self.controller.update_note(selected_note.id, updated_note) # TODO: check existing name
                    # TODO update table

        elif current_tab_name == "categories_tab":
            dialog = category_dialog.CategoryDialog(objectName="dialog")
            if action_name == "EDIT":
                selected_category = self.get_selected_category()
                dialog.fill_dialog(selected_category)

        elif current_tab_name == "tags_tab":
            dialog = tag_dialog.TagDialog(objectName="dialog")
            if action_name == "EDIT":
                selected_tag = self.get_selected_tag()
                dialog.fill_dialog(selected_tag)

        elif current_tab_name == "filters_tab":
            dialog = filter_dialog.FilterDialog(objectName="dialog")
            if action_name == "EDIT":
                selected_filter = self.get_selected_filter()
                dialog.fill_dialog(selected_filter)

        else:
            dialog = QtWidgets.QDialog() # TODO show error message
            dialog.exec()


    def get_selected_note(self):
        if self.is_table_view:
            selected_notes = self.notes_tab_table.get_selected_rows()
            if len(selected_notes) != 1:
                return None
            return self.controller.find_detailed_note_by_name(selected_notes[0][0])
        else:
            # TODO note from grid
            pass


    def get_selected_category(self):
        selected_categories = self.categories_tab_table.get_selected_rows()
        return selected_categories[0] if len(selected_categories) == 1 else None


    def get_selected_tag(self):
        selected_tags = self.tags_tab_table.get_selected_rows()
        return selected_tags[0] if len(selected_tags) == 1 else None


    def get_selected_filter(self):
        selected_filters = self.filters_tab_table.get_selected_rows()
        if len(selected_filters) != 1:
            return None
        return self.controller.find_filter_by_name(selected_filters[0][0])


    @QtCore.Slot()
    def delete_items(self): # TODO
        current_tab_name = self.tabs.currentWidget().objectName()
        if current_tab_name == "notes_tab":
            if self.is_table_view:
                pass
                selected_rows = self.notes_tab_table.get_selected_rows()
                selected_notes = [note[0] for note in selected_rows]
            else:
                pass # TODO grid checked items
                selected_notes = []
            controller.delete_notes(selected_notes)
            self.notes_tab_table.delete_selection()
            self.remove_notes_from_todays_notes(selected_notes)

        elif current_tab_name == "categories_tab":
            selected_rows = self.categories_tab_table.get_selected_rows()
            selected_categories = [category[0] for category in selected_rows]
            controller.delete_categories(selected_categories) # TODO
            self.categories_tab_table.delete_selection()
        
        elif current_tab_name == "tags_tab":
            selected_rows = self.notes_tags_table.get_selected_rows()
            selected_tags = [tag[0] for tag in selected_rows]
            controller.delete_tags(selected_tags) # TODO
            self.tags_tab_table.delete_selection()
        
        elif current_tab_name == "filters_tab":
            selected_rows = self.filters_tab_table.get_selected_rows()
            selected_filters = [fast_filter[0] for fast_filter in selected_rows]
            controller.delete_filters(selected_filters) # TODO
            self.filters_tab_table.delete_selection()
        
        else:
            dialog = QtWidgets.QDialog() # FIXME: show error message
            dialog.exec()


    @QtCore.Slot()
    def __set_basic_text_filtering(self, model, searchbar):
        # You can choose the type of search by connecting to a different slot here.
        # see https://doc.qt.io/qt-5/qsortfilterproxymodel.html#public-slots
        # self.searchbar.textChanged.connect(self.proxy_model.setFilterFixedString)
        model.setFilterFixedString(searchbar.text())



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    stylesheet="style.qss"
    with open(stylesheet, "r") as f:
        app.setStyleSheet(f.read())

    use_cases = UseCases.UseCases()
    #notes = [note for note in controller.get_notes()]
    #print(notes)

    widget = MainWindow(use_cases)
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
