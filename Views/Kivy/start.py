import kivy

from kivy import app, lang, metrics
from kivy.core import window
from kivy.uix import boxlayout, button, image, label, recycleview, switch, tabbedpanel

from kivymd import app

from datetime import datetime

from Controllers import UseCases

from dialogs import category_dialog, note_dialog, tag_dialog

# import clickable_label
import custom_mddatatable
import loading_bar
import searchbar_with_icon
import styled_widgets
import todays_notes_recycleview


class KivyApplicationLayout(boxlayout.BoxLayout):
    def __init__(self, use_cases, *args, **kwargs):
        super(KivyApplicationLayout, self).__init__(*args, **kwargs)

        self.use_cases = use_cases

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

        # toolbar layout on top
        self.toolbar_layout = boxlayout.BoxLayout(orientation="horizontal", size_hint=(1, 1/15))
        self._init_toolbar_layout()

        # todays notes layout
        self.todays_notes_layout = boxlayout.BoxLayout(orientation="vertical", size_hint=(1/8, 1))
        self._init_todays_notes_layout()

        # content layout
        self.tabs_content_layout = boxlayout.BoxLayout(orientation="vertical", size_hint=(7/8, 1))
        self._init_tabs_content_layout()

        # todays notes and content below toolbar
        todays_notes_and_content_layout = boxlayout.BoxLayout(orientation="horizontal", size_hint=(1, 14/15))
        todays_notes_and_content_layout.add_widget(self.todays_notes_layout)
        todays_notes_and_content_layout.add_widget(self.tabs_content_layout)
        
        # 15 rows : 8 columns
        self.add_widget(self.toolbar_layout)
        self.add_widget(todays_notes_and_content_layout)



    def _init_toolbar_layout(self):
        # Today's notes icon button
        self.todays_notes_icon_button = styled_widgets.TodaysNotesButton(on_release=self.toggle_todays_notes_pane)
        todays_notes_icon = image.Image(source = "/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/TodaysNotesIcon.png", size_hint=(1, 3/4))

        todays_notes_icon_button_layout = boxlayout.BoxLayout(orientation="vertical", size_hint=(4/32, 1))
        todays_notes_icon_button_layout.add_widget(todays_notes_icon)
        todays_notes_icon_button_layout.add_widget(self.todays_notes_icon_button)

        self.toolbar_layout.add_widget(todays_notes_icon_button_layout)
        self.todays_notes_pane_visible = True

        # Use fast filter section
        self.toolbar_layout.add_widget(styled_widgets.FastFilterLabel())

        self.fast_filters_text_links = [styled_widgets.ClickableLabel(text="[ref=1]#1[/ref]"),
                                        styled_widgets.ClickableLabel(text="[ref=2]#2[/ref]"),
                                        styled_widgets.ClickableLabel(text="[ref=3]#3[/ref]")]
        for order, fast_filter_text_link in enumerate(self.fast_filters_text_links):
            self.toolbar_layout.add_widget(fast_filter_text_link)
            fast_filter_text_link.click_command = lambda o=order: print(f"{o + 1}") # TODO self.use_fast_filter(o+1)

        # Time widget
        self.time_widget = styled_widgets.TimeLabel()
        self.toolbar_layout.add_widget(self.time_widget)

        # Add icon button
        self.add_icon_button = styled_widgets.ToolbarButton(background_normal="/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/AddIcon.png", on_release=self.add_item)
        self.toolbar_layout.add_widget(self.add_icon_button)

        # Edit icon button
        self.edit_icon_button = styled_widgets.ToolbarButton(background_normal="/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/EditIcon.png", disabled=True, on_release=self.edit_item)
        self.toolbar_layout.add_widget(self.edit_icon_button)

        # Delete icon button
        self.delete_icon_button = styled_widgets.ToolbarButton(background_normal="/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/DeleteIcon.png", disabled=True, on_release=self.delete_items)
        self.toolbar_layout.add_widget(self.delete_icon_button)

        # Loading bar
        self.loading_bar = loading_bar.LoadingBar(size_hint=(5/32, 1))
        self.toolbar_layout.add_widget(self.loading_bar)

        # Settings icon button
        self.settings_icon_button = styled_widgets.ToolbarButton(background_normal="/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/SettingsIcon.png")
        self.toolbar_layout.add_widget(self.settings_icon_button)



    def toggle_todays_notes_pane(self, button_instance):
        w = self.todays_notes_layout
        if self.todays_notes_pane_visible:
            w.saved_attrs = w.height, w.width, w.size_hint_x, w.size_hint_y, w.opacity, w.disabled
            w.height, w.width, w.size_hint_x, w.size_hint_y, w.opacity, w.disabled = 0, 0, None, None, 0, True
            self.tabs_content_layout.size_hint = 1, 1
            
        else:
            w.height, w.width, w.size_hint_x, w.size_hint_y, w.opacity, w.disabled = w.saved_attrs
            del w.saved_attrs
            self.tabs_content_layout.size_hint = 7/8, 1

        self.todays_notes_pane_visible = not self.todays_notes_pane_visible



    def use_fast_filter(self, order): # TODO
        self.current_note_filter = self.use_cases.find_filter_by_order(order)
        if self.current_note_filter == None:
            self.current_note_filter = self.create_default_filter()
            self.display_error_message_box(f"Fast filter with order={order} is not available")
        self.use_current_note_filter()

    

    def _init_todays_notes_layout(self):
        self.todays_notes_header = styled_widgets.TodaysNotesLabel()
        self.todays_notes_layout.add_widget(self.todays_notes_header)

        self.todays_notes_recycleview = todays_notes_recycleview.TodaysNotesRecycleview(self.today_notes)
        self.todays_notes_layout.add_widget(self.todays_notes_recycleview)


    def remove_notes_from_todays_notes(self, notes):
        todays_notes = self.todays_notes_recycleview.data
        for note in notes:
            index = next((i for i, v in enumerate(todays_notes) if v["name"] == note), None)
            if index:
                del todays_notes[index]


    def add_note_to_todays_notes(self, note):
        note_dict = {"time": note.time.strftime("%H:%M"), "name": note.name}
        for i, val in enumerate(self.todays_notes_recycleview.data):
            if val["time"] > note_dict["time"]:
                self.todays_notes_recycleview.data.insert(i, note_dict)
                return

        self.todays_notes_recycleview.data.append(note_dict)


    def _init_tabs_content_layout(self):
        self.tabs = tabbedpanel.TabbedPanel(do_default_tab=False)

        self.notes_tab = tabbedpanel.TabbedPanelItem(text="Notes")
        self._init_notes_tab()
        self.categories_tab = tabbedpanel.TabbedPanelItem(text="Categories")
        self._init_categories_tab()
        self.tags_tab = tabbedpanel.TabbedPanelItem(text="Tags")
        self._init_tags_tab()
        self.filters_tab = tabbedpanel.TabbedPanelItem(text="Fast filters")
        self._init_filters_tab()

        self.tabs.add_widget(self.notes_tab)
        self.tabs.add_widget(self.categories_tab)
        self.tabs.add_widget(self.tags_tab)
        self.tabs.add_widget(self.filters_tab)
        self.tabs.bind(current_tab=self.tab_update_buttons_enabling)

        self.tabs_content_layout.add_widget(self.tabs)



    def _init_notes_tab(self):
        self.notes_tab_searchbar = searchbar_with_icon.SearchBarWithIcon(size_hint=(4/8, 1))
        self.notes_filter_button = button.Button(text="Filter", size_hint=(1/8, 1))
        # TODO command=self._filter_items_by_name
        self.notes_advanced_filter_button = button.Button(text="Advanced filter", size_hint=(1/8, 1))
        # TODO command=self.notes_advanced_filtering
        self.notes_toggle_switch_label = label.Label(text="Table view", size_hint=(1/8, 1))
        self.notes_toggle_switch_button = switch.Switch(active=True, size_hint=(1/8, 1))
        # TODO command=self.toggle_notes_view

        self.notes_tab_toolbar_layout = boxlayout.BoxLayout(orientation="horizontal", size_hint=(1, 1/9))
        self.notes_tab_toolbar_layout.add_widget(self.notes_tab_searchbar)
        self.notes_tab_toolbar_layout.add_widget(self.notes_filter_button)
        self.notes_tab_toolbar_layout.add_widget(self.notes_advanced_filter_button)
        self.notes_tab_toolbar_layout.add_widget(self.notes_toggle_switch_label)
        self.notes_tab_toolbar_layout.add_widget(self.notes_toggle_switch_button)

        self.notes_tab_table = custom_mddatatable.CustomMDDataTable(
            check=True,
            elevation=0,
            size_hint=(1, 8/9),
            rows_num=100000,
            column_data=[
                ("Name", metrics.dp(30), lambda data: zip(*sorted(enumerate(data), key=lambda x:x[1][0]))),
                ("Priority", metrics.dp(30), lambda data: zip(*sorted(enumerate(data), key=lambda x:x[1][1]))),
                ("Time", metrics.dp(30), lambda data: zip(*sorted(enumerate(data), key=lambda x:x[1][2]))),
                ("Text", metrics.dp(50), lambda data: zip(*sorted(enumerate(data), key=lambda x:x[1][3])))
            ],
            row_data=self.table_notes
        )
        self.notes_tab_table.bind(on_row_press=self.table_update_buttons_enabling)

        # TODO accordion

        self.notes_tab_layout = boxlayout.BoxLayout(orientation="vertical", size_hint=(1, 1))
        self.notes_tab_layout.add_widget(self.notes_tab_toolbar_layout)
        self.notes_tab_layout.add_widget(self.notes_tab_table)

        self.notes_tab.add_widget(self.notes_tab_layout)

        #self.notes_tab_accordion = notes_accordion.NotesAccordion(self.notes_tab, self.grid_notes)
        #self.notes_tab_accordion.bind("<<RowCheck>>", self.notes_accordion_buttons_enabling)
        #self.notes_tab_accordion_pagination = pagination_labels.PaginationLabels(self.notes_tab, 10, len(self.table_notes))
        #self.notes_tab_accordion_pagination.bind("<<PageChanged>>", self.change_notes_tab_accordion_page)
        self.is_table_view = True


    def _init_categories_tab(self):
        self.categories_tab_searchbar = searchbar_with_icon.SearchBarWithIcon(size_hint=(4/8, 1))
        self.categories_filter_button = button.Button(text="Filter", size_hint=(1/8, 1))
        # TODO command=self._filter_items_by_name)

        self.categories_tab_toolbar_layout = boxlayout.BoxLayout(orientation="horizontal", size_hint=(1, 1/9))
        self.categories_tab_toolbar_layout.add_widget(self.categories_tab_searchbar)
        self.categories_tab_toolbar_layout.add_widget(self.categories_filter_button)
        self.categories_tab_toolbar_layout.add_widget(label.Label(size_hint=(3/8, 1)))

        self.categories_tab_table = custom_mddatatable.CustomMDDataTable(
            check=True,
            elevation=0,
            size_hint=(1, 8/9),
            rows_num=100000,
            column_data=[
                ("Name", metrics.dp(30), lambda data: zip(*sorted(enumerate(data), key=lambda x:x[1][0]))),
                ("Description", metrics.dp(100), lambda data: zip(*sorted(enumerate(data), key=lambda x:x[1][1]))),
            ],
            row_data=self.table_categories
        )
        self.categories_tab_table.bind(on_row_press=self.table_update_buttons_enabling)

        self.categories_tab_layout = boxlayout.BoxLayout(orientation="vertical", size_hint=(1, 1))
        self.categories_tab_layout.add_widget(self.categories_tab_toolbar_layout)
        self.categories_tab_layout.add_widget(self.categories_tab_table)

        self.categories_tab.add_widget(self.categories_tab_layout)




    def _init_tags_tab(self):
        self.tags_tab_searchbar = searchbar_with_icon.SearchBarWithIcon(size_hint=(4/8, 1))
        self.tags_filter_button = button.Button(text="Filter", size_hint=(1/8, 1))
        # TODO command=self._filter_items_by_name)

        self.tags_tab_toolbar_layout = boxlayout.BoxLayout(orientation="horizontal", size_hint=(1, 1/9))
        self.tags_tab_toolbar_layout.add_widget(self.tags_tab_searchbar)
        self.tags_tab_toolbar_layout.add_widget(self.tags_filter_button)
        self.tags_tab_toolbar_layout.add_widget(label.Label(size_hint=(3/8, 1)))

        self.tags_tab_table = custom_mddatatable.CustomMDDataTable(
            check=True,
            elevation=0,
            size_hint=(1, 8/9),
            rows_num=100000,
            column_data=[
                ("Name", metrics.dp(30), lambda data: zip(*sorted(enumerate(data), key=lambda x:x[1][0]))),
                ("Description", metrics.dp(100), lambda data: zip(*sorted(enumerate(data), key=lambda x:x[1][1]))),
            ],
            row_data=self.table_tags
        )
        self.tags_tab_table.bind(on_row_press=self.table_update_buttons_enabling)

        self.tags_tab_layout = boxlayout.BoxLayout(orientation="vertical", size_hint=(1, 1))
        self.tags_tab_layout.add_widget(self.tags_tab_toolbar_layout)
        self.tags_tab_layout.add_widget(self.tags_tab_table)

        self.tags_tab.add_widget(self.tags_tab_layout)



    def _init_filters_tab(self): # TODO
        self.filters_tab_searchbar = searchbar_with_icon.SearchBarWithIcon(size_hint=(4/8, 1))
        self.filters_filter_button = button.Button(text="Filter", size_hint=(1/8, 1))
        # TODO command=self._filter_items_by_name)

        self.filters_tab_toolbar_layout = boxlayout.BoxLayout(orientation="horizontal", size_hint=(1, 1/9))
        self.filters_tab_toolbar_layout.add_widget(self.filters_tab_searchbar)
        self.filters_tab_toolbar_layout.add_widget(self.filters_filter_button)
        self.filters_tab_toolbar_layout.add_widget(label.Label(size_hint=(3/8, 1)))

        self.filters_tab_table = custom_mddatatable.CustomMDDataTable(
            check=True,
            elevation=0,
            size_hint=(1, 8/9),
            rows_num=100000,
            column_data=[
                ("Name", metrics.dp(30), lambda data: zip(*sorted(enumerate(data), key=lambda x:x[1][0]))),
                ("Order", metrics.dp(25), lambda data: zip(*sorted(enumerate(data), key=lambda x:x[1][1]))),
                ("Note name", metrics.dp(30), lambda data: zip(*sorted(enumerate(data), key=lambda x:x[1][2]))),
                ("Description", metrics.dp(60), lambda data: zip(*sorted(enumerate(data), key=lambda x:x[1][3]))),
            ],
            row_data=self.table_filters
        )
        self.filters_tab_table.bind(on_row_press=self.table_update_buttons_enabling)


        self.filters_tab_layout = boxlayout.BoxLayout(orientation="vertical", size_hint=(1, 1))
        self.filters_tab_layout.add_widget(self.filters_tab_toolbar_layout)
        self.filters_tab_layout.add_widget(self.filters_tab_table)

        self.filters_tab.add_widget(self.filters_tab_layout)


    def tab_update_buttons_enabling(self, instance, value):
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
        return 0 # TODO


    def table_update_buttons_enabling(self, table_instance, row_instance):
        selected_rows_count = len(table_instance.selected_rows)
        self.edit_icon_button.disabled = selected_rows_count != 1
        self.delete_icon_button.disabled = selected_rows_count < 1
        


    def notes_accordion_buttons_enabling(self): # TODO
        pass


    # Operations on items

    def add_item(self, instance):
        # TODO start loading bar
        self.item_action("ADD")
        # TODO stop loading bar


    def edit_item(self, instance):
        # TODO start loading bar
        self.item_action("EDIT")
        # TODO stop loading bar


    def item_action(self, action_name):
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

        # TODO self.update_notes_tab_accordion()
        # TODO self.notes_accordion_buttons_enabling(None)



    def display_error_message_box(self, text): # TODO
        message_box = popup.Popup(
            title=text,
            content=button.Button(text="Close")
        )
        message_box.content.bind(on_press=message_box.dismiss)
        message_box.open()



    # CRUD operations for all items

    def _add_note(self):
        categories_names = [category.name for category in self.use_cases.get_categories()]
        tags_names = [tag.name for tag in self.use_cases.get_tags()]

        dialog = note_dialog.NoteDialog(categories_names, tags_names)
        dialog.bind(on_dismiss=self._add_note_dialog_closed)
        dialog.open()


    def _add_note_dialog_closed(self, dialog):
        if dialog.accepted:
            new_note = lambda: None
            new_note.name = dialog.data_dict["name"]
            new_note.time = dialog.data_dict["time"]
            new_note.text = dialog.data_dict["text"]
            new_note.priority = int(dialog.data_dict["priority"])
            new_note.category_name = dialog.data_dict["category"]
            new_note.tags_names = dialog.data_dict["tags"]
            if self.use_cases.create_note(new_note):
                self.add_note_to_todays_notes(new_note)
                if self._is_note_filter_accepted(new_note):
                    new_note_row = (new_note.name, new_note.priority, new_note.time.strftime("%d/%m/%Y %H:%M"), new_note.text)
                    self.notes_tab_table.add_row(new_note_row)
            else:
                self.display_error_message_box(f"Note with {new_note.name} already exists")


    
    def _edit_note(self):
        categories_names = [category.name for category in self.use_cases.get_categories()]
        tags_names = [tag.name for tag in self.use_cases.get_tags()]
        selected_note = self._get_selected_note()

        dialog = note_dialog.NoteDialog(categories_names, tags_names)
        dialog.fill_dialog(selected_note)
        dialog.bind(on_dismiss=self._edit_note_dialog_closed)
        dialog.open()


    def _edit_note_dialog_closed(self, dialog):
        selected_note = self._get_selected_note()
        if dialog.accepted:
            updated_note = lambda: None
            updated_note.name = dialog.data_dict["name"]
            updated_note.time = dialog.data_dict["time"]
            updated_note.text = dialog.data_dict["text"]
            updated_note.priority = int(dialog.data_dict["priority"])
            updated_note.category_name = dialog.data_dict["category"]
            updated_note.tags_names = dialog.data_dict["tags"]
            if self.use_cases.update_note(selected_note.id, updated_note):
                self.remove_notes_from_todays_notes([selected_note.name]) # TODO repair in Tk and PyQt
                self.add_note_to_todays_notes(updated_note)
                if self._is_note_filter_accepted(updated_note):
                    old_note_row = (selected_note.name, selected_note.priority, selected_note.time.strftime("%d/%m/%Y %H:%M"), selected_note.text)
                    new_note_row = (updated_note.name, updated_note.priority, updated_note.time.strftime("%d/%m/%Y %H:%M"), updated_note.text)
                    self.notes_tab_table.update_row(old_note_row, new_note_row)
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
        dialog = category_dialog.CategoryDialog()
        dialog.bind(on_dismiss=self._add_category_dialog_closed)
        dialog.open()


    def _add_category_dialog_closed(self, dialog):
        if dialog.accepted:
            new_category = lambda: None
            new_category.name = dialog.data_dict["name"]
            new_category.description = dialog.data_dict["description"]
            if self.use_cases.create_category(new_category):
                new_category_row = (new_category.name, new_category.description)
                self.categories_tab_table.add_row(new_category_row)
            else:
                self.display_error_message_box(f"Category with {new_category.name} already exists")


    def _edit_category(self):
        selected_category = self._get_selected_category()

        dialog = category_dialog.CategoryDialog()
        dialog.fill_dialog(selected_category)
        dialog.bind(on_dismiss=self._edit_category_dialog_closed)
        dialog.open()


    def _edit_category_dialog_closed(self, dialog):
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
                self.display_error_message_box(f"Category with {updated_category.name} already exists")



    def _add_tag(self):
        dialog = tag_dialog.TagDialog()
        dialog.bind(on_dismiss=self._add_tag_dialog_closed)
        dialog.open()


    def _add_tag_dialog_closed(self, dialog):
        if dialog.accepted:
            new_tag = lambda: None
            new_tag.name = dialog.data_dict["name"]
            new_tag.description = dialog.data_dict["description"]
            if self.use_cases.create_tag(new_tag):
                new_tag_row = (new_tag.name, new_tag.description)
                self.tags_tab_table.add_row(new_tag_row)
            else:
                self.display_error_message_box(f"Tag with {new_tag.name} already exists")


    def _edit_tag(self):
        selected_tag = self._get_selected_tag()
        
        dialog = tag_dialog.TagDialog()
        dialog.fill_dialog(selected_tag)
        dialog.bind(on_dismiss=self._edit_tag_dialog_closed)
        dialog.open()


    def _edit_tag_dialog_closed(self, dialog):
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
                self.display_error_message_box(f"Tag with {updated_tag.name} already exists")


    def _add_filter(self):
        dialog = filter_dialog.FilterDialog()
        dialog.bind(on_dismiss=self._add_filter_dialog_closed)
        dialog.open()


    def _add_filter_dialog_closed(self, dialog):
        pass


    def _edit_filter(self):
        selected_filter = self._get_selected_filter()

        dialog = filter_dialog.FilterDialog()
        dialog.fill_dialog(selected_filter)
        dialog.bind(on_dismiss=self._edit_filter_dialog_closed)
        dialog.open()


    def _edit_filter_dialog_closed(self, dialog):
        pass


    def delete_items(self, button_instance):
        current_tab_name = self.tabs.current_tab.text
        if current_tab_name == "Notes":
            if self.is_table_view:
                selected_rows = self.notes_tab_table.selected_rows
                selected_notes = [note[0] for note in selected_rows]
                self.notes_tab_table.delete_selection()
            else:
                selected_rows = self.notes_tab_accordion.selected_rows
                selected_notes = [note.name for note in selected_rows]
                table_rows = [(note.name, note.priority, note.time.strftime("%d/%m/%Y %H:%M"), note.text) for note in selected_rows]
                self.notes_tab_table.delete_rows(table_rows)
            self.use_cases.delete_notes(selected_notes)
            self.remove_notes_from_todays_notes(selected_notes)

        elif current_tab_name == "Categories":
            selected_rows = self.categories_tab_table.selected_rows
            selected_categories = [category[0] for category in selected_rows]
            if self.use_cases.delete_categories(selected_categories):
                self.categories_tab_table.delete_selection()
            else:
                self.display_error_message_box("Can not delete categories with assigned notes")

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
        
        # TODO with # #
        self.edit_icon_button.disabled = True
        self.delete_icon_button.disabled = True

        # self.update_notes_tab_accordion()
        # self.notes_accordion_buttons_enabling(None)


    def _get_selected_note(self):
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
        selected_categories = self.categories_tab_table.selected_rows
        if len(selected_categories) != 1:
            return None
        return self.use_cases.find_category_by_name(selected_categories[0][0])



    def _get_selected_tag(self):
        selected_tags = self.tags_tab_table.selected_rows
        if len(selected_tags) != 1:
            return None
        return self.use_cases.find_tag_by_name(selected_tags[0][0])



    def _get_selected_filter(self):
        selected_filters = self.filters_tab_table.selected_rows
        if len(selected_filters) != 1:
            return None
        return self.use_cases.find_filter_by_name(selected_filters[0][0])



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



class KivyApplication(app.MDApp):
    def build(self):
        window.Window.clearcolor = (50, 50, 50, 50)
        use_cases = UseCases.UseCases()
        return KivyApplicationLayout(use_cases, orientation="vertical")


if __name__ == "__main__":
    KivyApplication().run()


