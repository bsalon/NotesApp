import bisect
import pathlib
import random
import sys

from datetime import datetime

from BusinessLogic import UseCases

from PySideApp.dialogs import advanced_filter_dialog, category_dialog, filter_dialog, note_dialog, settings_dialog, tag_dialog

from PySideApp.widgets import clickable_label, common_table_view, loading_bar, notes_accordion, pagination_labels, searchbar_with_icon, time_widget, todays_notes_row_widget, toggle_switch_button

from PySide6 import QtCore, QtWidgets, QtGui



class MainWindow(QtWidgets.QWidget):
    def __init__(self, use_cases, *args, **kwargs):
        """
        Initializes the main window widget with all its contents

        :param use_cases: Class contaning methods that retrieve data for the application
        """

        super(MainWindow, self).__init__(*args, **kwargs)

        # Constant representing which gui is used 0 == PySide
        self.gui = 0

        self.use_cases = use_cases
        
        # Get data from database for tables and accordion
        self.current_note_filter = self.create_default_filter()
        self.grid_page = 1
        self.grid_notes = [note for note in self.use_cases.get_filtered_notes_paged(self.current_note_filter, page=self.grid_page, size=10)]

        controller_notes = [note for note in self.use_cases.get_notes()]
        self.table_notes = [(note.name, note.priority, note.time.strftime("%d/%m/%Y %H:%M"), note.text) for note in controller_notes]
        self.today_notes = [(note.time.strftime("%H:%M"), note.name) for note in controller_notes if note.time.date() == datetime.today().date()]
        self.today_notes.sort(key = lambda note: note[0])

        self.table_tags = [(tag.name, tag.description) for tag in self.use_cases.get_tags()]

        self.table_categories = [(category.name, category.description) for category in self.use_cases.get_categories()]
        
        self.table_filters = [(note_filter.name, 
                               note_filter.order,
                               note_filter.note_name,
                               note_filter.category_name) for note_filter in self.use_cases.get_filters()]
        
        # 15 rows : 8 columns
        self.layout = QtWidgets.QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Toolbar layout on top
        self.toolbar_container_widget = QtWidgets.QWidget(objectName="toolbar_container")
        self.toolbar_layout = QtWidgets.QGridLayout(self.toolbar_container_widget)
        self._init_toolbar_layout()
        self.layout.addWidget(self.toolbar_container_widget, 0, 0, 1, 8)
        
        # Todays notes layout
        self.todays_notes_container_widget = QtWidgets.QWidget(objectName="todays_notes_container")
        self.todays_notes_layout = QtWidgets.QGridLayout(self.todays_notes_container_widget)
        self._init_todays_notes_layout()
        self.layout.addWidget(self.todays_notes_container_widget, 1, 0, 14, 1)
        
        # Content layout
        self.tabs_content_container_widget = QtWidgets.QWidget(objectName="tabs_content_container")
        self.tabs_content_layout = QtWidgets.QGridLayout(self.tabs_content_container_widget)
        self._init_tabs_content_layout()
        self.layout.addWidget(self.tabs_content_container_widget, 1, 1, 14, 7)

        # Stretch rows and columns
        for r in range(15):
            self.layout.setRowStretch(r, 1)
        for c in range(8):
            self.layout.setColumnStretch(c, 1)
        self.setLayout(self.layout)



    def _init_toolbar_layout(self):
        """
        Initializes widgets in the toolbar
        """

        col = 0
        image_dir_path = pathlib.Path(__file__).parent.parent / "Images"

        # Today's notes icon button
        todays_notes_icon_path = image_dir_path / "TodaysNotesIcon.png"
        todays_notes_icon = QtGui.QIcon()
        todays_notes_icon.addFile(todays_notes_icon_path.resolve().as_posix())
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
        self.toolbar_layout.addWidget(QtWidgets.QLabel("Use fast filters:", objectName="black_label"), 0, col, 0, 3, alignment=QtGui.Qt.AlignCenter)
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
        add_icon_path = image_dir_path / "AddIcon.png"
        add_icon = QtGui.QIcon()
        add_icon.addFile(add_icon_path.resolve().as_posix())
        self.add_icon_button = QtWidgets.QToolButton()
        self.add_icon_button.setIcon(add_icon)
        self.add_icon_button.setIconSize(QtCore.QSize(28, 28))
        self.add_icon_button.setObjectName("toolbar_icon_button")
        self.add_icon_button.clicked.connect(self.add_item)
        self.toolbar_layout.addWidget(self.add_icon_button, 0, col, 0, 2, alignment=QtGui.Qt.AlignCenter)
        col += 2
        
        # Edit icon button
        edit_icon_path = image_dir_path / "EditIcon.png"
        self.edit_icon = QtGui.QIcon()
        self.edit_icon.addFile(edit_icon_path.resolve().as_posix())
        self.edit_icon_button = QtWidgets.QToolButton()
        self.edit_icon_button.setIcon(self.edit_icon)
        self.edit_icon_button.setIconSize(QtCore.QSize(28, 28))
        self.edit_icon_button.setObjectName("toolbar_icon_button")
        self.edit_icon_button.setEnabled(False)
        self.edit_icon_button.clicked.connect(self.edit_item)
        self.toolbar_layout.addWidget(self.edit_icon_button, 0, col, 0, 2, alignment=QtGui.Qt.AlignCenter)
        col += 2
        
        # Delete icon button
        delete_icon_path = image_dir_path / "DeleteIcon.png"
        self.delete_icon = QtGui.QIcon()
        self.delete_icon.addFile(delete_icon_path.resolve().as_posix())
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

        # Settings icon button
        settings_icon_path = image_dir_path / "SettingsIcon.png"
        self.settings_icon = QtGui.QIcon()
        self.settings_icon.addFile(settings_icon_path.resolve().as_posix())
        self.settings_button = QtWidgets.QToolButton()
        self.settings_button.setIcon(self.settings_icon)
        self.settings_button.setIconSize(QtCore.QSize(28, 28))
        self.settings_button.setObjectName("toolbar_icon_button")
        self.settings_button.clicked.connect(self.change_library)
        self.toolbar_layout.addWidget(self.settings_button, 0, col, 0, 2, alignment=QtGui.Qt.AlignRight)
        col += 2

        # Stretch time widget more than other widgets
        for c in range(col):
            self.toolbar_layout.setColumnStretch(c, 1)
        for time_col in range(14, 19):
            self.toolbar_layout.setColumnStretch(time_col, 2)



    def change_library(self):
        """
        Changes the used gui library of the application
        """

        dialog = settings_dialog.SettingsDialog(objectName="dialog")
        if dialog.exec():
            self.gui = dialog.data_dict["library"]
            if self.gui == 0:
                return
            QtCore.QCoreApplication.quit()



    @QtCore.Slot()
    def toggle_todays_notes_pane(self):
        """
        Toggles the visibility of todays notes pane
        """

        # Hide todays notes pane
        if self.todays_notes_pane_visible:
            self.todays_notes_container_widget.hide()
            self.layout.addWidget(self.tabs_content_container_widget, 1, 0, 14, 8)
        # Show todays notes pane
        else:
            self.layout.addWidget(self.tabs_content_container_widget, 1, 1, 14, 7)
            self.todays_notes_container_widget.show()
        self.todays_notes_pane_visible = not self.todays_notes_pane_visible



    @QtCore.Slot()
    def use_fast_filter(self, order):
        """
        Uses fast filter from the toolbar layout

        :param order: Order value of the Filter object
        """

        self.current_note_filter = self.use_cases.find_filter_by_order(order)
        if self.current_note_filter == None:
            self.current_note_filter = self.create_default_filter()
            self.display_error_message_box(f"Fast filter with order={order} is not available")
        self.use_current_note_filter()



    def _init_todays_notes_layout(self):
        """
        Initializes widgets in todays notes pane
        """

        self.todays_notes_layout.setContentsMargins(0, 0, 0, 0)
        self.todays_notes_layout.setSpacing(0)
        
        # Todays notes header label
        self.todays_notes_header = QtWidgets.QLabel("Today's notes", objectName="todays_notes_header")
        self.todays_notes_header.setAlignment(QtCore.Qt.AlignHCenter)
        self.todays_notes_header.setMargin(12)
        self.todays_notes_layout.addWidget(self.todays_notes_header)

        # List of todays notes
        # Comparison construct
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
        """
        Removes notes from todays notes pane

        :param notes: Notes to remove from todays notes pane
        """

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
        """
        Adds note to todays notes pane

        :param note: Note to add to todays notes pane
        """

        # Add only if date of note is today
        if note.time.date() == datetime.today().date():
            note_tuple = (note.time.strftime("%H:%M"), note.name)
            bisect.insort_left(self.today_notes, note_tuple)

            new_note_index = self.today_notes.index(note_tuple)

            item = QtWidgets.QListWidgetItem()
            self.todays_notes_list.insertItem(new_note_index, item)
            row = todays_notes_row_widget.TodaysNotesRowWidget(*note_tuple)
            item.setSizeHint(row.minimumSizeHint())
            self.todays_notes_list.setItemWidget(item, row)


    
    def _init_tabs_content_layout(self):
        """
        Initializes tabs widget
        """

        self.tabs = QtWidgets.QTabWidget(objectName="tabs")

        # Specific tabs
        self.notes_tab_widget = QtWidgets.QWidget(objectName="notes_tab")
        self._init_notes_tab()
        self.categories_tab_widget = QtWidgets.QWidget(objectName="categories_tab")
        self._init_categories_tab()
        self.tags_tab_widget = QtWidgets.QWidget(objectName="tags_tab")
        self._init_tags_tab()
        self.filters_tab_widget = QtWidgets.QWidget(objectName="filters_tab")
        self._init_filters_tab()

        # Adding initialized tabs
        self.tabs.addTab(self.notes_tab_widget, "Notes")
        self.tabs.addTab(self.categories_tab_widget, "Categories")
        self.tabs.addTab(self.tags_tab_widget, "Tags")
        self.tabs.addTab(self.filters_tab_widget, "Fast filters")
        
        self.tabs.currentChanged.connect(self.tab_update_buttons_enabling)
        self.tabs_content_layout.addWidget(self.tabs)



    def _init_notes_tab(self):
        """
        Initializes widgets in the notes tab
        """

        self.notes_tab_layout = QtWidgets.QGridLayout(self.notes_tab_widget)

        self.notes_tab_filtering_container_widget = QtWidgets.QWidget(objectName="filtering_container")
        self.notes_tab_filtering_layout = QtWidgets.QGridLayout(self.notes_tab_filtering_container_widget)
        self.notes_tab_filtering_layout.setContentsMargins(0, 0, 0, 0)

        self.notes_tab_searchbar = searchbar_with_icon.SearchBarWithIcon(objectName="search_container")
        
        self.notes_filter_button = QtWidgets.QPushButton("Filter", objectName="black_pbutton")
        self.notes_filter_button.setToolTip("Resets fast or advanced filter")
        self.notes_filter_button.clicked.connect(lambda: self._set_basic_text_filtering(
            self.notes_tab_table.filter_proxy_model,
            self.notes_tab_searchbar.searchbar)
        )

        self.notes_advanced_filter_button = QtWidgets.QPushButton("Advanced filter", objectName="black_pbutton")
        self.notes_advanced_filter_button.clicked.connect(self.notes_advanced_filtering)

        self.notes_toggle_switch_label = QtWidgets.QLabel("Table view", objectName="black_label")
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

        # Accordion with pagination
        self.notes_tab_accordion = notes_accordion.NotesAccordion(self.grid_notes)
        self.notes_tab_accordion.selection_changed.connect(self.notes_accordion_buttons_enabling)
        self.notes_tab_accordion.hide()
        self.notes_tab_accordion_pagination = pagination_labels.PaginationLabels(10, len(self.table_notes))
        self.notes_tab_accordion_pagination.page_changed.connect(self.change_notes_tab_accordion_page)
        
        self.notes_tab_accordion_pagination.hide()
        self.is_table_view = True

        self.notes_tab_layout.addWidget(self.notes_tab_filtering_container_widget, 0, 0, alignment=QtCore.Qt.AlignTop)
        self.notes_tab_layout.addWidget(self.notes_tab_table, 1, 0)
        self.notes_tab_layout.addWidget(self.notes_tab_accordion, 2, 0)
        self.notes_tab_layout.addWidget(self.notes_tab_accordion_pagination, 3, 0, alignment=QtCore.Qt.AlignCenter)
        


    @QtCore.Slot()
    def notes_advanced_filtering(self):
        """
        Opens advanced filter dialog and filters notes based on its values
        """

        dialog = advanced_filter_dialog.AdvancedFilterDialog(objectName="dialog")
        if dialog.exec():
            filters = lambda: None
            filters.note_name = dialog.data_dict["note_name"]
            filters.note_min_priority = dialog.data_dict["note_min_priority"]
            filters.note_max_priority = dialog.data_dict["note_max_priority"]
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
        """
        Filters notes based on the currently saved filter
        """

        self.grid_page = self.notes_tab_accordion_pagination.current_page = 1
        filtered_notes = self.use_cases.get_filtered_notes(self.current_note_filter)
        self.table_notes = [(note.name, note.priority, note.time.strftime("%d/%m/%Y %H:%M"), note.text) for note in filtered_notes]

        self.notes_tab_table.replace_data(list(set(self.table_notes)))
        self.update_notes_tab_accordion()



    @QtCore.Slot()
    def toggle_notes_view(self, table_view):
        """
        Toggles visibility of table and accordion based on the toggle state
        """

        self.is_table_view = table_view

        # Hide accordion and show table
        if table_view:
            self.notes_tab_accordion.hide()
            self.notes_tab_accordion_pagination.hide()
            selected_rows_count = self.count_selected_rows(self.notes_tab_table)
            self.notes_tab_table.show()
        # Hide table and show accordion
        else:
            self.notes_tab_table.hide()
            selected_rows_count = self.count_selected_notes()
            self.notes_tab_accordion.show()
            self.notes_tab_accordion_pagination.show()

        self.edit_icon_button.setEnabled(selected_rows_count == 1)
        self.delete_icon_button.setEnabled(selected_rows_count >= 1)



    def _init_categories_tab(self):
        """
        Initializes widgets in the categories tab
        """

        self.categories_tab_layout = QtWidgets.QGridLayout(self.categories_tab_widget)
        self.categories_tab_searchbar = searchbar_with_icon.SearchBarWithIcon(objectName="search_container")
        self.categories_filter_button = QtWidgets.QPushButton("Filter", objectName="black_pbutton")
        self.categories_filter_button.clicked.connect(lambda: self._set_basic_text_filtering(
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



    def _init_tags_tab(self):
        """
        Initializes widgets in the tags tab
        """

        self.tags_tab_layout = QtWidgets.QGridLayout(self.tags_tab_widget)
        self.tags_tab_searchbar = searchbar_with_icon.SearchBarWithIcon(objectName="search_container")
        self.tags_filter_button = QtWidgets.QPushButton("Filter", objectName="black_pbutton")
        self.tags_filter_button.clicked.connect(lambda: self._set_basic_text_filtering(
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



    def _init_filters_tab(self):
        """
        Initializes widgets in the filters tab
        """

        self.filters_tab_layout = QtWidgets.QGridLayout(self.filters_tab_widget)
        self.filters_tab_searchbar = searchbar_with_icon.SearchBarWithIcon(objectName="search_container")
        self.filters_filter_button = QtWidgets.QPushButton("Filter", objectName="black_pbutton")
        self.filters_filter_button.clicked.connect(lambda: self._set_basic_text_filtering(
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
        """
        Updates buttons state based on the count of currently selected rows

        :param index: Index of the tab
        """

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
        """
        Counts number of selected rows in the table

        :param table: Table with selectable rows

        :return: Number of selected rows in the table
        """

        return len(table.selectionModel().selectedRows())



    def count_selected_notes(self):
        """
        Counts number of selected rows in the accordion

        :return: Number of selected rows in the accordion
        """

        return len(self.notes_tab_accordion.get_selected_notes())



    @QtCore.Slot()
    def table_update_buttons_enabling(self):
        """
        Updates buttons state based on the count of currently selected rows in current tabs table
        """

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
        """
        Updates buttons state based on the count of currently selected rows in accordion
        """

        if self.tabs.currentWidget().objectName() == "notes_tab" and not self.is_table_view:
            selected_notes_count = self.count_selected_notes()
            self.edit_icon_button.setEnabled(selected_notes_count == 1)
            self.delete_icon_button.setEnabled(selected_notes_count >= 1)


    
    # Operations on items

    @QtCore.Slot()
    def add_item(self):
        """
        Adds item
        """

        self.loading_bar.loading_bar.setRange(0, 0)
        self.item_action("ADD")
        self.loading_bar.loading_bar.setRange(0, 1)


    
    @QtCore.Slot()
    def edit_item(self):
        """
        Edits item
        """

        self.loading_bar.loading_bar.setRange(0, 0)
        self.item_action("EDIT")
        self.loading_bar.loading_bar.setRange(0, 1)


    
    def item_action(self, action_name):
        """
        Takes action on item

        :param action_name: EDIT or ADD action to be taken on item
        """

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
        """
        Displays error message box

        :param text: Message of error message box
        """

        message_box = QtWidgets.QMessageBox(self)
        message_box.setWindowTitle("Error")
        message_box.setText(text)
        message_box.exec()
        


    # CRUD operations for all items

    def _add_note(self):
        """
        Opens new note dialog
        """

        categories_names = [category.name for category in self.use_cases.get_categories()]
        tags_names = [tag.name for tag in self.use_cases.get_tags()]
        
        dialog = note_dialog.NoteDialog(categories_names, tags_names, objectName="dialog")
        if dialog.exec():
            new_note = lambda: None
            new_note.name = dialog.data_dict["name"]
            new_note.time = dialog.data_dict["time"].toPython()
            new_note.text = dialog.data_dict["text"]
            new_note.priority = dialog.data_dict["priority"]
            new_note.category_name = dialog.data_dict["category"]
            new_note.tags_names = dialog.data_dict["tags"]
            if self.use_cases.create_note(new_note):
                self.add_note_to_todays_notes(new_note)
                if self._is_note_filter_accepted(new_note):
                    new_note_row = (new_note.name, new_note.priority, new_note.time.strftime("%d/%m/%Y %H:%M"), new_note.text)
                    self.notes_tab_table.add_row(new_note_row)
            else:
                self.display_error_message_box(f"Note with name={new_note.name} already exists")



    def _edit_note(self):
        """
        Opens edit dialog for selected note
        """

        categories_names = [category.name for category in self.use_cases.get_categories()]
        tags_names = [tag.name for tag in self.use_cases.get_tags()]
        selected_note = self._get_selected_note()
        
        dialog = note_dialog.NoteDialog(categories_names, tags_names, objectName="dialog")
        dialog.fill_dialog(selected_note)
        if dialog.exec():
            updated_note = lambda: None
            updated_note.name = dialog.data_dict["name"]
            updated_note.time = dialog.data_dict["time"].toPython()
            updated_note.text = dialog.data_dict["text"]
            updated_note.priority = dialog.data_dict["priority"]
            updated_note.category_name = dialog.data_dict["category"]
            updated_note.tags_names = dialog.data_dict["tags"]
            if self.use_cases.update_note(selected_note.id, updated_note):
                self.remove_notes_from_todays_notes([selected_note.name])
                self.add_note_to_todays_notes(updated_note)
                if self._is_note_filter_accepted(updated_note):
                    old_note_row = (selected_note.name, selected_note.priority, selected_note.time.strftime("%d/%m/%Y %H:%M"), selected_note.text)
                    new_note_row = (updated_note.name, updated_note.priority, updated_note.time.strftime("%d/%m/%Y %H:%M"), updated_note.text)
                    self.notes_tab_table.replace_row(old_note_row, new_note_row)
            else:
                self.display_error_message_box(f"Note with name={updated_note.name} already exists")



    def _is_note_filter_accepted(self, note):
        """
        Determines whether current filter accepts the note

        :param note: Note tested against the filter

        :return: True if filter accepts the note False otherwise
        """

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
        """
        Opens new category dialog
        """

        dialog = category_dialog.CategoryDialog(objectName="dialog")
        if dialog.exec():
            new_category = lambda: None
            new_category.name = dialog.data_dict["name"]
            new_category.description = dialog.data_dict["description"]
            if self.use_cases.create_category(new_category):
                new_category_row = (new_category.name, new_category.description)
                self.categories_tab_table.add_row(new_category_row)
            else:
                self.display_error_message_box(f"Category with name={new_category.name} already exists")



    def _edit_category(self):
        """
        Opens edit dialog for selected category
        """

        selected_category = self._get_selected_category()
        if selected_category.name == "Default":
            return

        dialog = category_dialog.CategoryDialog(objectName="dialog")
        dialog.fill_dialog(selected_category)
        if dialog.exec():
            updated_category = lambda: None
            updated_category.name = dialog.data_dict["name"]
            updated_category.description = dialog.data_dict["description"]
            if self.use_cases.update_category(selected_category.id, updated_category):
                old_category = self.categories_tab_table.get_selected_rows()[0]
                new_category = (updated_category.name, updated_category.description)
                self.categories_tab_table.replace_row(old_category, new_category)
            else:
                self.display_error_message_box(f"Category with name={updated_category.name} already exists")


    def _add_tag(self):
        """
        Opens new tag dialog
        """

        dialog = tag_dialog.TagDialog(objectName="dialog")
        if dialog.exec():
            new_tag = lambda: None
            new_tag.name = dialog.data_dict["name"]
            new_tag.description = dialog.data_dict["description"]
            if self.use_cases.create_tag(new_tag):
                new_tag_row = (new_tag.name, new_tag.description)
                self.tags_tab_table.add_row(new_tag_row)
            else:
                self.display_error_message_box(f"Tag with name={new_tag.name} already exists")


    def _edit_tag(self):
        """
        Opens edit dialog for selected tag
        """

        selected_tag = self._get_selected_tag()
        
        dialog = tag_dialog.TagDialog(objectName="dialog")
        dialog.fill_dialog(selected_tag)
        if dialog.exec():
            updated_tag = lambda: None
            updated_tag.name = dialog.data_dict["name"]
            updated_tag.description = dialog.data_dict["description"]
            if self.use_cases.update_tag(selected_tag.id, updated_tag):
                old_tag = self.tags_tab_table.get_selected_rows()[0]
                new_tag = (updated_tag.name, updated_tag.description)
                self.tags_tab_table.replace_row(old_tag, new_tag)
            else:
                self.display_error_message_box(f"Tag with name={updated_tag.name} already exists")


    def _add_filter(self):
        """
        Opens new filter dialog
        """

        dialog = filter_dialog.FilterDialog(objectName="dialog")
        if dialog.exec():
            new_filter = lambda: None
            new_filter.name = dialog.data_dict["name"]
            new_filter.note_name = dialog.data_dict["note_name"]
            new_filter.note_min_priority = dialog.data_dict["note_min_priority"]
            new_filter.note_max_priority = dialog.data_dict["note_max_priority"]
            new_filter.note_min_time = dialog.data_dict["note_from_time"].toPython()
            new_filter.note_max_time = dialog.data_dict["note_to_time"].toPython()
            new_filter.note_text = dialog.data_dict["note_text"]
            new_filter.tag_name = dialog.data_dict["tag_name"]
            new_filter.tag_description = dialog.data_dict["tag_description"]
            new_filter.category_name = dialog.data_dict["category_name"]
            new_filter.category_description = dialog.data_dict["category_description"]
            new_filter.order = dialog.data_dict["order"]

            ordered_filters = [fast_filter for fast_filter in self.use_cases.find_filter_by_order_listed(new_filter.order)]
            
            if self.use_cases.create_filter(new_filter):
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
                self.display_error_message_box(f"Fast filter with name={new_filter.name} already exists")


    def _edit_filter(self):
        """
        Opens edit dialog for selected filter
        """

        selected_filter = self._get_selected_filter()
        
        dialog = filter_dialog.FilterDialog(objectName="dialog")
        dialog.fill_dialog(selected_filter)
        if dialog.exec():
            updated_filter = lambda: None
            updated_filter.name = dialog.data_dict["name"]
            updated_filter.note_name = dialog.data_dict["note_name"]
            updated_filter.note_min_priority = dialog.data_dict["note_min_priority"]
            updated_filter.note_max_priority = dialog.data_dict["note_max_priority"]
            updated_filter.note_min_time = dialog.data_dict["note_from_time"].toPython()
            updated_filter.note_max_time = dialog.data_dict["note_to_time"].toPython()
            updated_filter.note_text = dialog.data_dict["note_text"]
            updated_filter.tag_name = dialog.data_dict["tag_name"]
            updated_filter.tag_description = dialog.data_dict["tag_description"]
            updated_filter.category_name = dialog.data_dict["category_name"]
            updated_filter.category_description = dialog.data_dict["category_description"]
            updated_filter.order = dialog.data_dict["order"]

            ordered_filters = [fast_filter for fast_filter in self.use_cases.find_filter_by_order_listed(updated_filter.order)]

            if self.use_cases.update_filter(selected_filter.id, updated_filter):
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
                self.display_error_message_box(f"Fast filter with name={updated_filter.name} already exists")



    @QtCore.Slot()
    def delete_items(self):
        """
        Deletes currently selected items
        """

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
            self.use_cases.delete_notes(selected_notes)
            self.remove_notes_from_todays_notes(selected_notes)

        elif current_tab_name == "categories_tab":
            selected_rows = self.categories_tab_table.get_selected_rows()
            selected_categories = [category[0] for category in selected_rows]
            if "Default" in selected_categories:
                self.display_error_message_box("Can not delete default category")
                return
            else:
                if self.use_cases.delete_categories(selected_categories):
                    self.categories_tab_table.delete_selection()
                else:
                    self.display_error_message_box("Can not delete category with assigned notes")
        
        elif current_tab_name == "tags_tab":
            selected_rows = self.tags_tab_table.get_selected_rows()
            selected_tags = [tag[0] for tag in selected_rows]
            self.use_cases.delete_tags(selected_tags)
            self.tags_tab_table.delete_selection()
        
        elif current_tab_name == "filters_tab":
            selected_rows = self.filters_tab_table.get_selected_rows()
            selected_filters = [fast_filter[0] for fast_filter in selected_rows]
            self.use_cases.delete_filters(selected_filters)
            self.filters_tab_table.delete_selection()
        
        else:
            self.display_error_message_box("Unknown tab")

        self.update_notes_tab_accordion()
        self.notes_accordion_buttons_enabling()



    def _get_selected_note(self):
        """
        Gets all information about the currently selected note
        """

        if self.is_table_view:
            selected_notes = self.notes_tab_table.get_selected_rows()
            if len(selected_notes) != 1:
                return None
            return self.use_cases.find_detailed_note_by_name(selected_notes[0][0])
        else:
            selected_notes = self.notes_tab_accordion.get_selected_notes()
            if len(selected_notes) != 1:
                return None
            return selected_notes[0]



    def _get_selected_category(self):
        """
        Gets all information about the currently selected category
        """

        selected_categories = self.categories_tab_table.get_selected_rows()
        if len(selected_categories) != 1:
            return None
        return self.use_cases.find_category_by_name(selected_categories[0][0])



    def _get_selected_tag(self):
        """
        Gets all information about the currently selected tag
        """

        selected_tags = self.tags_tab_table.get_selected_rows()
        if len(selected_tags) != 1:
            return None
        return self.use_cases.find_tag_by_name(selected_tags[0][0])



    def _get_selected_filter(self):
        """
        Gets all information about the currently selected filter
        """

        selected_filters = self.filters_tab_table.get_selected_rows()
        if len(selected_filters) != 1:
            return None
        return self.use_cases.find_filter_by_name(selected_filters[0][0])



    @QtCore.Slot()
    def change_notes_tab_accordion_page(self):
        """
        Changes the page of the accordion widget
        """

        self.grid_page = self.notes_tab_accordion_pagination.current_page
        self.update_notes_tab_accordion()
        selected_rows_count = self.count_selected_notes()
        self.edit_icon_button.setEnabled(selected_rows_count == 1)
        self.delete_icon_button.setEnabled(selected_rows_count >= 1)


    def update_notes_tab_accordion(self):
        """
        Updates the displayed notes in the accordion widget
        """

        self.grid_notes = [note for note in self.use_cases.get_filtered_notes_paged(self.current_note_filter, page=self.grid_page, size=10)]
        self.notes_tab_accordion.replace_sections(self.grid_notes)

        index = self.notes_tab_table.currentIndex()
        self.notes_tab_accordion_pagination.items_count = self.notes_tab_table.model.rowCount(index)
        self.notes_tab_accordion_pagination.create_labels()


    @QtCore.Slot()
    def _set_basic_text_filtering(self, model, searchbar):
        """
        Filters table items by their name

        :param model: Model on which will the filter be used
        :param searchbar: Searchbar widget with filter text
        """

        if self.tabs.currentWidget().objectName() == "notes_tab":
            self.current_note_filter = self.create_default_filter()
            self.current_note_filter.note_name = searchbar.text()
            self.use_current_note_filter()
        model.setFilterFixedString(searchbar.text())



    def create_default_filter(self):
        """
        Creates object with default filter values

        :return: Object with default filter values
        """

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



def run_application():
    """
    Runs the application with the PySide gui

    :return: Gui number of the next library
    """

    # Application is created the first time
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication([])
    else:
        app = QtWidgets.QApplication.instance()

    stylesheet_path = pathlib.Path(__file__).parent / "style.qss"

    # Connect the stylesheet to the application
    stylesheet = stylesheet_path.resolve().as_posix()
    with open(stylesheet, "r") as f:
        app.setStyleSheet(f.read())

    # Create and customize the main widget
    use_cases = UseCases.UseCases()
    widget = MainWindow(use_cases)
    widget.setWindowTitle("PySideApplication")
    widget.resize(1280, 640)
    widget.setMinimumSize(1280, 640)
    widget.setMaximumSize(1280, 640)
    widget.show()
    app.exec()

    return widget.gui
    

if __name__ == "__main__":
    run_application()

