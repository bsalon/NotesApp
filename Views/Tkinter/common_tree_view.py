import tkinter
from tkinter import ttk


class CommonTreeView(ttk.Treeview):
    def __init__(self, master, headings, items, stretch, sort_col, reverse, *args, **kwargs):
        super(CommonTreeView, self).__init__(master, column=headings, *args, **kwargs)
        self["show"] = "headings"

        for i, heading in enumerate(headings):
            # stretch_tkinter = tkinter.YES if i == stretch else tkinter.NO
            self.heading(heading, text=heading, command=lambda _head=heading: self._sort_column(_head, True))
            self.column(heading)# , stretch=stretch_tkinter)

        self.fill_table(items)
        self._sort_column(sort_col, reverse)

        self.bind("<Button-1>", self._handle_separator_click)


    def fill_table(self, items):
        self.items = items
        for i, item in enumerate(items):
            self.insert("", 'end', iid=i, values=item)


    # Inspired by https://stackoverflow.com/questions/1966929/tk-treeview-column-sort
    def _sort_column(self, column, reverse):
        items = [(self.set(k, column), k) for k in self.get_children('')]
        items.sort(reverse=reverse)

        for index, (val, k) in enumerate(items):
            self.move(k, '', index)

        self.heading(column, command=lambda _column=column: self._sort_column(_column, not reverse))


    # Inspired by https://stackoverflow.com/questions/45358408/how-to-disable-manual-resizing-of-tkinters-treeview-column
    def _handle_separator_click(self, event):
        if self.identify_region(event.x, event.y) == "separator":
            return "break"
