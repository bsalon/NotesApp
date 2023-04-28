import tkinter
import tkcalendar

from tkinter import ttk
from tkinter import simpledialog

import datetime


class SettingsDialog(tkinter.simpledialog.Dialog):
    def __init__(self, master, *args, **kwargs):
        self.accepted = False
        super(SettingsDialog, self).__init__(master, title="Select GUI library", *args, **kwargs)


    def body(self, frame):
        frame.configure(bg="#d7eb5a")

        info_label = tkinter.Label(frame, text="Saving with different than current library will restart the application", bg="#d7eb5a", fg="red")
        info_label.grid(row=0, column=0, sticky="news", pady=(0, 20))


        # Radio buttons
        self.gui_library = tkinter.IntVar()

        qt_radiobutton = tkinter.Radiobutton(frame, text="PySide", variable=self.gui_library, value=0, bg="#d7eb5a", fg="black")
        qt_radiobutton.grid(row=1, column=0, pady=(5, 5))
        
        tk_radiobutton = tkinter.Radiobutton(frame, text="Tkinter", variable=self.gui_library, value=1, bg="#d7eb5a", fg="black")
        tk_radiobutton.grid(row=2, column=0, pady=(5, 5))
        
        kv_radiobutton = tkinter.Radiobutton(frame, text="Kivy", variable=self.gui_library, value=2, bg="#d7eb5a", fg="black")
        kv_radiobutton.grid(row=3, column=0, pady=(5, 5))

        self.gui_library.set(1)

        self.resizable(False, False)

        return frame


    def save_pressed(self):
        self.accepted = True
        self.data_dict = {
            "library" : self.gui_library.get()
        }
        self.destroy()


    def cancel_pressed(self):
        self.destroy()


    def buttonbox(self):
        self.configure(bg="#d7eb5a")
        self.ok_button = tkinter.Button(self, text='Save', width=5, command=self.save_pressed)
        self.ok_button.pack(side="top")
        cancel_button = tkinter.Button(self, text='Cancel', width=5, command=self.cancel_pressed)
        cancel_button.pack(side="bottom")
        self.bind("<Return>", lambda event: self.save_pressed())
        self.bind("<Escape>", lambda event: self.cancel_pressed())




def mydialog(app):
    dialog = SettingsDialog(master=app)


def main():
    app.title('Dialog')
    answer = mydialog(app)
    app.mainloop()


if __name__ == "__main__":
    app = tkinter.Tk()
    main()

