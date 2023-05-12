import tkinter
import tkcalendar

from tkinter import ttk
from tkinter import simpledialog

import datetime


class TagDialog(tkinter.simpledialog.Dialog):
    def __init__(self, master, tag=None, *args, **kwargs):
        """
        Initializes tag dialog
        """

        self.accepted = False
        self.tag = tag
        super(TagDialog, self).__init__(master, title="Tag dialog", *args, **kwargs)


    def body(self, frame):
        """
        Puts all dialog widgets into the dialog frame
        """

        frame.configure(bg="#d7eb5a")
        
        # Name
        name_label = tkinter.Label(frame, text="Name:", bg="#d7eb5a", fg="black")
        name_label.grid(row=0, column=0, sticky="news")
        self.name_entry = tkinter.Entry(frame, width=25)
        self.name_entry.grid(row=0, column=1, columnspan=2, pady=(5, 5))

        # Description
        description_label = tkinter.Label(frame, text="Description:", bg="#d7eb5a", fg="black")
        description_label.grid(row=3, column=0, pady=(5, 20), sticky="news")
        self.description_entry = tkinter.Entry(frame, width=25)
        self.description_entry.grid(row=3, column=1, columnspan=2, pady=(5, 20))

        if self.tag:
            self.fill_dialog()

        self.resizable(False, False)

        return frame


    def save_pressed(self):
        """
        Fills data_dict property with field values and closes the dialog
        """

        if not self._validate():
            return
        self.accepted = True
        self.data_dict = {
            "name" : self.name_entry.get(),
            "description" : self.description_entry.get(),
        }
        self.destroy()


    def _validate(self):
        """
        Validates name field
        """

        return self._validate_field(self.name_entry)


    def _validate_field(self, field):
        """
        Validates field value by testing if its empty

        :param field: Field to be validated

        :return: True if field value is not empty False otherwise
        """

        if field.get() == "" or field.get().isspace():
            field.config({"background": "#ff7f7f"})
            return False
        field.config({"background": "White"})
        return True


    def cancel_pressed(self):
        """
        Closes the dialog
        """

        self.accepted = False
        self.destroy()


    def buttonbox(self):
        """
        Creates buttons for dialog
        """

        self.configure(bg="#d7eb5a")
        self.ok_button = tkinter.Button(self, text='Save', width=5, command=self.save_pressed)
        self.ok_button.pack(side="top")
        cancel_button = tkinter.Button(self, text='Cancel', width=5, command=self.cancel_pressed)
        cancel_button.pack(side="top")
        self.bind("<Return>", lambda event: self.save_pressed())
        self.bind("<Escape>", lambda event: self.cancel_pressed())


    def fill_dialog(self):
        """
        Fills dialog fields with tag values
        """

        tag = self.tag
        self.name_entry.insert(0, tag.name)
        self.description_entry.insert(0, tag.description)


def mydialog(app):
    dialog = TagDialog(title="Login", master=app)


def main():
    app.title('Dialog')
    answer = mydialog(app)
    app.mainloop()


if __name__ == "__main__":
    app = tkinter.Tk()
    main()

