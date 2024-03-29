import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"

import platform

from kivy import app, lang, metrics
from kivy.core import window
from kivy.uix import boxlayout, button, image, label, popup, tabbedpanel

from kivymd import app

from datetime import datetime

import pathlib

from BusinessLogic import UseCases

from KivyApp import styled_widgets
from KivyApp.widgets import loading_bar, notes_accordion, pagination_labels, searchbar_with_icon, todays_notes_recycleview



class KivyApplicationLayout(boxlayout.BoxLayout):
    def __init__(self, use_cases, *args, **kwargs):
        """
        Initializes the main window layout with all its contents

        :param use_cases: Class containing methods that retrieve data for the application
        """

        super(KivyApplicationLayout, self).__init__(*args, **kwargs)

        # Constant representing which gui is used 2 == Kivy
        self.gui = 2

        self.padding = (2, 2)

        self.use_cases = use_cases

        # Get data from database for tables and accordion
        self.current_note_filter = self.create_default_filter()
        self.grid_page = 1
        self.grid_notes = [note for note in self.use_cases.get_filtered_notes_paged(self.current_note_filter, page=self.grid_page, size=10)]

        use_cases_notes = [note for note in self.use_cases.get_notes()]
        self.table_notes = [(note.name, note.priority, note.time.strftime("%d/%m/%Y %H:%M"), note.text) for note in use_cases_notes]
        self.today_notes = [(note.time.strftime("%H:%M"), note.name) for note in use_cases_notes if note.time.date() == datetime.today().date()]
        self.today_notes.sort(key = lambda note: note[0])

        self.table_tags = [(tag.name, tag.description) for tag in self.use_cases.get_tags()]

        self.table_categories = [(category.name, category.description) for category in self.use_cases.get_categories()]

        self.table_filters = [(note_filter.name,
                               note_filter.order,
                               note_filter.note_name,
                               note_filter.category_name) for note_filter in self.use_cases.get_filters()]

        # Toolbar layout on top
        self.toolbar_layout = styled_widgets.ToolbarLayout()
        self._init_toolbar_layout()

        # Todays notes layout
        self.todays_notes_layout = styled_widgets.TodaysNotesLayout()
        self._init_todays_notes_layout()

        # Content layout
        self.tabs_content_layout = styled_widgets.TabsContentLayout()
        self._init_tabs_content_layout()

        # Todays notes and content below toolbar
        todays_notes_and_content_layout = boxlayout.BoxLayout(orientation="horizontal", size_hint=(1, 14/15))
        todays_notes_and_content_layout.add_widget(self.todays_notes_layout)
        todays_notes_and_content_layout.add_widget(self.tabs_content_layout)
        
        # 15 rows : 8 columns
        self.add_widget(self.toolbar_layout)
        self.add_widget(todays_notes_and_content_layout)



    def _init_toolbar_layout(self):
        """
        Initializes widgets in the toolbar
        """

        image_dir_path = pathlib.Path(__file__).parent.parent / "Images"

        # Today's notes icon button
        todays_notes_icon_path = image_dir_path / "TodaysNotesIcon.png"
        self.todays_notes_icon_button = styled_widgets.TodaysNotesButton(on_release=self.toggle_todays_notes_pane)
        todays_notes_icon = image.Image(source = todays_notes_icon_path.resolve().as_posix(), size_hint=(1, 3/5))

        todays_notes_button_layout = boxlayout.BoxLayout(size_hint=(4/32, 1), orientation="vertical")
        todays_notes_button_layout.add_widget(todays_notes_icon)
        todays_notes_button_layout.add_widget(self.todays_notes_icon_button)

        self.toolbar_layout.add_widget(todays_notes_button_layout)
        self.todays_notes_pane_visible = True

        # Use fast filter section
        self.toolbar_layout.add_widget(styled_widgets.FastFilterLabel())

        self.fast_filters_text_links = [styled_widgets.FastFilterRefLabel(text="[ref=1]#1[/ref]"),
                                        styled_widgets.FastFilterRefLabel(text="[ref=2]#2[/ref]"),
                                        styled_widgets.FastFilterRefLabel(text="[ref=3]#3[/ref]")]
        for order, fast_filter_text_link in enumerate(self.fast_filters_text_links):
            self.toolbar_layout.add_widget(fast_filter_text_link)
            fast_filter_text_link.bind(on_ref_press=lambda _, o=order: self.use_fast_filter(int(o)+1))

        # Time widget
        self.time_widget = styled_widgets.TimeLabel()
        self.toolbar_layout.add_widget(self.time_widget)

        # Add icon button
        add_icon_path = image_dir_path / "AddIcon.png"
        self.add_icon_button = styled_widgets.ToolbarButton(background_image = add_icon_path.resolve().as_posix(), on_release=self.add_item)
        add_icon_box = styled_widgets.ToolbarButtonBox()
        add_icon_box.add_widget(self.add_icon_button)
        self.toolbar_layout.add_widget(add_icon_box)

        # Edit icon button
        edit_icon_path = image_dir_path / "EditIcon.png"
        self.edit_icon_button = styled_widgets.ToolbarButton(background_image = edit_icon_path.resolve().as_posix(), disabled=True, on_release=self.edit_item)
        edit_icon_box = styled_widgets.ToolbarButtonBox()
        edit_icon_box.add_widget(self.edit_icon_button)
        self.toolbar_layout.add_widget(edit_icon_box)

        # Delete icon button
        delete_icon_path = image_dir_path / "DeleteIcon.png"
        self.delete_icon_button = styled_widgets.ToolbarButton(background_image = delete_icon_path.resolve().as_posix(), disabled=True, on_release=self.delete_items)
        delete_icon_box = styled_widgets.ToolbarButtonBox()
        delete_icon_box.add_widget(self.delete_icon_button)
        self.toolbar_layout.add_widget(delete_icon_box)

        # Loading bar
        self.loading_bar = loading_bar.LoadingBar(size_hint=(5/32, 1))
        self.toolbar_layout.add_widget(self.loading_bar)

        # Settings icon button
        settings_icon_path = image_dir_path / "SettingsIcon.png"
        self.settings_icon_button = styled_widgets.ToolbarButton(background_image = settings_icon_path.resolve().as_posix(), on_release=self.change_library)
        settings_icon_box = styled_widgets.ToolbarButtonBox()
        settings_icon_box.add_widget(self.settings_icon_button)
        self.toolbar_layout.add_widget(settings_icon_box)



    def change_library(self, button_instance):
        """
        Changes the used gui library of the application

        :param button_instance: Button causing this method
        """

        dialog = styled_widgets.SettingsDialog()
        dialog.bind(on_dismiss=self._settings_dialog_closed)
        dialog.open()


    def _settings_dialog_closed(self, dialog):
        """
        Handles closed settings dialog by changing the gui library

        :param dialog: Closed dialog
        """

        if dialog.accepted:
            self.gui = dialog.data_dict["library"]
            if self.gui == 2:
                return
            app.MDApp.get_running_app().stop()



    def toggle_todays_notes_pane(self, button_instance):
        """
        Toggles the visibility of todays notes pane

        :param button_instance: Button causing this method
        """

        w = self.todays_notes_layout

        # Hide todays notes pane
        if self.todays_notes_pane_visible:
            w.saved_attrs = w.height, w.width, w.size_hint_x, w.size_hint_y, w.opacity, w.disabled
            w.height, w.width, w.size_hint_x, w.size_hint_y, w.opacity, w.disabled = 0, 0, None, None, 0, True
            self.tabs_content_layout.size_hint = 1, 1
        # Show todays notes pane
        else:
            w.height, w.width, w.size_hint_x, w.size_hint_y, w.opacity, w.disabled = w.saved_attrs
            del w.saved_attrs
            self.tabs_content_layout.size_hint = 7/8, 1
        self.todays_notes_pane_visible = not self.todays_notes_pane_visible



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

        # Todays notes header label
        self.todays_notes_header = styled_widgets.TodaysNotesLabel()
        self.todays_notes_layout.add_widget(self.todays_notes_header)

        # List of todays notes
        # Comparison construct
        self.todays_notes_recycleview = todays_notes_recycleview.TodaysNotesRecycleview(self.today_notes)
        self.todays_notes_layout.add_widget(self.todays_notes_recycleview)


    def remove_notes_from_todays_notes(self, notes):
        """
        Removes notes from todays notes pane

        :param notes: Notes to remove from todays notes pane
        """

        todays_notes = self.todays_notes_recycleview.data
        for note in notes:
            index = [i for i, v in enumerate(todays_notes) if v["name"] == note]
            if index:
                del todays_notes[index[0]]


    def add_note_to_todays_notes(self, note):
        """
        Adds note to todays notes pane

        :param note: Note to add to todays notes pane
        """

        note_dict = {"time": note.time.strftime("%H:%M"), "name": note.name}
        for i, val in enumerate(self.todays_notes_recycleview.data):
            if val["time"] > note_dict["time"]:
                self.todays_notes_recycleview.data.insert(i, note_dict)
                return

        self.todays_notes_recycleview.data.append(note_dict)


    def _init_tabs_content_layout(self):
        """
        Initializes tabs widget
        """

        self.tabs = styled_widgets.NotesTabbedPanel()
        self.tabs._tab_layout.padding = "2dp", "2dp", "2dp", "-2dp"

        # Specific tabs
        self.notes_tab = styled_widgets.NotesTabbedPanelItem(text="Notes")
        self._init_notes_tab()
        self.categories_tab = styled_widgets.NotesTabbedPanelItem(text="Categories")
        self._init_categories_tab()
        self.tags_tab = styled_widgets.NotesTabbedPanelItem(text="Tags")
        self._init_tags_tab()
        self.filters_tab = styled_widgets.NotesTabbedPanelItem(text="Fast filters")
        self._init_filters_tab()

        # Adding initialized tabs
        self.tabs.add_widget(self.notes_tab)
        self.tabs.add_widget(self.categories_tab)
        self.tabs.add_widget(self.tags_tab)
        self.tabs.add_widget(self.filters_tab)
        self.tabs.bind(current_tab=self.tab_update_buttons_enabling)

        self.tabs_content_layout.add_widget(self.tabs)



    def _init_notes_tab(self):
        """
        Initializes widgets in the notes tab
        """

        self.notes_tab_searchbar = styled_widgets.SearchBarWithIcon()
        self.notes_filter_button = button.Button(text="Filter", size_hint=(1/8, 1), on_release=self._filter_items_by_name)
        self.notes_advanced_filter_button = button.Button(text="Advanced filter", size_hint=(1/8, 1), on_release=self.notes_advanced_filtering)
        
        self.notes_toggle_switch_label = label.Label(text="Table view", size_hint=(1/8, 1), color="black", halign="right", valign="center")
        self.notes_toggle_switch_label.bind(size=self.notes_toggle_switch_label.setter("text_size"))
        self.notes_toggle_switch_button = styled_widgets.NotesToggleSwitch()
        self.notes_toggle_switch_button.bind(active=self.toggle_notes_view)

        self.notes_tab_toolbar_layout = styled_widgets.TabToolbarLayout()
        self.notes_tab_toolbar_layout.add_widget(self.notes_tab_searchbar)
        self.notes_tab_toolbar_layout.add_widget(self.notes_filter_button)
        self.notes_tab_toolbar_layout.add_widget(self.notes_advanced_filter_button)
        self.notes_tab_toolbar_layout.add_widget(self.notes_toggle_switch_label)
        self.notes_tab_toolbar_layout.add_widget(self.notes_toggle_switch_button)

        self.notes_tab_table = styled_widgets.CustomMDDataTable(
            check=True,
            elevation=0,
            size_hint=(1, 33/36),
            rows_num=100000,
            column_data=[
                ("Name", metrics.dp(60), lambda data: zip(*sorted(enumerate(data), key=lambda x:x[1][0]))),
                ("Priority", metrics.dp(30), lambda data: zip(*sorted(enumerate(data), key=lambda x:x[1][1]))),
                ("Time", metrics.dp(40), lambda data: zip(*sorted(enumerate(data), key=lambda x:x[1][2]))),
                ("Text", metrics.dp(95), lambda data: zip(*sorted(enumerate(data), key=lambda x:x[1][3])))
            ],
            row_data=self.table_notes
        )
        self.notes_tab_table.bind(on_row_press=self.table_update_buttons_enabling)

        # Accordion with pagination
        self.notes_tab_accordion = notes_accordion.NotesAccordionBox(
            self.grid_notes,
            self.notes_accordion_buttons_enabling,
            size_hint=(1, 32/36)
        )
        self.notes_tab_accordion_pagination = styled_widgets.PaginationLabels(10, len(self.notes_tab_table.row_data))
        self.notes_tab_accordion_pagination.bind(on_page_changed=self.change_notes_tab_accordion_page)

        self.notes_tab_layout = styled_widgets.NotesTabLayout()
        self.notes_tab_layout.add_widget(self.notes_tab_toolbar_layout)
        self.notes_tab_layout.add_widget(self.notes_tab_accordion)
        self.notes_tab_layout.add_widget(self.notes_tab_accordion_pagination)
        self._save_accordion_attrs()
        self.notes_tab_layout.add_widget(self.notes_tab_table)

        self.notes_tab.add_widget(self.notes_tab_layout)

        self.is_table_view = True


    def notes_advanced_filtering(self, button_instance):
        """
        Opens advanced filter dialog

        :param button_instance: Button causing this method
        """

        self.loading_bar.start()
        dialog = styled_widgets.AdvancedFilterDialog()
        dialog.bind(on_dismiss=self._notes_advanced_filtering_dialog_closed)
        dialog.open()


    def _notes_advanced_filtering_dialog_closed(self, dialog):
        """
        Filters notes based on dialog values

        :param dialog: Dialog from which are the values taken
        """

        if dialog.accepted:
            filters = lambda: None
            filters.note_name = dialog.data_dict["note_name"]
            filters.note_min_priority = dialog.data_dict["note_min_priority"]
            filters.note_max_priority = dialog.data_dict["note_max_priority"]
            filters.note_min_time = dialog.data_dict["note_from_date"]
            filters.note_max_time = dialog.data_dict["note_to_date"]
            filters.note_text = dialog.data_dict["note_text"]
            filters.category_name = dialog.data_dict["category_name"]
            filters.category_description = dialog.data_dict["category_description"]
            filters.tag_name = dialog.data_dict["tag_name"]
            filters.tag_description = dialog.data_dict["tag_description"]

            self.current_note_filter = filters
            self.use_current_note_filter()
        self.loading_bar.stop()


    
    def use_current_note_filter(self):
        """
        Filters notes based on the currently saved filter
        """

        self.grid_page = self.notes_tab_accordion_pagination.current_page = 1
        filtered_notes = self.use_cases.get_filtered_notes(self.current_note_filter)
        self.table_notes = [(note.name, note.priority, note.time.strftime("%d/%m/%Y %H:%M"), note.text) for note in filtered_notes]

        self.notes_tab_table.update_table_data(self.notes_tab_table.table_data, list(set(self.table_notes)))
        self.update_notes_tab_accordion()


    def _save_accordion_attrs(self):
        """
        Saves accordion attributes to make visibility toggling possible
        """

        acc = self.notes_tab_accordion
        acc.saved_attrs = acc.height, acc.width, acc.size_hint_x, acc.size_hint_y, acc.opacity, acc.disabled
        acc.height, acc.width, acc.size_hint_x, acc.size_hint_y, acc.opacity, acc.disabled = 0, 0, None, None, 0, True
        
        pag = self.notes_tab_accordion_pagination
        pag.saved_attrs = pag.height, pag.width, pag.size_hint_x, pag.size_hint_y, pag.opacity, pag.disabled
        pag.height, pag.width, pag.size_hint_x, pag.size_hint_y, pag.opacity, pag.disabled = 0, 0, None, None, 0, True



    def toggle_notes_view(self, switch, value):
        """
        Toggles visibitlity of table and accordion based on the toggle state

        :param switch: Toggle button causing this method
        :param value: State value of toggle button
        """

        acc = self.notes_tab_accordion
        pag = self.notes_tab_accordion_pagination
        tab = self.notes_tab_table

        # Hide accordion and show table
        if self.is_table_view:
            tab.saved_attrs = tab.height, tab.width, tab.size_hint_x, tab.size_hint_y, tab.opacity, tab.disabled
            tab.height, tab.width, tab.size_hint_x, tab.size_hint_y, tab.opacity, tab.disabled = 0, 0, None, None, 0, True
            acc.height, acc.width, acc.size_hint_x, acc.size_hint_y, acc.opacity, acc.disabled = acc.saved_attrs
            del acc.saved_attrs

            pag.height, pag.width, pag.size_hint_x, pag.size_hint_y, pag.opacity, pag.disabled = pag.saved_attrs
            del pag.saved_attrs
            selected_rows_count = self.count_selected_notes()
        # Hide table and show accordion
        else:
            acc.saved_attrs = acc.height, acc.width, acc.size_hint_x, acc.size_hint_y, acc.opacity, acc.disabled
            acc.height, acc.width, acc.size_hint_x, acc.size_hint_y, acc.opacity, acc.disabled = 0, 0, None, None, 0, True

            pag.saved_attrs = pag.height, pag.width, pag.size_hint_x, pag.size_hint_y, pag.opacity, pag.disabled
            pag.height, pag.width, pag.size_hint_x, pag.size_hint_y, pag.opacity, pag.disabled = 0, 0, None, None, 0, True

            tab.height, tab.width, tab.size_hint_x, tab.size_hint_y, tab.opacity, tab.disabled = tab.saved_attrs
            del tab.saved_attrs

            selected_rows_count = len(self.notes_tab_table.selected_rows)

        self.edit_icon_button.disabled = selected_rows_count != 1
        self.delete_icon_button.disabled = selected_rows_count < 1
        self.is_table_view = not self.is_table_view



    def _init_categories_tab(self):
        """
        Initializes widgets in the categories tab
        """

        self.categories_tab_searchbar = searchbar_with_icon.SearchBarWithIcon(size_hint=(4/8, 1))
        self.categories_filter_button = button.Button(text="Filter", size_hint=(1/8, 1),  on_release=self._filter_items_by_name)

        self.categories_tab_toolbar_layout = styled_widgets.TabToolbarLayout()
        self.categories_tab_toolbar_layout.add_widget(self.categories_tab_searchbar)
        self.categories_tab_toolbar_layout.add_widget(self.categories_filter_button)
        self.categories_tab_toolbar_layout.add_widget(label.Label(size_hint=(3/8, 1)))

        self.categories_tab_table = styled_widgets.CustomMDDataTable(
            check=True,
            elevation=0,
            size_hint=(1, 33/36),
            rows_num=100000,
            column_data=[
                ("Name", metrics.dp(80), lambda data: zip(*sorted(enumerate(data), key=lambda x:x[1][0]))),
                ("Description", metrics.dp(145), lambda data: zip(*sorted(enumerate(data), key=lambda x:x[1][1]))),
            ],
            row_data=self.table_categories
        )
        self.categories_tab_table.bind(on_row_press=self.table_update_buttons_enabling)

        self.categories_tab_layout = boxlayout.BoxLayout(orientation="vertical", size_hint=(1, 1))
        self.categories_tab_layout.add_widget(self.categories_tab_toolbar_layout)
        self.categories_tab_layout.add_widget(self.categories_tab_table)

        self.categories_tab.add_widget(self.categories_tab_layout)



    def _init_tags_tab(self):
        """
        Initializes widgets in the tags tab
        """

        self.tags_tab_searchbar = searchbar_with_icon.SearchBarWithIcon(size_hint=(4/8, 1))
        self.tags_filter_button = button.Button(text="Filter", size_hint=(1/8, 1), on_release=self._filter_items_by_name)

        self.tags_tab_toolbar_layout = styled_widgets.TabToolbarLayout()
        self.tags_tab_toolbar_layout.add_widget(self.tags_tab_searchbar)
        self.tags_tab_toolbar_layout.add_widget(self.tags_filter_button)
        self.tags_tab_toolbar_layout.add_widget(label.Label(size_hint=(3/8, 1)))

        self.tags_tab_table = styled_widgets.CustomMDDataTable(
            check=True,
            elevation=0,
            size_hint=(1, 33/36),
            rows_num=100000,
            column_data=[
                ("Name", metrics.dp(80), lambda data: zip(*sorted(enumerate(data), key=lambda x:x[1][0]))),
                ("Description", metrics.dp(145), lambda data: zip(*sorted(enumerate(data), key=lambda x:x[1][1]))),
            ],
            row_data=self.table_tags
        )
        self.tags_tab_table.bind(on_row_press=self.table_update_buttons_enabling)

        self.tags_tab_layout = boxlayout.BoxLayout(orientation="vertical", size_hint=(1, 1))
        self.tags_tab_layout.add_widget(self.tags_tab_toolbar_layout)
        self.tags_tab_layout.add_widget(self.tags_tab_table)

        self.tags_tab.add_widget(self.tags_tab_layout)



    def _init_filters_tab(self):
        """
        Initializes widgets in the filters tab
        """

        self.filters_tab_searchbar = searchbar_with_icon.SearchBarWithIcon(size_hint=(4/8, 1))
        self.filters_filter_button = button.Button(text="Filter", size_hint=(1/8, 1), on_release=self._filter_items_by_name)

        self.filters_tab_toolbar_layout = styled_widgets.TabToolbarLayout()
        self.filters_tab_toolbar_layout.add_widget(self.filters_tab_searchbar)
        self.filters_tab_toolbar_layout.add_widget(self.filters_filter_button)
        self.filters_tab_toolbar_layout.add_widget(label.Label(size_hint=(3/8, 1)))

        self.filters_tab_table = styled_widgets.CustomMDDataTable(
            check=True,
            elevation=0,
            size_hint=(1, 33/36),
            rows_num=100000,
            column_data=[
                ("Name", metrics.dp(60), lambda data: zip(*sorted(enumerate(data), key=lambda x:x[1][0]))),
                ("Order", metrics.dp(25), lambda data: zip(*sorted(enumerate(data), key=lambda x:x[1][1]))),
                ("Note name", metrics.dp(60), lambda data: zip(*sorted(enumerate(data), key=lambda x:x[1][2]))),
                ("Category name", metrics.dp(80), lambda data: zip(*sorted(enumerate(data), key=lambda x:x[1][3]))),
            ],
            row_data=self.table_filters
        )
        self.filters_tab_table.bind(on_row_press=self.table_update_buttons_enabling)


        self.filters_tab_layout = boxlayout.BoxLayout(orientation="vertical", size_hint=(1, 1))
        self.filters_tab_layout.add_widget(self.filters_tab_toolbar_layout)
        self.filters_tab_layout.add_widget(self.filters_tab_table)

        self.filters_tab.add_widget(self.filters_tab_layout)


    def tab_update_buttons_enabling(self, instance, value):
        """
        Updates buttons state based on the count of currently selected rows

        :param instance: Widget instance causing this method
        :param value: State value of the widget instance
        """

        current_tab_name = self.tabs.current_tab.text
        if current_tab_name == "Notes":
            if self.is_table_view:
                selected_rows_count = len(self.notes_tab_table.selected_rows)
            else:
                selected_rows_count = self.count_selected_notes()
        elif current_tab_name == "Categories":
            selected_rows_count = len(self.categories_tab_table.selected_rows)
        elif current_tab_name == "Tags":
            selected_rows_count = len(self.tags_tab_table.selected_rows)
        elif current_tab_name == "Fast filters":
            selected_rows_count = len(self.filters_tab_table.selected_rows)
        else:
            self.edit_icon_button.disabled = True
            self.delete_icon_button.disabled = True
        self.edit_icon_button.disabled = selected_rows_count != 1
        self.delete_icon_button.disabled = selected_rows_count < 1


    def count_selected_notes(self):
        """
        Counts number of selected rows in the accordion

        :return: Number of selected rows in the accordion
        """

        return len(self.notes_tab_accordion.get_selected_notes())


    def table_update_buttons_enabling(self, table_instance, row_instance):
        """
        Updates buttons state based on the count of currently selected rows in current tabs table

        :table_instance: Current tabs table
        :row_instance: Clicked row
        """

        selected_rows_count = len(table_instance.selected_rows)
        self.edit_icon_button.disabled = selected_rows_count != 1
        self.delete_icon_button.disabled = selected_rows_count < 1
        


    def notes_accordion_buttons_enabling(self):
        """
        Updates buttons state based on the count of currently selected rows in accordion
        """

        if self.tabs.current_tab.text == "Notes" and not self.is_table_view:
            selected_notes_count = self.count_selected_notes()
            self.edit_icon_button.disabled = selected_notes_count != 1
            self.delete_icon_button.disabled = selected_notes_count < 1


    # Operations on items

    def add_item(self, instance):
        """
        Adds item
        """
        self.loading_bar.start()
        self.item_action("ADD")


    def edit_item(self, instance):
        """
        Edits item
        """
        self.loading_bar.start()
        self.item_action("EDIT")


    def item_action(self, action_name):
        """
        Takes action on item

        :param action_name: EDIT or ADD action to be taken on item
        """

        current_tab_name = self.tabs.current_tab.text
        if current_tab_name == "Notes":
            if action_name == "EDIT":
                self._edit_note()
            elif action_name == "ADD":
                self._add_note()

        elif current_tab_name == "Categories":
            if action_name == "EDIT":
                self._edit_category()
            elif action_name == "ADD":
                self._add_category()

        elif current_tab_name == "Tags":
            if action_name == "EDIT":
                self._edit_tag()
            elif action_name == "ADD":
                self._add_tag()

        elif current_tab_name == "Fast filters":
            if action_name == "EDIT":
                self._edit_filter()

            elif action_name == "ADD":
                self._add_filter()
        else:
            self.display_error_message_box("Unknown tab")



    def display_error_message_box(self, text):
        """
        Displays error message box

        :param text: Message of error message box
        """

        message_box = popup.Popup(
            title=text,
            content=button.Button(text="Close", size_hint=(1/2, 1/2)),
            size_hint=(1/3, 1/4)
        )
        message_box.content.bind(on_press=message_box.dismiss)
        message_box.open()



    # CRUD operations for all items

    def _add_note(self):
        """
        Opens new note dialog
        """

        categories_names = [category.name for category in self.use_cases.get_categories()]
        tags_names = [tag.name for tag in self.use_cases.get_tags()]

        dialog = styled_widgets.NoteDialog(categories_names, tags_names)
        dialog.bind(on_dismiss=self._add_note_dialog_closed)
        dialog.open()


    def _add_note_dialog_closed(self, dialog):
        """
        Creates note based on the dialog values

        :param dialog: Dialog from which are the values taken
        """

        if dialog.accepted:
            new_note = lambda: None
            new_note.name = dialog.data_dict["name"]
            new_note.time = dialog.data_dict["time"]
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
            self.update_notes_tab_accordion()
        self.loading_bar.stop()

    
    def _edit_note(self):
        """
        Opens edit dialog for selected note
        """

        categories_names = [category.name for category in self.use_cases.get_categories()]
        tags_names = [tag.name for tag in self.use_cases.get_tags()]
        selected_note = self._get_selected_note()

        dialog = styled_widgets.NoteDialog(categories_names, tags_names)
        dialog.fill_dialog(selected_note)
        dialog.bind(on_dismiss=self._edit_note_dialog_closed)
        dialog.open()


    def _edit_note_dialog_closed(self, dialog):
        """
        Edits note based on the dialog values

        :param dialog: Dialog from which are the values taken
        """

        selected_note = self._get_selected_note()
        if dialog.accepted:
            updated_note = lambda: None
            updated_note.name = dialog.data_dict["name"]
            updated_note.time = dialog.data_dict["time"]
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
                    self.notes_tab_table.update_row(old_note_row, new_note_row)
            else:
                self.display_error_message_box(f"Note with name={updated_note.name} already exists")
            self.update_notes_tab_accordion()
        self.loading_bar.stop()



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

        dialog = styled_widgets.CategoryDialog()
        dialog.bind(on_dismiss=self._add_category_dialog_closed)
        dialog.open()


    def _add_category_dialog_closed(self, dialog):
        """
        Creates category based on the dialog values

        :param dialog: Dialog from which are the values taken
        """
        
        if dialog.accepted:
            new_category = lambda: None
            new_category.name = dialog.data_dict["name"]
            new_category.description = dialog.data_dict["description"]
            if self.use_cases.create_category(new_category):
                new_category_row = (new_category.name, new_category.description)
                self.categories_tab_table.add_row(new_category_row)
            else:
                self.display_error_message_box(f"Category with name={new_category.name} already exists")
            self.update_notes_tab_accordion()
        self.loading_bar.stop()


    def _edit_category(self):
        """
        Opens edit dialog for selected category
        """

        selected_category = self._get_selected_category()
        if selected_category.name == "Default":
            return

        dialog = styled_widgets.CategoryDialog()
        dialog.fill_dialog(selected_category)
        dialog.bind(on_dismiss=self._edit_category_dialog_closed)
        dialog.open()


    def _edit_category_dialog_closed(self, dialog):
        """
        Edits category based on the dialog values

        :param dialog: Dialog from which are the values taken
        """
        
        selected_category = self._get_selected_category()
        if dialog.accepted:
            updated_category = lambda: None
            updated_category.name = dialog.data_dict["name"]
            updated_category.description = dialog.data_dict["description"]
            if self.use_cases.update_category(selected_category.id, updated_category):
                old_category = tuple(self.categories_tab_table.selected_rows[0])
                new_category = (updated_category.name, updated_category.description)
                self.categories_tab_table.update_row(old_category, new_category)
            else:
                self.display_error_message_box(f"Category with name={updated_category.name} already exists")
            self.update_notes_tab_accordion()
        self.loading_bar.stop()



    def _add_tag(self):
        """
        Opens new tag dialog
        """

        dialog = styled_widgets.TagDialog()
        dialog.bind(on_dismiss=self._add_tag_dialog_closed)
        dialog.open()


    def _add_tag_dialog_closed(self, dialog):
        """
        Creates tag based on the dialog values

        :param dialog: Dialog from which are the values taken
        """

        if dialog.accepted:
            new_tag = lambda: None
            new_tag.name = dialog.data_dict["name"]
            new_tag.description = dialog.data_dict["description"]
            if self.use_cases.create_tag(new_tag):
                new_tag_row = (new_tag.name, new_tag.description)
                self.tags_tab_table.add_row(new_tag_row)
            else:
                self.display_error_message_box(f"Tag with name={new_tag.name} already exists")
            self.update_notes_tab_accordion()
        self.loading_bar.stop()


    def _edit_tag(self):
        """
        Opens edit dialog for selected tag
        """

        selected_tag = self._get_selected_tag()
        
        dialog = styled_widgets.TagDialog()
        dialog.fill_dialog(selected_tag)
        dialog.bind(on_dismiss=self._edit_tag_dialog_closed)
        dialog.open()


    def _edit_tag_dialog_closed(self, dialog):
        """
        Edits tag based on the dialog values

        :param dialog: Dialog from which are the values taken
        """
        
        selected_tag = self._get_selected_tag()
        if dialog.accepted:
            updated_tag = lambda: None
            updated_tag.name = dialog.data_dict["name"]
            updated_tag.description = dialog.data_dict["description"]
            if self.use_cases.update_tag(selected_tag.id, updated_tag):
                old_tag = tuple(self.tags_tab_table.selected_rows[0])
                new_tag = (updated_tag.name, updated_tag.description)
                self.tags_tab_table.update_row(old_tag, new_tag)
            else:
                self.display_error_message_box(f"Tag with name={updated_tag.name} already exists")
            self.update_notes_tab_accordion()
        self.loading_bar.stop()


    def _add_filter(self):
        """
        Opens new filter dialog
        """

        dialog = styled_widgets.FilterDialog()
        dialog.bind(on_dismiss=self._add_filter_dialog_closed)
        dialog.open()


    def _add_filter_dialog_closed(self, dialog):
        """
        Creates filter based on the dialog values

        :param dialog: Dialog from which are the values taken
        """
        
        if dialog.accepted:
            new_filter = lambda: None
            new_filter.name = dialog.data_dict["name"]
            new_filter.note_name = dialog.data_dict["note_name"]
            new_filter.note_min_priority = dialog.data_dict["note_min_priority"]
            new_filter.note_max_priority = dialog.data_dict["note_max_priority"]
            new_filter.note_min_time = dialog.data_dict["note_from_time"]
            new_filter.note_max_time = dialog.data_dict["note_to_time"]
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

                for i, row in enumerate(table_rows):
                    new_row = row[0], -1, row[2], row[3]
                    self.filters_tab_table.update_row(row, new_row)
            else:
                self.display_error_message_box(f"Fast filter with name={new_filter.name} already exists")
            self.update_notes_tab_accordion()
        self.loading_bar.stop()



    def _edit_filter(self):
        """
        Opens edit dialog for selected filter
        """

        selected_filter = self._get_selected_filter()

        dialog = styled_widgets.FilterDialog()
        dialog.fill_dialog(selected_filter)
        dialog.bind(on_dismiss=self._edit_filter_dialog_closed)
        dialog.open()


    def _edit_filter_dialog_closed(self, dialog):
        """
        Edits filter based on the dialog values

        :param dialog: Dialog from which are the values taken
        """
        
        selected_filter = self._get_selected_filter()

        if dialog.accepted:
            updated_filter = lambda: None
            updated_filter.name = dialog.data_dict["name"]
            updated_filter.note_name = dialog.data_dict["note_name"]
            updated_filter.note_min_priority = dialog.data_dict["note_min_priority"]
            updated_filter.note_max_priority = dialog.data_dict["note_max_priority"]
            updated_filter.note_min_time = dialog.data_dict["note_from_time"]
            updated_filter.note_max_time = dialog.data_dict["note_to_time"]
            updated_filter.note_text = dialog.data_dict["note_text"]
            updated_filter.tag_name = dialog.data_dict["tag_name"]
            updated_filter.tag_description = dialog.data_dict["tag_description"]
            updated_filter.category_name = dialog.data_dict["category_name"]
            updated_filter.category_description = dialog.data_dict["category_description"]
            updated_filter.order = dialog.data_dict["order"]

            ordered_filters = [fast_filter for fast_filter in self.use_cases.find_filter_by_order_listed(updated_filter.order)]

            if self.use_cases.update_filter(selected_filter.id, updated_filter):
                old_filter = (selected_filter.name,
                              selected_filter.order,
                              selected_filter.note_name,
                              selected_filter.category_name)
                new_filter = (updated_filter.name,
                              updated_filter.order,
                              updated_filter.note_name,
                              updated_filter.category_name)
                self.filters_tab_table.update_row(old_filter, new_filter)

                table_rows = [(row.name,
                               row.order,
                               row.note_name,
                               row.category_name) for row in ordered_filters if row.name != updated_filter.name]
                for row in table_rows:
                    new_row = (row[0], -1, row[2], row[3])
                    self.filters_tab_table.update_row(row, new_row)

                self.edit_icon_button.disabled = True
                self.delete_icon_button.disabled = True
            else:
                self.display_error_message_box(f"Fast filter with name={updated_filter.name} already exists")
            self.update_notes_tab_accordion()
        self.loading_bar.stop()


    def delete_items(self, button_instance):
        """
        Deletes currently selected items
        """

        current_tab_name = self.tabs.current_tab.text
        if current_tab_name == "Notes":
            if self.is_table_view:
                selected_rows = self.notes_tab_table.selected_rows
                selected_notes = [note[0] for note in selected_rows]
                self.notes_tab_table.delete_selection()
            else:
                selected_rows = self.notes_tab_accordion.get_selected_notes()
                selected_notes = [note.name for note in selected_rows]
                table_rows = [(note.name, note.priority, note.time.strftime("%d/%m/%Y %H:%M"), note.text) for note in selected_rows]
                self.notes_tab_table.delete_rows(table_rows)
            self.use_cases.delete_notes(selected_notes)
            self.remove_notes_from_todays_notes(selected_notes)

        elif current_tab_name == "Categories":
            selected_rows = self.categories_tab_table.selected_rows
            selected_categories = [category[0] for category in selected_rows]
            if "Default" in selected_categories:
                self.display_error_message_box("Can not delete default category")
                # return
            else:
                if self.use_cases.delete_categories(selected_categories):
                    self.categories_tab_table.delete_selection()
                else:
                    self.display_error_message_box("Can not delete category with assigned notes")

        elif current_tab_name == "Tags":
            selected_rows = self.tags_tab_table.selected_rows
            selected_tags = [tag[0] for tag in selected_rows]
            self.use_cases.delete_tags(selected_tags)
            self.tags_tab_table.delete_selection()

        elif current_tab_name == "Fast filters":
            selected_rows = self.filters_tab_table.selected_rows
            selected_filters = [fast_filter[0] for fast_filter in selected_rows]
            self.use_cases.delete_filters(selected_filters)
            self.filters_tab_table.delete_selection()

        else:
            self.display_error_message_box("Unknown tab")
        
        self.edit_icon_button.disabled = True
        self.delete_icon_button.disabled = True

        self.update_notes_tab_accordion()


    def _get_selected_note(self):
        """
        Gets all information about the currently selected note
        """

        if self.is_table_view:
            selected_notes = self.notes_tab_table.selected_rows
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

        selected_categories = self.categories_tab_table.selected_rows
        if len(selected_categories) != 1:
            return None
        return self.use_cases.find_category_by_name(selected_categories[0][0])



    def _get_selected_tag(self):
        """
        Gets all information about the currently selected tag
        """

        selected_tags = self.tags_tab_table.selected_rows
        if len(selected_tags) != 1:
            return None
        return self.use_cases.find_tag_by_name(selected_tags[0][0])



    def _get_selected_filter(self):
        """
        Gets all information about the currently selected filter
        """

        selected_filters = self.filters_tab_table.selected_rows
        if len(selected_filters) != 1:
            return None
        return self.use_cases.find_filter_by_name(selected_filters[0][0])


    def change_notes_tab_accordion_page(self, label_instance):
        """
        Changes the page of the accordion widget
        """

        self.grid_page = self.notes_tab_accordion_pagination.current_page
        self.update_notes_tab_accordion()


    def update_notes_tab_accordion(self):
        """
        Updates the displayed notes in the accordion widget
        """

        self.grid_notes = [note for note in self.use_cases.get_filtered_notes_paged(self.current_note_filter, page=self.grid_page, size=10)]
        self.notes_tab_accordion.replace_rows(self.grid_notes)
        self.edit_icon_button.disabled = True
        self.delete_icon_button.disabled = True

        self.notes_tab_accordion_pagination.items_count = len(self.notes_tab_table.row_data)
        self.notes_tab_accordion_pagination.create_labels()


    def _filter_items_by_name(self, button_instance):
        """
        Filters table items by their name

        :param button_instance: Button causing this method
        """

        current_tab_name = self.tabs.current_tab.text
        if current_tab_name == "Notes":
            self.current_note_filter = self.create_default_filter()
            self.current_note_filter.note_name = self.notes_tab_searchbar.input.text
            self.use_current_note_filter()

        elif current_tab_name == "Categories":
            categories_name = self.categories_tab_searchbar.input.text
            self.table_categories = [(category.name, category.description) for category in self.use_cases.find_categories_by_name(categories_name)]
            self.categories_tab_table.update_table_data(self.categories_tab_table.table_data, self.table_categories)

        elif current_tab_name == "Tags":
            tags_name = self.tags_tab_searchbar.input.text
            self.table_tags = [(tag.name, tag.description) for tag in self.use_cases.find_tags_by_name(tags_name)]
            self.tags_tab_table.update_table_data(self.tags_tab_table.table_data, self.table_tags)

        elif current_tab_name == "Fast filters":
            filters_name = self.filters_tab_searchbar.input.text
            self.table_filters = [(note_filter.name,
                                   note_filter.order,
                                   note_filter.note_name,
                                   note_filter.category_name) for note_filter in self.use_cases.find_filters_by_name(filters_name)]
            self.filters_tab_table.update_table_data(self.filters_tab_table.table_data, self.table_filters)

        else:
            self.display_error_message_box("Unknown tab")

        self.edit_icon_button.disabled = True
        self.delete_icon_button.disabled = True


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



class KivyApplication(app.MDApp):
    def __init__(self, *args, **kwargs):
        """
        Initializes application widget and its properties
        """

        super(KivyApplication, self).__init__(*args, **kwargs)
        # MacOS doubles the size -- https://github.com/kivy/kivy/issues/8140
        # This sizing doesnt work on the tested MacOS system
        window.Window.size = (1280, 640)
        if platform.system() != "Darwin":
            window.Window.minimum_width, window.Window.minimum_height = window.Window.size
            window.Window.maximum_width, window.Window.maximum_height = window.Window.size
        use_cases = UseCases.UseCases()
        self.kivy_app = KivyApplicationLayout(use_cases, orientation="vertical")


    def build(self):
        return self.kivy_app


def run_application():
    """
    Runs the application with the Kivy gui

    :return: Gui number of the next library
    """

    # Create and run the application
    application = KivyApplication()
    application.run()
    gui = application.kivy_app.gui
    window.Window.close()
    return gui


if __name__ == "__main__":
    run_application()

