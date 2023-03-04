import tkinter as tk

def toggle():
    if var.get() == "ON":
        print("turning on...")
    else:
        print("turning off...")

root = tk.Tk()
var = tk.StringVar()
toggle = tk.Checkbutton(root, onvalue="ON", offvalue="OFF", width=8,
                        indicatoron=False, 
                        variable=var, textvariable=var,
                        selectcolor="green", background="red",
                        command=toggle)

var.set("OFF")
toggle.pack()

root.mainloop()
