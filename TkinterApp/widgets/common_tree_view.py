import tkinter
from tkinter import ttk


class CommonTreeView(ttk.Treeview):
    """
    Table used in the tabs to display records

    Methods are used for CRUD operations
    """

    def __init__(self, master, headings, items, sort_col, reverse, int_cols = [], *args, **kwargs):
        super(CommonTreeView, self).__init__(master, column=headings, *args, **kwargs)
        self["show"] = "headings"

        for i, heading in enumerate(headings):
            #stretch_tkinter = tkinter.YES if i == stretch else tkinter.NO
            self.heading(heading, text=heading, command=lambda _head=heading: self._sort_column(_head, True))
            self.column(heading, anchor="n") #, stretch=stretch_tkinter)
            


        self.fill_table(items)

        self.headings = headings
        self.column = sort_col
        self.reverse = reverse
        self.int_cols = int_cols
        self._sort_column(sort_col, reverse)

        self.bind("<Button-1>", self._handle_separator_click)

        # Word-wrapping in Treeview needs to be programmed manually - which makes the problem
        # challenging because of font sizes and dynamic calculation of pixels
        # https://stackoverflow.com/questions/51131812/wrap-text-inside-row-in-tkinter-treeview
        # Row height would need to be programmed manually as well

        # Idea would be to 
        #   1. Use .grid() before fill_table()
        #       * This would require more arguments for constructor - col, row, colspan, rowspan
        #   2. Count column width in pixels by winfo_width // len(headings)
        #   3. Convert pixels to number of characters which can fit the width
        #       * tkinter doesn't seem to support this functionality so this would require to remember
        #         the current font and its size, and also to know sizes of particular characters
        #         in that font to get the precise number
        #       * this makes the problem programmatically more challenging because it would be needed
        #         to calculate the number of characters that can fit the row for each row of the text
        #         before it is split, for example:
        #           - row width is 200px
        #           - string has 150 characters
        #           - 200px can fit from 5 to 20 characters
        #           - string has to be split accordingly to fit the maximal number of characters
        #           - it can be split like this - www, iiiiii, ........, normal, and so on
        #           - the string would have to be looped by character and the algorithm would
        #             remember the current pixels taken
        #           - after pixels exceed the row width, '\n' is inserted - this is not supported by the textwrap 
        #             module, and would have to be programmed manually - it also doesn't take into the account
        #             the word wrapping
        #   4. Use textwrap module to wrap the text to fit the column (if possible)
        #   5. Count number of '\n's in the resulting text to calculate the row height
        #   6. Use the counted number to multiply the current row size

        # This idea doesn't take into the account the responsibility of the main window which can
        # break the sizings of the columns and rows - requires more information to know if this holds


    def fill_table(self, items):
        self.items = items
        for item in items:
            self.insert("", 'end', values=item)


    def add_row(self, row):
        self.insert("", 'end', values=row)
        self.items.append(row)
        self._sort_column(self.column, self.reverse)


    def replace_row(self, old_row, new_row):
        self.delete_rows([old_row])
        self.add_row(new_row)


    def replace_data(self, items):
        self.delete(*self.get_children())
        self.fill_table(items)


    def get_selected_rows(self):
        return [self.item(iid)["values"] for iid in self.selection()]


    def delete_selection(self):
        for iid in self.selection():
            for i, item in enumerate(self.items):
                if item[0] == self.item(iid)["values"][0]:
                    self.items.pop(i)
                    break
            self.delete(iid)


    def delete_rows(self, rows):
        for iid in self.get_children():
            for row in rows:
                if row[0] == self.item(iid)["values"][0]:
                    i = self.items.index(row)
                    self.items.pop(i)
                    self.delete(iid)
                    break


    # Inspired by https://stackoverflow.com/questions/1966929/tk-treeview-column-sort
    def _sort_column(self, column, reverse):
        self.column = column
        self.reverse = reverse
        
        items = [(self.set(k, column), k) for k in self.get_children('')]
        if column in self.int_cols:
            items.sort(key=lambda item: int(item[0]), reverse=reverse)
        else:
            items.sort(reverse=reverse)

        for index, (val, k) in enumerate(items):
            self.move(k, '', index)

        self.heading(column, command=lambda _column=column: self._sort_column(_column, not reverse))


    # Inspired by https://stackoverflow.com/questions/45358408/how-to-disable-manual-resizing-of-tkinters-treeview-column
    def _handle_separator_click(self, event):
        if self.identify_region(event.x, event.y) == "separator":
            return "break"

