from datetime import datetime
import tkinter

from tkinter import ttk

from Controllers import UseCases

import common_tree_view
import time_label
import searchbar_with_icon
import scrollable_frame


class TkinterApplication(ttk.Frame):
    def __init__(self, master, use_cases, *args, **kwargs):
        super(TkinterApplication, self).__init__(master, *args, **kwargs)
        self.use_cases = use_cases

        style = ttk.Style()
        style.configure("layout.TFrame", background="white")
        style.configure("today.TFrame", background="grey")
        style.configure("content.TFrame", background="blue")
        self.config(style="layout.TFrame")

        self.current_note_filter = self.create_default_filter()
        self.grid_page = 1
        self.grid_notes = [note for note in self.use_cases.get_filtered_notes_paged(self.current_note_filter, page=self.grid_page, size=10)]

        use_cases_notes = [note for note in self.use_cases.get_notes()]
        self.table_notes = [(note.name, f"{note.priority:03d}", note.time.strftime("%d/%m/%Y %H:%M"), note.text) for note in use_cases_notes]
        self.today_notes = [(note.time.strftime("%H:%M"), note.name) for note in use_cases_notes if note.time.date() == datetime.today().date()]
        self.today_notes.sort(key = lambda note: note[0])

        #self.table_tags = [(tag.name, tag.description) for tag in self.controller.get_tags()]

        #self.table_categories = [(category.name, category.description) for category in self.controller.get_categories()]

        #self.table_filters = [(note_filter.name,
        #                       note_filter.order,
        #                       note_filter.note_name,
        #                       note_filter.category_name) for note_filter in self.controller.get_filters()]

        # 15 rows : 8 columns
        self.pack(padx=0, pady=0, fill="both", expand=True)

        # toolbar layout on top
        self.toolbar_layout = ttk.Frame(self, style="layout.TFrame")
        self._init_toolbar_layout()
        self.toolbar_layout.grid(row=0, column=0, rowspan=1, columnspan=8, sticky="news")

        # todays notes layout
        self.todays_notes_layout = ttk.Frame(self, style="today.TFrame")
        self._init_todays_notes_layout()
        self.todays_notes_layout.grid(row=1, column=0, rowspan=14, columnspan=1, sticky="news")

        # content layout
        self.tabs_content_layout = ttk.Frame(self, style="content.TFrame")
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
        todays_notes_icon = todays_notes_icon.subsample(18, 18) # FIXME - resize image
        self.todays_notes_icon_button = ttk.Button(self.toolbar_layout, text = "Today's notes", image = todays_notes_icon, compound = "top") # TODO click
        self.todays_notes_icon_button.icon = todays_notes_icon
        self.todays_notes_icon_button.grid(row=0, column=col, rowspan=1, columnspan=4)
        self.todays_notes_pane_visible = True
        col += 4

        # Use fast filter section
        ttk.Label(self.toolbar_layout, text = "Use fast filters:").grid(row=0, column=col, rowspan=1, columnspan=3)
        col += 3

        self.fast_filters_text_links = []

        # Time widget
        self.time_widget = time_label.TimeLabel(self.toolbar_layout)
        self.time_widget.grid(row=0, column=col, rowspan=1, columnspan=6)
        col += 6

        # Add icon button
        add_icon = tkinter.PhotoImage(file = "/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/AddIcon.png")
        add_icon = add_icon.subsample(16, 16) # FIXME - resize image
        self.add_icon_button = ttk.Button(self.toolbar_layout, image = add_icon) # TODO click
        self.add_icon_button.icon = add_icon
        self.add_icon_button.grid(row=0, column=col, rowspan=1, columnspan=2)
        col += 2

        # Edit icon button
        edit_icon = tkinter.PhotoImage(file = "/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/EditIcon.png")
        edit_icon = edit_icon.subsample(14, 14) # FIXME - resize image
        self.edit_icon_button = ttk.Button(self.toolbar_layout, image = edit_icon) # TODO click
        self.edit_icon_button.icon = edit_icon
        self.edit_icon_button.grid(row=0, column=col, rowspan=1, columnspan=2)
        col += 2

        # Delete icon button
        delete_icon = tkinter.PhotoImage(file = "/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/DeleteIcon.png")
        delete_icon = delete_icon.subsample(16, 16) # FIXME - resize image
        self.delete_icon_button = ttk.Button(self.toolbar_layout, image = delete_icon) # TODO click
        self.delete_icon_button.icon = delete_icon
        self.delete_icon_button.grid(row=0, column=col, rowspan=1, columnspan=2)
        col += 2

        # Loading bar
        self.loading_bar = ttk.Progressbar(self.toolbar_layout, mode="indeterminate")
        self.loading_bar.grid(row=0, column=col, rowspan=1, columnspan=5)
        self.loading_bar.start(8)
        col += 5
        

        # Settings icon button
        settings_icon = tkinter.PhotoImage(file = "/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/SettingsIcon.png")
        settings_icon = settings_icon.subsample(16, 16) # FIXME - resize image
        self.settings_icon_button = ttk.Button(self.toolbar_layout, image = settings_icon) # TODO click
        self.settings_icon_button.icon = settings_icon
        self.settings_icon_button.grid(row=0, column=col, rowspan=1, columnspan=2)
        col += 2

        # Stretch time widget more than other widgets
        for c in range(col):
            self.toolbar_layout.columnconfigure(c, weight=1)
        for time_col in range(14, 19):
            self.toolbar_layout.columnconfigure(time_col, weight=2)


    def _init_todays_notes_layout(self):
        self.todays_notes_header = tkinter.Label(self.todays_notes_layout, text = "Today's notes")
        self.todays_notes_header.grid(row=0, column=0, padx=(12, 12), pady=(12, 12))

        self.todays_notes_list_frame = scrollable_frame.ScrollableFrame(self.todays_notes_layout)
        self.todays_notes_list_frame.grid(row=1, column=0, sticky="news")
        self.todays_notes_list = []
        self._fill_todays_notes_list()
        
        self.todays_notes_layout.rowconfigure(0, weight=0)
        self.todays_notes_layout.rowconfigure(1, weight=1)
        self.todays_notes_layout.columnconfigure(0, weight=1)


    def _fill_todays_notes_list(self):
        # TODO - wrap and width

        for note in self.today_notes:
            time_label = tkinter.Label(self.todays_notes_list_frame.interior, text = note[0], bg="red")
            time_label.grid(pady=(0, 5))

            name_label = tkinter.Label(self.todays_notes_list_frame.interior, text = note[1], bg="yellow")
            name_label.grid(pady=(0, 20))

            self.todays_notes_list.append((time_label, name_label))


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

        self.tabs.add(self.notes_tab, text = "Notes", sticky = "news")
        self.tabs.add(self.categories_tab, text = "Categories", sticky = "news")
        self.tabs.add(self.tags_tab, text = "Tags", sticky = "news")
        self.tabs.add(self.filters_tab, text = "Fast filters", sticky = "news")

        self.tabs.pack(fill=tkinter.BOTH, expand=True)


    def _init_notes_tab(self):
        self.notes_tab_searchbar = searchbar_with_icon.SearchBarWithIcon(self.notes_tab)
        self.notes_filter_button = tkinter.Button(self.notes_tab, text = "Filter")
        self.notes_advanced_filter_button = tkinter.Button(self.notes_tab, text = "Advanced filter")
        
        self.notes_toggle_switch_label = tkinter.Label(self.notes_tab, text = "Table view")
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
        ) # TODO: use winfo_width() / len(headings) to wrap and justify text
        # with self.notes_tab_table.update()
        # from https://stackoverflow.com/questions/51131812/wrap-text-inside-row-in-tkinter-treeview
        self.notes_tab_table.bind("<<TreeviewSelect>>", lambda x: print(len(self.notes_tab_table.selection())))

        # self.notes_tab_accordion = notes_accordion.NotesAccordion(self.notes_tab, self.grid_notes)

        self.notes_tab_searchbar.grid(row=0, column=0, columnspan=4)
        self.notes_filter_button.grid(row=0, column=4)
        self.notes_advanced_filter_button.grid(row=0, column=5)
        self.notes_toggle_switch_label.grid(row=0, column=6)
        self.notes_toggle_switch_button.grid(row=0, column=7)
        
        self.notes_tab_table.grid(row=1, column=0, columnspan=8, sticky="nsew")

        self.notes_tab.grid_rowconfigure(1, weight=1)
        self.notes_tab.grid_columnconfigure(tuple(range(8)), weight=1)


    def toggle_notes_view(self):
        pass


    def _init_categories_tab(self):
        pass


    def _init_tags_tab(self):
        pass


    def _init_filters_tab(self):
        pass


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
    app = TkinterApplication(root, use_cases)
    app.master.minsize(800, 600)
    app.mainloop()
