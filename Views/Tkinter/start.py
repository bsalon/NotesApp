from datetime import datetime
import tkinter

from tkinter import ttk

import bisect
import textwrap

from Controllers import UseCases

from dialogs import advanced_filter_dialog, category_dialog, note_dialog, filter_dialog, tag_dialog

import common_tree_view
import notes_accordion
import time_label
import searchbar_with_icon
import scrollable_frame


class TkinterApplication(ttk.Frame):
    def __init__(self, master, use_cases, *args, **kwargs):
        super(TkinterApplication, self).__init__(master, *args, **kwargs)
        self.use_cases = use_cases

        self.current_note_filter = self.create_default_filter()
        self.grid_page = 1
        self.grid_notes = [note for note in self.use_cases.get_filtered_notes_paged(self.current_note_filter, page=self.grid_page, size=10)]

        use_cases_notes = [note for note in self.use_cases.get_notes()]
        self.table_notes = [(note.name, f"{note.priority:03d}", note.time.strftime("%d/%m/%Y %H:%M"), note.text) for note in use_cases_notes]
        self.today_notes = [(note.time.strftime("%H:%M"), note.name) for note in use_cases_notes if note.time.date() == datetime.today().date()]
        self.today_notes.sort(key = lambda note: note[0])

        self.table_tags = [(tag.name, tag.description) for tag in self.use_cases.get_tags()]

        self.table_categories = [(category.name, category.description) for category in self.use_cases.get_categories()]

        self.table_filters = [(note_filter.name,
                               f"{note_filter.order:05d}",
                               note_filter.note_name,
                               note_filter.category_name) for note_filter in self.use_cases.get_filters()]

        # 15 rows : 8 columns
        self.pack(padx=0, pady=0, fill="both", expand=True)

        # toolbar layout on top
        self.toolbar_layout = ttk.Frame(self, style="toolbar_container.TFrame")
        self._init_toolbar_layout()
        self.toolbar_layout.grid(row=0, column=0, rowspan=1, columnspan=8, sticky="news")

        # todays notes layout
        self.todays_notes_layout = ttk.Frame(self, style="todays_notes_container.TFrame")
        self._init_todays_notes_layout()
        self.todays_notes_layout.grid(row=1, column=0, rowspan=14, columnspan=1, sticky="news")

        # content layout
        self.tabs_content_layout = ttk.Frame(self, style="tabs_content_container.TFrame")
        self._init_tabs_content_layout()
        self.tabs_content_layout.grid(row=1, column=1, rowspan=14, columnspan=7, sticky="news")

        # stretch rows and columns
        for r in range(1, 15):
            self.rowconfigure(r, weight=1)
        for c in range(8):
            self.columnconfigure(c, weight=1)



    def _init_toolbar_layout(self):
        col = 0

        # Today's notes icon button
        todays_notes_icon = tkinter.PhotoImage(file = "TodaysNotesIcon.png")
        todays_notes_icon = todays_notes_icon.subsample(18, 18) # TODO - resize image
        self.todays_notes_icon_button = ttk.Button(self.toolbar_layout, text="Today's notes", image=todays_notes_icon, compound="top", command=self.toggle_todays_notes_pane, style="today_notes_icon_button.TButton")
        self.todays_notes_icon_button.icon = todays_notes_icon
        self.todays_notes_icon_button.grid(row=0, column=col, rowspan=1, columnspan=4)
        self.todays_notes_pane_visible = True
        col += 4

        # Use fast filter section
        tkinter.Label(self.toolbar_layout, text = "Use fast filters:").grid(row=0, column=col, rowspan=1, columnspan=3)
        col += 3
        self.fast_filters_text_links = [tkinter.Label(self.toolbar_layout, text = "#1"), tkinter.Label(self.toolbar_layout, text = "#2"), tkinter.Label(self.toolbar_layout, text = "#3")]
        for order, fast_filter_text_link in enumerate(self.fast_filters_text_links):
            fast_filter_text_link.grid(row=0, column=col, rowspan=1, columnspan=2)
            fast_filter_text_link.bind("<Button-1>", lambda e, o=order: self.use_fast_filter(o+1))
            col += 2

        # Time widget
        self.time_widget = time_label.TimeLabel(self.toolbar_layout)
        self.time_widget.grid(row=0, column=col, rowspan=1, columnspan=6)
        col += 6

        # Add icon button
        add_icon = tkinter.PhotoImage(file = "/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/AddIcon.png")
        add_icon = add_icon.subsample(16, 16) # TODO - resize image
        self.add_icon_button = ttk.Button(self.toolbar_layout, image = add_icon, command=self.add_item)
        self.add_icon_button.icon = add_icon
        self.add_icon_button.grid(row=0, column=col, rowspan=1, columnspan=2)
        col += 2

        # Edit icon button
        edit_icon = tkinter.PhotoImage(file = "/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/EditIcon.png")
        edit_icon = edit_icon.subsample(14, 14) # TODO - resize image
        self.edit_icon_button = ttk.Button(self.toolbar_layout, image = edit_icon, command=self.edit_item)
        self.edit_icon_button.icon = edit_icon
        self.edit_icon_button.grid(row=0, column=col, rowspan=1, columnspan=2)
        col += 2

        # Delete icon button
        delete_icon = tkinter.PhotoImage(file = "/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/DeleteIcon.png")
        delete_icon = delete_icon.subsample(16, 16) # TODO - resize image
        self.delete_icon_button = ttk.Button(self.toolbar_layout, image = delete_icon, command=self.delete_items)
        self.delete_icon_button.icon = delete_icon
        self.delete_icon_button.grid(row=0, column=col, rowspan=1, columnspan=2)
        col += 2

        # Loading bar
        self.loading_bar = ttk.Progressbar(self.toolbar_layout, mode="indeterminate")
        self.loading_bar.grid(row=0, column=col, rowspan=1, columnspan=5)
        col += 5
        

        # Settings icon button
        settings_icon = tkinter.PhotoImage(file = "/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/SettingsIcon.png")
        settings_icon = settings_icon.subsample(16, 16) # TODO - resize image
        self.settings_icon_button = ttk.Button(self.toolbar_layout, image = settings_icon) # TODO click
        self.settings_icon_button.icon = settings_icon
        self.settings_icon_button.grid(row=0, column=col, rowspan=1, columnspan=2)
        col += 2

        # Stretch time widget more than other widgets
        for c in range(col):
            self.toolbar_layout.columnconfigure(c, weight=1)
        for time_col in range(14, 19):
            self.toolbar_layout.columnconfigure(time_col, weight=2)



    def toggle_todays_notes_pane(self):
        if self.todays_notes_pane_visible:
            self.todays_notes_layout.grid_forget()
            self.tabs_content_layout.grid(row=1, column=0, rowspan=14, columnspan=8, sticky="news")
        else:
            self.tabs_content_layout.grid(row=1, column=1, rowspan=14, columnspan=7, sticky="news")
            self.todays_notes_layout.grid(row=1, column=0, rowspan=14, columnspan=1, sticky="news")
        self.todays_notes_pane_visible = not self.todays_notes_pane_visible



    def use_fast_filter(self, order):
        self.current_note_filter = self.use_cases.find_filter_by_order(order)
        if self.current_note_filter == None:
            self.current_note_filter = self.create_default_filter()
            self.display_error_message_box(f"Fast filter with order={order} is not available")
        self.use_current_note_filter()



    def _init_todays_notes_layout(self):
        self.todays_notes_header = ttk.Label(self.todays_notes_layout, text="Today's notes", style="todays_notes_header.TLabel")
        self.todays_notes_header.grid(row=0, column=0, padx=(12, 12), pady=(12, 12))

        self.todays_notes_list_frame = scrollable_frame.ScrollableFrame(self.todays_notes_layout)
        self.todays_notes_list_frame.grid(row=1, column=0, sticky="news")
        self.todays_notes_list_frame.interior.columnconfigure(0, weight=1)
        self.todays_notes_list = []
        self._fill_todays_notes_list()
        
        self.todays_notes_layout.rowconfigure(0, weight=0)
        self.todays_notes_layout.rowconfigure(1, weight=1)
        self.todays_notes_layout.columnconfigure(0, weight=1)



    def _fill_todays_notes_list(self):
        for note in self.today_notes:
            time_label = tkinter.Label(self.todays_notes_list_frame.interior, text=note[0], bg="red")
            time_label.grid(pady=(0, 5), sticky="news")

            # Fixed width of 20 characters
            wrapped_name = '\n'.join(textwrap.wrap(note[1], 20))
            name_label = tkinter.Label(self.todays_notes_list_frame.interior, text=wrapped_name, bg="yellow")
            name_label.grid(pady=(0, 20), sticky="news")

            self.todays_notes_list.append((time_label, name_label))



    def remove_notes_from_todays_notes(self, notes):
        remove_indices = []
        for time_label, name_label in self.todays_notes_list:
            name = name_label.cget("text")
            time = time_label.cget("text")
            if name in notes:
                i = self.today_notes.index((time, name))
                remove_indices.append(i)

        for i in reversed(sorted(remove_indices)):
            name_label, time_label = self.todays_notes_list[i]
            name_label.destroy()
            time_label.destroy()
            self.today_notes.pop(i)
            self.todays_notes_list.pop(i)



    def add_note_to_todays_notes(self, note):
        if note.time.date() == datetime.today().date():
            # Fixed width of 20 characters
            wrapped_name = '\n'.join(textwrap.wrap(note.name, 20))
            
            note_tuple = (note.time.strftime("%H:%M"), wrapped_name)
            bisect.insort_left(self.today_notes, note_tuple)

            new_note_index = self.today_notes.index(note_tuple)
            
            time_label = tkinter.Label(self.todays_notes_list_frame.interior, text=note_tuple[0], bg="red")
            name_label = tkinter.Label(self.todays_notes_list_frame.interior, text=note_tuple[1], bg="yellow")
            self.todays_notes_list.insert(new_note_index, (time_label, name_label))

            for widget in self.todays_notes_list_frame.interior.children.values():
                widget.grid_forget()
            
            index = 0
            for time_label, name_label in self.todays_notes_list:
                time_label.grid(row=index, pady=(0, 5))
                index += 1
                name_label.grid(row=index, pady=(0, 20))
                index += 1



    def _init_tabs_content_layout(self):
        self.tabs = ttk.Notebook(self.tabs_content_layout)
        
        self.notes_tab = tkinter.Frame(self.tabs)
        self._init_notes_tab()
        self.categories_tab = tkinter.Frame(self.tabs)
        self._init_categories_tab()
        self.tags_tab = tkinter.Frame(self.tabs)
        self._init_tags_tab()
        self.filters_tab = tkinter.Frame(self.tabs)
        self._init_filters_tab()

        self.tabs.add(self.notes_tab, text="Notes", sticky="news")
        self.tabs.add(self.categories_tab, text="Categories", sticky="news")
        self.tabs.add(self.tags_tab, text="Tags", sticky="news")
        self.tabs.add(self.filters_tab, text="Fast filters", sticky="news")

        self.tabs.bind("<<NotebookTabChanged>>", self.tab_update_buttons_enabling)
        self.tabs.pack(fill=tkinter.BOTH, expand=True)



    def _init_notes_tab(self):
        self.notes_tab_searchbar = searchbar_with_icon.SearchBarWithIcon(self.notes_tab)
        self.notes_filter_button = tkinter.Button(self.notes_tab, text="Filter", command=self._filter_items_by_name)
        self.notes_advanced_filter_button = tkinter.Button(self.notes_tab, text="Advanced filter", command=self.notes_advanced_filtering)
        
        self.notes_toggle_switch_label = tkinter.Label(self.notes_tab, text="Table view")
        self.notes_toggle_switch_button_var = tkinter.StringVar()
        self.notes_toggle_switch_button = tkinter.Checkbutton(self.notes_tab, onvalue="ON", offvalue="OFF", width=8,
            indicatoron=False, variable=self.notes_toggle_switch_button_var,
            textvariable=self.notes_toggle_switch_button_var, selectcolor="green", background="red",
            command=self.toggle_notes_view)
        self.notes_toggle_switch_button_var.set("ON")
        
        self.notes_tab_table = common_tree_view.CommonTreeView(
            master=self.notes_tab,
            headings=("Name", "Priority", "Time", "Text"),
            items=self.table_notes,
            stretch=3,
            sort_col="Priority",
            reverse=False
        )
        self.notes_tab_table.bind("<<TreeviewSelect>>", self.table_update_buttons_enabling)
        self.notes_tab_accordion = notes_accordion.NotesAccordion(self.notes_tab, self.grid_notes)
        self.notes_tab_accordion.bind("<<RowCheck>>", self.notes_accordion_buttons_enabling)
        self.is_table_view = True

        self.notes_tab_searchbar.grid(row=0, column=0, columnspan=4)
        self.notes_filter_button.grid(row=0, column=4)
        self.notes_advanced_filter_button.grid(row=0, column=5)
        self.notes_toggle_switch_label.grid(row=0, column=6)
        self.notes_toggle_switch_button.grid(row=0, column=7)
        
        self.notes_tab_table.grid(row=1, column=0, columnspan=8, sticky="nsew")

        self.notes_tab.grid_rowconfigure(1, weight=1)
        self.notes_tab.grid_columnconfigure(tuple(range(8)), weight=1)



    def notes_advanced_filtering(self): 
        dialog = advanced_filter_dialog.AdvancedFilterDialog(self)
        if dialog.accepted:
            filters = lambda: None
            filters.note_name = dialog.data_dict["note_name"]
            filters.note_min_priority = int("0" + dialog.data_dict["note_min_priority"])
            filters.note_max_priority = int("0" + dialog.data_dict["note_max_priority"])
            filters.note_min_time = dialog.data_dict["note_from_date"]
            filters.note_max_time = dialog.data_dict["note_to_date"]
            filters.note_text = dialog.data_dict["note_text"]
            filters.category_name = dialog.data_dict["category_name"]
            filters.category_description = dialog.data_dict["category_description"]
            filters.tag_name = dialog.data_dict["tag_name"]
            filters.tag_description = dialog.data_dict["tag_description"]

            self.current_note_filter = filters
            self.use_current_note_filter()



    def use_current_note_filter(self):
        filtered_notes = self.use_cases.get_filtered_notes(self.current_note_filter)
        self.table_notes = [(note.name, f"{note.priority:03d}", note.time.strftime("%d/%m/%Y %H:%M"), note.text) for note in filtered_notes]

        self.notes_tab_table.replace_data(list(set(self.table_notes)))
        self.update_notes_tab_accordion()



    def toggle_notes_view(self):
        self.is_table_view = not self.is_table_view
        if self.is_table_view:
            self.notes_tab_accordion.grid_forget()
            self.notes_tab_table.grid()
            self.notes_tab_table.grid(row=1, column=0, columnspan=8, sticky="nsew")
            selected_rows_count = len(self.notes_tab_table.selection())
        else:
            self.notes_tab_table.grid_forget()
            self.notes_tab_accordion.grid(row=1, column=0, columnspan=8, sticky="nsew")
            selected_rows_count = self.count_selected_notes()
        self.edit_icon_button["state"] = "enable" if selected_rows_count == 1 else "disabled"
        self.delete_icon_button["state"] = "enable" if selected_rows_count >= 1 else "disabled"



    def _init_categories_tab(self):
        self.categories_tab_searchbar = searchbar_with_icon.SearchBarWithIcon(self.categories_tab)
        self.categories_filter_button = tkinter.Button(self.categories_tab, text="Filter", command=self._filter_items_by_name)
        
        self.categories_tab_table = common_tree_view.CommonTreeView(
            master=self.categories_tab,
            headings=("Name", "Description"),
            items=self.table_categories,
            stretch=0,
            sort_col="Name",
            reverse=False
        )
        self.categories_tab_table.bind("<<TreeviewSelect>>", self.table_update_buttons_enabling)

        self.categories_tab_searchbar.grid(row=0, column=0, columnspan=4)
        self.categories_filter_button.grid(row=0, column=4)
        tkinter.Label(self.categories_tab).grid(row=0, column=5, columnspan=3, sticky="nsew")

        self.categories_tab_table.grid(row=1, column=0, columnspan=8, sticky="nsew")

        self.categories_tab.grid_rowconfigure(1, weight=1)
        self.categories_tab.grid_columnconfigure(tuple(range(8)), weight=1)



    def _init_tags_tab(self):
        self.tags_tab_searchbar = searchbar_with_icon.SearchBarWithIcon(self.tags_tab)
        self.tags_filter_button = tkinter.Button(self.tags_tab, text = "Filter", command=self._filter_items_by_name)
        
        self.tags_tab_table = common_tree_view.CommonTreeView(
            master=self.tags_tab,
            headings=("Name", "Description"),
            items=self.table_tags,
            stretch=0,
            sort_col="Name",
            reverse=False
        )
        self.tags_tab_table.bind("<<TreeviewSelect>>", self.table_update_buttons_enabling)

        self.tags_tab_searchbar.grid(row=0, column=0, columnspan=4)
        self.tags_filter_button.grid(row=0, column=4)
        tkinter.Label(self.tags_tab).grid(row=0, column=5, columnspan=3, sticky="nsew")

        self.tags_tab_table.grid(row=1, column=0, columnspan=8, sticky="nsew")

        self.tags_tab.grid_rowconfigure(1, weight=1)
        self.tags_tab.grid_columnconfigure(tuple(range(8)), weight=1)



    def _init_filters_tab(self):
        self.filters_tab_searchbar = searchbar_with_icon.SearchBarWithIcon(self.filters_tab)
        self.filters_filter_button = tkinter.Button(self.filters_tab, text = "Filter", command=self._filter_items_by_name)
        
        self.filters_tab_table = common_tree_view.CommonTreeView(
            master=self.filters_tab,
            headings=("Name", "Order", "Note name", "Description"),
            items=self.table_filters,
            stretch=0,
            sort_col="Name",
            reverse=False
        )
        self.filters_tab_table.bind("<<TreeviewSelect>>", self.table_update_buttons_enabling)

        self.filters_tab_searchbar.grid(row=0, column=0, columnspan=4)
        self.filters_filter_button.grid(row=0, column=4)
        tkinter.Label(self.filters_tab).grid(row=0, column=5, columnspan=3, sticky="nsew")

        self.filters_tab_table.grid(row=1, column=0, columnspan=8, sticky="nsew")

        self.filters_tab.grid_rowconfigure(1, weight=1)
        self.filters_tab.grid_columnconfigure(tuple(range(8)), weight=1)



    def tab_update_buttons_enabling(self, event):
        current_tab_name = self.tabs.tab(self.tabs.select(), "text")
        if current_tab_name == "Notes":
            if True:
                selected_rows_count = len(self.notes_tab_table.selection())
            else:
                selected_rows_count = self.count_selected_notes()
        elif current_tab_name == "Categories":
            selected_rows_count = len(self.categories_tab_table.selection())
        elif current_tab_name == "Tags":
            selected_rows_count = len(self.tags_tab_table.selection())
        elif current_tab_name == "Fast filters":
            selected_rows_count = len(self.filters_tab_table.selection())
        else:
            self.edit_icon_button["state"] = "disabled"
            self.delete_icon_button["state"] = "disabled"
        self.edit_icon_button["state"] = "enable" if selected_rows_count == 1 else "disabled"
        self.delete_icon_button["state"] = "enable" if selected_rows_count >= 1 else "disabled"



    def count_selected_notes(self):
        return len(self.notes_tab_accordion.get_selected_notes())



    def table_update_buttons_enabling(self, event):
        current_tab_name = self.tabs.tab(self.tabs.select(), "text")
        if current_tab_name == "Notes":
            selected_rows_count = len(self.notes_tab_table.selection())
        elif current_tab_name == "Categories":
            selected_rows_count = len(self.categories_tab_table.selection())
        elif current_tab_name == "Tags":
            selected_rows_count = len(self.tags_tab_table.selection())
        elif current_tab_name == "Fast filters":
            selected_rows_count = len(self.filters_tab_table.selection())
        else:
            self.edit_icon_button["state"] = "disabled"
            self.delete_icon_button["state"] = "disabled"
        self.edit_icon_button["state"] = "enable" if selected_rows_count == 1 else "disabled"
        self.delete_icon_button["state"] = "enable" if selected_rows_count >= 1 else "disabled"



    def notes_accordion_buttons_enabling(self, event):
        if self.tabs.tab(self.tabs.select(), "text") == "Notes" and not self.is_table_view:
            selected_notes_count = self.count_selected_notes()
            self.edit_icon_button["state"] = "enable" if selected_notes_count == 1 else "disabled"
            self.delete_icon_button["state"] = "enable" if selected_notes_count >= 1 else "disabled"



    # Operations on items
    
    def add_item(self):
        self.loading_bar.start(8)
        self.item_action("ADD")
        self.loading_bar.stop()



    def edit_item(self):
        self.loading_bar.start(8)
        self.item_action("EDIT")
        self.loading_bar.stop()



    def item_action(self, action_name):
        current_tab_name = self.tabs.tab(self.tabs.select(), "text")
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

        self.update_notes_tab_accordion()
        self.notes_accordion_buttons_enabling(None)



    def display_error_message_box(self, text):
        tkinter.messagebox.showerror("Error", text)



    # CRUD operations for all items

    def _add_note(self):
        categories_names = [category.name for category in self.use_cases.get_categories()]
        tags_names = [tag.name for tag in self.use_cases.get_tags()]

        dialog = note_dialog.NoteDialog(self, categories_names, tags_names)
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

        dialog = note_dialog.NoteDialog(self, categories_names, tags_names, note=selected_note)
        if dialog.accepted:
            updated_note = lambda: None
            updated_note.name = dialog.data_dict["name"]
            updated_note.time = dialog.data_dict["time"]
            updated_note.text = dialog.data_dict["text"]
            updated_note.priority = int(dialog.data_dict["priority"])
            updated_note.category_name = dialog.data_dict["category"]
            updated_note.tags_names = dialog.data_dict["tags"]
            if self.use_cases.update_note(selected_note.id, updated_note):
                self.remove_notes_from_todays_notes([updated_note.name])
                self.add_note_to_todays_notes(updated_note)
                if self._is_note_filter_accepted(updated_note):
                    old_note_row = (selected_note.name,  f"{selected_note.priority:03d}", selected_note.time.strftime("%d/%m/%Y %H:%M"), selected_note.text)
                    new_note_row = (updated_note.name, f"{updated_note.priority:03d}", updated_note.time.strftime("%d/%m/%Y %H:%M"), updated_note.text)
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
        dialog = category_dialog.CategoryDialog(self)
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

        dialog = category_dialog.CategoryDialog(self, category=selected_category)
        if dialog.accepted:
            updated_category = lambda: None
            updated_category.name = dialog.data_dict["name"]
            updated_category.description = dialog.data_dict["description"]
            if self.use_cases.update_category(selected_category.id, updated_category):
                old_category = tuple(self.categories_tab_table.get_selected_rows()[0])
                new_category = (updated_category.name, updated_category.description)
                self.categories_tab_table.replace_row(old_category, new_category)
            else:
                self.display_error_message_box(f"Category with {updated_category.name} already exists")


    def _add_tag(self):
        dialog = tag_dialog.TagDialog(self.tags_tab)
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

        dialog = tag_dialog.TagDialog(self, tag=selected_tag)
        if dialog.accepted:
            updated_tag = lambda: None
            updated_tag.name = dialog.data_dict["name"]
            updated_tag.description = dialog.data_dict["description"]
            if self.use_cases.update_tag(selected_tag.id, updated_tag):
                old_tag = tuple(self.tags_tab_table.get_selected_rows()[0])
                new_tag = (updated_tag.name, updated_tag.description)
                self.tags_tab_table.replace_row(old_tag, new_tag)
            else:
                self.display_error_message_box(f"Tag with {updated_tag.name} already exists")


    def _add_filter(self):
        dialog = filter_dialog.FilterDialog(self)
        if dialog.accepted:
            new_filter = lambda: None
            new_filter.name = dialog.data_dict["name"]
            new_filter.note_name = dialog.data_dict["note_name"]
            new_filter.note_min_priority = int("0" + dialog.data_dict["note_min_priority"])
            new_filter.note_max_priority = int("0" + dialog.data_dict["note_max_priority"])
            new_filter.note_min_time = dialog.data_dict["note_from_time"]
            new_filter.note_max_time = dialog.data_dict["note_to_time"]
            new_filter.note_text = dialog.data_dict["note_text"]
            new_filter.tag_name = dialog.data_dict["tag_name"]
            new_filter.tag_description = dialog.data_dict["tag_description"]
            new_filter.category_name = dialog.data_dict["category_name"]
            new_filter.category_description = dialog.data_dict["category_description"]
            new_filter.order = int(dialog.data_dict["order"])

            ordered_filters = [fast_filter for fast_filter in self.controller.find_filter_by_order_listed(updated_filter.order)]

            if self.use_cases.create_filter(new_filter):
                new_filter_row = (new_filter.name,
                                  f"{new_filter.order:05d}",
                                  new_filter.note_name,
                                  new_filter.category_name)
                self.filters_tab_table.add_row(new_filter_row)

                table_rows = [(row.name,
                               f"{row.order:05d}",
                               row.note_name,
                               row.category_name) for row in ordered_filters if row.name != new_filter.name]
                self.filters_tab_table.delete_rows(table_rows)

                for i, row in enumerate(table_rows):
                    table_rows[i] = row[0], "-00001", row[2], row[3]
                    self.filters_tab_table.add_row(table_rows[i])
            else:
                self.display_error_message_box(f"Fast filter with {new_filter.name} already exists")


    def _edit_filter(self):
        selected_filter = self._get_selected_filter()

        dialog = filter_dialog.FilterDialog(self, fast_filter = selected_filter)
        if dialog.accepted:
            updated_filter = lambda: None
            updated_filter.name = dialog.data_dict["name"]
            updated_filter.note_name = dialog.data_dict["note_name"]
            updated_filter.note_min_priority = int("0" + dialog.data_dict["note_min_priority"])
            updated_filter.note_max_priority = int("0" + dialog.data_dict["note_max_priority"])
            updated_filter.note_min_time = dialog.data_dict["note_from_time"]
            updated_filter.note_max_time = dialog.data_dict["note_to_time"]
            updated_filter.note_text = dialog.data_dict["note_text"]
            updated_filter.tag_name = dialog.data_dict["tag_name"]
            updated_filter.tag_description = dialog.data_dict["tag_description"]
            updated_filter.category_name = dialog.data_dict["category_name"]
            updated_filter.category_description = dialog.data_dict["category_description"]
            updated_filter.order = int("0" + dialog.data_dict["order"])

            ordered_filters = [fast_filter for fast_filter in self.use_cases.find_filter_by_order_listed(updated_filter.order)]

            if self.use_cases.update_filter(selected_filter.id, updated_filter):
                old_filter = self.filters_tab_table.get_selected_rows()[0]
                old_filter[1] = f"{old_filter[1]:05d}"
                old_filter = tuple(old_filter)
                new_filter = (updated_filter.name,
                              f"{updated_filter.order:05d}",
                              updated_filter.note_name,
                              updated_filter.category_name)
                self.filters_tab_table.replace_row(old_filter, new_filter)

                table_rows = [(row.name,
                               f"{row.order:05d}",
                               row.note_name,
                               row.category_name) for row in ordered_filters if row.name != updated_filter.name]
                self.filters_tab_table.delete_rows(table_rows)

                for i, row in enumerate(table_rows):
                    table_rows[i] = row[0], -1, row[2], row[3]
                    self.filters_tab_table.add_row(table_rows[i])
            else:
                self.display_error_message_box(f"Fast filter with {updated_filter.name} already exists")



    def delete_items(self):
        current_tab_name = self.tabs.tab(self.tabs.select(), "text")
        if current_tab_name == "Notes":
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

        elif current_tab_name == "Categories":
            selected_rows = self.categories_tab_table.get_selected_rows()
            selected_categories = [category[0] for category in selected_rows]
            if self.use_cases.delete_categories(selected_categories):
                self.categories_tab_table.delete_selection()
            else:
                self.display_error_message_box("Can not delete categories with assigned notes")

        elif current_tab_name == "Tags":
            selected_rows = self.tags_tab_table.get_selected_rows()
            selected_tags = [tag[0] for tag in selected_rows]
            self.use_cases.delete_tags(selected_tags)
            self.tags_tab_table.delete_selection()

        elif current_tab_name == "Fast filters":
            selected_rows = self.filters_tab_table.get_selected_rows()
            selected_filters = [fast_filter[0] for fast_filter in selected_rows]
            self.use_cases.delete_filters(selected_filters)
            self.filters_tab_table.delete_selection()

        else:
            self.display_error_message_box("Unknown tab")

        self.update_notes_tab_accordion()
        self.notes_accordion_buttons_enabling(None)



    def _get_selected_note(self):
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
        selected_categories = self.categories_tab_table.get_selected_rows()
        if len(selected_categories) != 1:
            return None
        return self.use_cases.find_category_by_name(selected_categories[0][0])



    def _get_selected_tag(self):
        selected_tags = self.tags_tab_table.get_selected_rows()
        if len(selected_tags) != 1:
            return None
        return self.use_cases.find_tag_by_name(selected_tags[0][0])



    def _get_selected_filter(self):
        selected_filters = self.filters_tab_table.get_selected_rows()
        if len(selected_filters) != 1:
            return None
        return self.use_cases.find_filter_by_name(selected_filters[0][0])


    def change_notes_tab_accordion_page(self): # TODO
        #self.grid_page = self.notes_tab_accordion_pagination.current_page
        self.update_notes_tab_accordion()
        selected_rows_count = self.count_selected_notes()
        self.edit_icon_button.setEnabled(selected_rows_count == 1)
        self.delete_icon_button.setEnabled(selected_rows_count >= 1)


    def update_notes_tab_accordion(self): # TODO
        self.grid_notes = [note for note in self.use_cases.get_filtered_notes_paged(self.current_note_filter, page=self.grid_page, size=10)]
        self.notes_tab_accordion.replace_rows(self.grid_notes)

        #self.notes_tab_accordion_pagination.items_count = self.notes_tab_table.model.rowCount(index)
        #self.notes_tab_accordion_pagination.create_labels()


    def _filter_items_by_name(self):
        current_tab_name = self.tabs.tab(self.tabs.select(), "text")
        if current_tab_name == "Notes":
            self.current_note_filter = self.create_default_filter()
            self.current_note_filter.note_name = self.notes_tab_searchbar.entry.get()
            self.use_current_note_filter()
        elif current_tab_name == "Categories":
            self.table_categories = None
        elif current_tab_name == "Tags":
            self.table_tags = None
        elif current_tab_name == "Fast filters":
            self.table_filters = None
            self.filters_tab_table.replace
        else:
            self.display_error_message_box("Unknown tab")
        


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
    use_cases = UseCases.UseCases()

    root = tkinter.Tk()
    
    style = ttk.Style()
    style.configure("toolbar_container.TFrame", background="#ffc957")
    style.configure("todays_notes_container.TFrame", background="#f1f6be")
    style.configure("tabs_content_container.TFrame", background="#f1f6be")
    style.configure("inter.TFrame", background="black")
    
    style.configure("today_notes_icon_button.TButton", background="#ffc957")
    style.configure("text_link.TLabel", background="#ffc957")
    style.configure("toolbar_icon_button.TButton", background="white")

    style.configure("todays_notes_header.TLabel", background="#d7eb5a")
    
    app = TkinterApplication(root, use_cases)
    app.master.minsize(800, 600)
    app.mainloop()
