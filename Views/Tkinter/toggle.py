from tkinter import *

window = Tk()
window.title("Start/Stop Button")
window.geometry('200x100')

class Christina(Frame):
    def __init__(self, master=None, **kwargs):
        Frame.__init__(self, master, **kwargs)

        self.btn = Button(self, text="Start", command=self.clicked)
        self.btn.grid(column=0, row=0)
        self.lbl = Label(self, text="   OFF", bg="red")
        self.lbl.grid(column=1, row=0)

    def clicked(self):
        if self.btn['text'] == "Start":
            self.btn.configure(text="Stop")
            self.lbl.configure(text="ON    ", bg="green")
        else:
            self.btn.configure(text="Start")
            self.lbl.configure(text="   OFF", bg="red")

btn1 = Christina(window)
btn1.grid()
btn2 = Christina(window)
btn2.grid()
btn3 = Christina(window)
btn3.grid()

window.mainloop()
