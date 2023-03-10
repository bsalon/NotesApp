import tkinter
import tkcalendar

from tkinter import ttk
from tkinter import simpledialog

import datetime


class CategoryDialog(tkinter.simpledialog.Dialog):
    def __init__(self, master, category=None, *args, **kwargs):
        self.accepted = False
        self.category = category
        super(CategoryDialog, self).__init__(master, *args, **kwargs)


    def body(self, frame):
        # Name
        name_label = tkinter.Label(frame, text="Name:", anchor="e")
        name_label.grid(row=0, column=0, sticky="news")
        self.name_entry = tkinter.Entry(frame, width=25)
        self.name_entry.grid(row=0, column=1, columnspan=2, pady=(5, 5))

        # Description
        description_label = tkinter.Label(frame, text="Description:", anchor="e")
        description_label.grid(row=3, column=0, pady=(5, 20), sticky="news")
        self.description_entry = tkinter.Entry(frame, width=25)
        self.description_entry.grid(row=3, column=1, columnspan=2, pady=(5, 20))

        if self.category:
            self.fill_dialog()

        return frame


    def save_pressed(self):
        self.accepted = True
        self.data_dict = {
            "name" : self.name_entry.get(),
            "description" : self.description_entry.get(),
        }
        self.destroy()


    def cancel_pressed(self):
        self.accepted = False
        self.destroy()


    def buttonbox(self):
        self.ok_button = tkinter.Button(self, text='Save', width=5, command=self.save_pressed)
        self.ok_button.pack(side="top")
        cancel_button = tkinter.Button(self, text='Cancel', width=5, command=self.cancel_pressed)
        cancel_button.pack(side="top")
        self.bind("<Return>", lambda event: self.save_pressed())
        self.bind("<Escape>", lambda event: self.cancel_pressed())


    def fill_dialog(self):
        category = self.category
        self.name_entry.insert(0, category.name)
        self.description_entry.insert(0, category.description)


def mydialog(app):
    dialog = CategoryDialog(title="Login", master=app)


def main():
    app.title('Dialog')
    answer = mydialog(app)
    app.mainloop()


if __name__ == "__main__":
    app = tkinter.Tk()
    main()

