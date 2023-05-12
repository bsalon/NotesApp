import tkinter
from tkinter import ttk

import pathlib


class SearchBarWithIcon(ttk.Frame):
    """
    Search field with magnify icon to filter items by name
    """

    def __init__(self, master, *args, **kwargs):
        super(SearchBarWithIcon, self).__init__(master, *args, **kwargs)
        image_path = pathlib.Path(__file__).parent.parent.parent / "Images" / "SearchIcon.png"
        searchbar_icon = tkinter.PhotoImage(file = image_path.resolve().as_posix())
        searchbar_icon = searchbar_icon.subsample(10, 10)

        self.searchbar_icon_container = tkinter.Label(self, image = searchbar_icon, anchor="e", bg="white")
        self.searchbar_icon_container.icon = searchbar_icon
        self.searchbar_icon_container.grid(row=0, column=0, padx=(2, 0), pady=(2, 2))

        self.entry = ttk.Entry(self, style="searchbar_entry.TEntry")
        self.entry_put_placeholder()
        self.entry.bind("<FocusIn>", self.entry_focus_in)
        self.entry.bind("<FocusOut>", self.entry_focus_out)
        self.entry.grid(row=0, column=1, sticky="news", padx=(0, 2), pady=(2, 2))

        self.columnconfigure(1, weight=1)



    def entry_put_placeholder(self):
        self.entry.insert(0, "Filter by name...")
        self.entry['style'] = "searchbar_placeholder.TEntry"


    def entry_focus_in(self, event):
        if self.entry['style'] == "searchbar_placeholder.TEntry":
            self.entry.delete('0', 'end')
            self.entry['style'] = "searchbar_entry.TEntry"


    def entry_focus_out(self, event):
        if not self.entry.get():
            self.entry_put_placeholder()
