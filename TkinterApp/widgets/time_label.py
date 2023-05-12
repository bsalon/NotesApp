import tkinter
from tkinter import ttk

from datetime import datetime


# Inspired by https://www.geeksforgeeks.org/python-create-a-digital-clock-using-tkinter/
class TimeLabel(ttk.Label):
    """
    Current time with seconds precision
    """

    def __init__(self, master, *args, **kwargs):
        super(TimeLabel, self).__init__(master, *args, **kwargs)
        self.configure(justify="center")
        self.tick()

    def tick(self):
        time_text = datetime.now().strftime("%d-%m-%Y\n%H:%M:%S")
        self.config(text=time_text)
        self.after(1000, self.tick)


if __name__ == "__main__":
    root = tkinter.Tk()
    
    label = TimeLabel(root)
    label.grid(anchor="center")
    
    root.mainloop()
