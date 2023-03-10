import tkinter
import tkcalendar

from tkinter import ttk
from tkinter import simpledialog

import datetime


class FilterDialog(tkinter.simpledialog.Dialog):
    def __init__(self, master, fast_filter=None, *args, **kwargs):
        self.accepted = False
        self.fast_filter = fast_filter
        super(FilterDialog, self).__init__(master, *args, **kwargs)


    def body(self, frame):
        # Filter
        filter_name_label = tkinter.Label(frame, text="Filter name:", anchor="e")
        filter_name_label.grid(row=0, column=0, sticky="news")
        self.filter_name_entry = tkinter.Entry(frame, width=25)
        self.filter_name_entry.grid(row=0, column=1, columnspan=5, pady=(5, 5), sticky="news")

        filter_order_label = tkinter.Label(frame, text="Filter order:", anchor="e")
        filter_order_label.grid(row=1, column=0, sticky="news")
        self.filter_order_entry = tkinter.Entry(frame, width=25)
        self.filter_order_entry.grid(row=1, column=1, columnspan=5, pady=(5, 20), sticky="news")

        # Note name
        note_name_label = tkinter.Label(frame, text="Note name contains:", anchor="e")
        note_name_label.grid(row=2, column=0, sticky="news")
        self.note_name_entry = tkinter.Entry(frame, width=25)
        self.note_name_entry.grid(row=2, column=1, columnspan=5, pady=(5, 5), sticky="news")

        # Note date
        today = datetime.date.today()
        note_date_label = tkinter.Label(frame, text="Note date range:", anchor="e")
        note_date_label.grid(row=3, column=0, sticky="news")
        self.note_from_date_entry = tkcalendar.DateEntry(frame, selectmode="day", year=today.year, month=today.month, day=today.day)
        self.note_from_date_entry.grid(row=3, column=1, columnspan=2, pady=(5, 5), sticky="news")

        note_date_divider_label = tkinter.Label(frame, text="  -  ")
        note_date_divider_label.grid(row=3, column=3, sticky="news")
        self.note_to_date_entry = tkcalendar.DateEntry(frame, selectmode="day", year=today.year, month=today.month, day=today.day)
        self.note_to_date_entry.grid(row=3, column=4, columnspan=2, pady=(5, 5), sticky="news")

        # Note time
        note_time_label = tkinter.Label(frame, text="Note time (hh:mm) range:", anchor="e")
        note_time_label.grid(row=4, column=0, pady=(5, 5), sticky="news")
        self.note_from_time_hour_spinbox = tkinter.Spinbox(frame, from_=0, to=23, wrap=True, width=5, state="readonly", justify=tkinter.CENTER)
        self.note_from_time_hour_spinbox.grid(row=4, column=1, pady=(5, 5), sticky="news")
        self.note_from_time_minute_spinbox = tkinter.Spinbox(frame, from_=0, to=60, wrap=True, width=5, state="readonly", justify=tkinter.CENTER)
        self.note_from_time_minute_spinbox.grid(row=4, column=2, pady=(5, 5), sticky="news")
        
        note_time_divider_label = tkinter.Label(frame, text="  -  ")
        note_time_divider_label.grid(row=4, column=3, sticky="news")
        self.note_to_time_hour_spinbox = tkinter.Spinbox(frame, from_=0, to=23, wrap=True, width=5, state="readonly", justify=tkinter.CENTER)
        self.note_to_time_hour_spinbox.grid(row=4, column=4, pady=(5, 5), sticky="news")
        self.note_to_time_minute_spinbox = tkinter.Spinbox(frame, from_=0, to=60, wrap=True, width=5, state="readonly", justify=tkinter.CENTER)
        self.note_to_time_minute_spinbox.grid(row=4, column=5, pady=(5, 5), sticky="news")

        # Note text
        note_text_label = tkinter.Label(frame, text="Note text contains:", anchor="e")
        note_text_label.grid(row=5, column=0, pady=(5, 20), sticky="news")
        self.note_text_entry = tkinter.Entry(frame, width=25)
        self.note_text_entry.grid(row=5, column=1, columnspan=5, pady=(5, 20), sticky="news")

        # Priority
        note_priority_label = tkinter.Label(frame, text="Note priority range:", anchor="e")
        note_priority_label.grid(row=6, column=0, pady=(5, 20), sticky="news")
        self.note_min_priority_entry = tkinter.Entry(frame, width=25)
        self.note_min_priority_entry.grid(row=6, column=1, columnspan=2, pady=(5, 20), sticky="news")

        note_priority_divider_label = tkinter.Label(frame, text="  -  ")
        note_priority_divider_label.grid(row=6, column=3, pady=(5, 20), sticky="news")
        self.note_max_priority_entry = tkinter.Entry(frame, width=25)
        self.note_max_priority_entry.grid(row=6, column=4, columnspan=2, pady=(5, 20), sticky="news")

        # Category
        category_name_label = tkinter.Label(frame, text="Category name contains:", anchor="e")
        category_name_label.grid(row=7, column=0, sticky="news")
        self.category_name_entry = tkinter.Entry(frame, width=25)
        self.category_name_entry.grid(row=7, column=1, columnspan=5, pady=(5, 5), sticky="news")
        
        category_description_label = tkinter.Label(frame, text="Category description contains:", anchor="e")
        category_description_label.grid(row=8, column=0, sticky="news")
        self.category_description_entry = tkinter.Entry(frame, width=25)
        self.category_description_entry.grid(row=8, column=1, columnspan=5, pady=(5, 5), sticky="news")

        # Tag
        tag_name_label = tkinter.Label(frame, text="Tag name contains:", anchor="e")
        tag_name_label.grid(row=9, column=0, sticky="news")
        self.tag_name_entry = tkinter.Entry(frame, width=25)
        self.tag_name_entry.grid(row=9, column=1, columnspan=5, pady=(5, 5), sticky="news")
        
        tag_description_label = tkinter.Label(frame, text="Tag description contains:", anchor="e")
        tag_description_label.grid(row=10, column=0, sticky="news")
        self.tag_description_entry = tkinter.Entry(frame, width=25)
        self.tag_description_entry.grid(row=10, column=1, columnspan=5, pady=(5, 5), sticky="news")

        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(tuple(range(1, 6)), weight=1)

        if self.fast_filter:
            self.fill_dialog()

        return frame


    def fill_dialog(self):
        fast_filter = self.fast_filter
        self.filter_name_entry.insert(0, fast_filter.name)
        self.filter_order_entry.insert(0, str(fast_filter.order))
        self.note_name_entry.insert(0, fast_filter.note_name)
        self.note_from_date_entry.set_date(fast_filter.note_min_time.date())
        self.note_from_time_hour_spinbox.insert(0, str(fast_filter.note_min_time.hour))
        self.note_from_time_minute_spinbox.insert(0, str(fast_filter.note_min_time.minute))
        self.note_to_date_entry.set_date(fast_filter.note_max_time.date())
        self.note_to_time_hour_spinbox.insert(0, str(fast_filter.note_max_time.hour))
        self.note_to_time_minute_spinbox.insert(0, str(fast_filter.note_max_time.minute))
        self.note_min_priority_entry.insert(0, str(fast_filter.note_min_priority))
        self.note_max_priority_entry.insert(0, str(fast_filter.note_max_priority))
        self.note_text_entry.insert(0, fast_filter.note_text)
        self.category_name_entry.insert(0, fast_filter.tag_name)
        self.category_description_entry.insert(0, fast_filter.tag_description)
        self.tag_name_entry.insert(0, fast_filter.category_name)
        self.tag_description_entry.insert(0, fast_filter.category_description)


    def save_pressed(self):
        self.accepted = True
        self.data_dict = {
            "name": self.filter_name_entry.get(),
            "order": self.filter_order_entry.get(),
            "note_name" : self.note_name_entry.get(),
            "note_from_time" : self._get_selected_from_datetime(),
            "note_to_time": self._get_selected_to_datetime(),
            "note_min_priority": self.note_min_priority_entry.get(),
            "note_max_priority": self.note_max_priority_entry.get(),
            "note_text": self.note_text_entry.get(),
            "category_name": self.category_name_entry.get(),
            "category_description": self.category_description_entry.get(),
            "tag_name": self.tag_name_entry.get(),
            "tag_description": self.tag_description_entry.get(),
        }
        self.destroy()


    def _get_selected_from_datetime(self):
        date = self.note_from_date_entry.get_date()
        note_date = datetime.datetime.combine(date, datetime.datetime.min.time())
        note_datetime = note_date + datetime.timedelta(hours=int(self.note_from_time_hour_spinbox.get()),
                                                       minutes=int(self.note_from_time_minute_spinbox.get()))
        return note_datetime


    def _get_selected_to_datetime(self):
        date = self.note_to_date_entry.get_date()
        note_date = datetime.datetime.combine(date, datetime.datetime.min.time())
        note_datetime = note_date + datetime.timedelta(hours=int(self.note_to_time_hour_spinbox.get()),
                                                       minutes=int(self.note_to_time_minute_spinbox.get()))
        return note_datetime


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




def mydialog(app):
    dialog = AdvancedFilterDialog(title="Login", master=app)


def main():
    app.title('Dialog')
    answer = mydialog(app)
    app.mainloop()


if __name__ == "__main__":
    app = tkinter.Tk()
    main()

