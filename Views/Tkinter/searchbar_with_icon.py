import tkinter

class SearchBarWithIcon(tkinter.Frame):
    def __init__(self, master, *args, **kwargs):
        super(SearchBarWithIcon, self).__init__(master, *args, **kwargs)

        searchbar_icon = tkinter.PhotoImage(file = "TodaysNotesIcon.png")
        searchbar_icon = searchbar_icon.subsample(15, 15) # FIXME - resize image

        searchbar_icon_container = tkinter.Label(self, image = searchbar_icon)
        searchbar_icon_container.icon = searchbar_icon
        searchbar_icon_container.grid(row=0, column=0, sticky="news")

        self.entry = tkinter.Entry(self)
        self.entry.insert(0, "Filter by name...")
        self.entry.grid(row=0, column=1, sticky="news")
