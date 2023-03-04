import tkinter
import tkcalendar

from tkinter import ttk
from tkinter import simpledialog

import datetime


class NoteDialog(tkinter.simpledialog.Dialog):
    def __init__(self, master, *args, **kwargs):
        super(NoteDialog, self).__init__(master, *args, **kwargs)
        self.categories_names = []
        self.tags_names = []


    def body(self, frame):
        # Name
        name_label = tkinter.Label(frame, text="Name:", anchor="e")
        name_label.grid(row=0, column=0, sticky="news")
        self.name_entry = tkinter.Entry(frame, width=25)
        self.name_entry.grid(row=0, column=1, columnspan=2, pady=(5, 5))

        # Date and time
        today = datetime.date.today()

        date_label = tkinter.Label(frame, text="Date:", anchor="e")
        date_label.grid(row=1, column=0, sticky="news")
        self.date_entry = tkcalendar.DateEntry(frame, selectmode="day", year=today.year, month=today.month, day=today.day)
        self.date_entry.grid(row=1, column=1, columnspan=2, pady=(5, 5), sticky="news")

        time_label = tkinter.Label(frame, text="Time (hh:mm):", anchor="e")
        time_label.grid(row=2, column=0, pady=(5, 5), sticky="news")
        self.time_hour_spinbox = tkinter.Spinbox(frame, from_=0, to=23, wrap=True, width=5, state="readonly", justify=tkinter.CENTER)
        self.time_hour_spinbox.grid(row=2, column=1, pady=(5, 5), sticky="news")
        self.time_minute_spinbox = tkinter.Spinbox(frame, from_=0, to=60, wrap=True, width=5, state="readonly", justify=tkinter.CENTER)
        self.time_minute_spinbox.grid(row=2, column=2, pady=(5, 5), sticky="news")

        # Text
        text_label = tkinter.Label(frame, text="Text:", anchor="e")
        text_label.grid(row=3, column=0, pady=(5, 20), sticky="news")
        self.text_entry = tkinter.Entry(frame, width=25)
        self.text_entry.grid(row=3, column=1, columnspan=2, pady=(5, 20))

        # Priority radio buttons
        priority_label = tkinter.Label(frame, text="Assign priority:", anchor="e")
        priority_label.grid(row=4, column=0, pady=(5, 5), sticky="news")
        self.assign_priority = tkinter.IntVar()
        yes_radiobutton = tkinter.Radiobutton(frame, text="Yes", variable=self.assign_priority, value=1, command=self._slider_enabling)
        yes_radiobutton.grid(row=4, column=1, pady=(5, 5))
        no_radiobutton = tkinter.Radiobutton(frame, text="No", variable=self.assign_priority, value=2, command=self._slider_enabling)
        no_radiobutton.grid(row=4, column=2, pady=(5, 5))

        # Priority slider
        self.priority_slider = tkinter.Scale(frame, from_=0, to=100, orient=tkinter.HORIZONTAL)
        self.priority_slider.grid(row=5, column=1, columnspan=2, pady=(5, 20), sticky="news")

        # Categories
        self.categories_label = tkinter.Label(frame, text="Select category:", anchor="e")
        self.categories_label.grid(row=6, column=0, pady=(5, 5), sticky="news")
        self.categories_combobox = ttk.Combobox(frame, width = 25)
        self.categories_combobox["values"] = ["1","1","1","1",] # TODO categories
        self.categories_combobox.grid(row=6, column=1, columnspan=2, pady=(5, 5))
        self.categories_combobox.current(0)

        # Tags
        self.tags_label = tkinter.Label(frame, text="Select tags:", anchor="e")
        self.tags_label.grid(row=7, column=0, pady=(5, 5), sticky="news")
        self.tags = tkinter.Variable(value=["a","b","c","d","e","f","g","h","i"]) # TODO tags
        self.tags_listbox = tkinter.Listbox(frame, listvariable=self.tags, height = 3, selectmode="multiple")
        self.tags_listbox.grid(row=7, column=1, columnspan=2, pady=(5, 5))

        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(tuple(range(1, 3)), weight=1)

        return frame


    def save_pressed(self):
        self.data_dict = {
            "name" : self.name_entry.get(),
            "time" : self._get_selected_datetime(),
            "text" : self.text_entry.get(),
            "priority" : self.priority_slider.get(),
            "category" : self.categories_combobox.get(),
            "tags" : self._get_selected_tags()
        }
        print(self.data_dict)
        self.destroy()


    def _get_selected_datetime(self):
        date = self.date_entry.get_date()
        note_date = datetime.datetime.combine(date, datetime.datetime.min.time())
        note_datetime = note_date + datetime.timedelta(hours=int(self.time_hour_spinbox.get()),
                                                       minutes=int(self.time_minute_spinbox.get()))
        return note_datetime


    def _get_selected_tags(self):
        return [self.tags_listbox.get(i) for i in self.tags_listbox.curselection()]


    def cancel_pressed(self):
        self.destroy()


    def buttonbox(self):
        self.ok_button = tkinter.Button(self, text='Save', width=5, command=self.save_pressed)
        self.ok_button.pack(side="top")
        cancel_button = tkinter.Button(self, text='Cancel', width=5, command=self.cancel_pressed)
        cancel_button.pack(side="bottom")
        self.bind("<Return>", lambda event: self.save_pressed())
        self.bind("<Escape>", lambda event: self.cancel_pressed())


    def fill_dialog(self):
        pass


    def _slider_enabling(self):
        if self.assign_priority.get() == 1:
            self.priority_slider.grid()
        else:
            self.priority_slider.set(0)
            self.priority_slider.grid_remove()


def mydialog(app):
    dialog = NoteDialog(title="Login", master=app)


def main():
    app.title('Dialog')
    answer = mydialog(app)
    app.mainloop()


app = tkinter.Tk()

main()
