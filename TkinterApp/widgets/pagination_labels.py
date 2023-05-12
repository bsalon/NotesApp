import math

import tkinter
from tkinter import ttk


class PaginationLabels(tkinter.Frame):
    """
    Pagination for the accordion

    Methods are used to change the current page
    """

    def __init__(self, master, page_size, items_count, *args, **kwargs):
        super(PaginationLabels, self).__init__(master, *args, **kwargs)
        self.page_size = page_size
        self.items_count = items_count
        
        self.master = master
        self.args = args
        self.kwargs = kwargs

        self.current_page = 1
        self.create_labels()

    
    def create_labels(self):
        self.clear_frame()

        last_page = self.pages_count()
        prev_page = 1 if self.current_page - 1 < 1 else self.current_page - 1
        next_page = last_page if self.current_page + 1 > last_page else self.current_page + 1

        list_pages = {1, prev_page, self.current_page, next_page, last_page}

        self.prev_page_label = ttk.Label(self, text="<<", style="pagination.TLabel")
        self.prev_page_label.bind("<Button-1>", self.go_to_prev_page)

        list_labels = [self.prev_page_label]
        for page in list_pages:
            page_label = ttk.Label(self, text=str(page), style="pagination.TLabel")
            if page == self.current_page:
                page_label.configure(style="pagination_current_page.TLabel")
            page_label.bind("<Button-1>", lambda e, p=page: self.go_to_page(p))
            list_labels.append(page_label)

        self.next_page_label = ttk.Label(self, text=">>", style="pagination.TLabel")
        self.next_page_label.bind("<Button-1>", self.go_to_next_page)
        list_labels.append(self.next_page_label)

        for col, label in enumerate(list_labels):
            label.grid(row=0, column=col)


    def pages_count(self):
        return math.ceil(self.items_count / self.page_size)


    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()
    

    def go_to_prev_page(self, event):
        self.current_page -= 1
        self.current_page = self.current_page if self.current_page >= 1 else 1
        self.event_generate("<<PageChanged>>")
        self.create_labels()


    def go_to_next_page(self, event):
        last_page = self.pages_count()
        self.current_page += 1
        self.current_page = self.current_page if self.current_page <= last_page else last_page
        self.event_generate("<<PageChanged>>")
        self.create_labels()


    def go_to_page(self, page):
        self.current_page = page
        self.event_generate("<<PageChanged>>")
        self.create_labels()


if __name__ == "__main__":
    app = tkinter.Tk()
    frame = PaginationLabels(app, 5, 150)
    frame.grid()
    app.mainloop()
