import tkinter as tk
from tkinter import ttk


# root window
root = tk.Tk()
root.geometry('300x200')
root.resizable(False, False)
root.title('Spinbox Demo')

# Spinbox
current_value = tk.StringVar(value=0)
spin_box = ttk.Spinbox(
    root,
    from_=0,
    to=30,
    wrap=True)

spin_box.pack()
print(type(spin_box.get()))
print(spin_box.get())

root.mainloop()
