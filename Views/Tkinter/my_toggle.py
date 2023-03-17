from tkinter import *


# Inspired by https://stackoverflow.com/questions/65480255/is-it-posible-to-create-toggle-switch-button-in-tkinter

class ToggleButton(Canvas):
    def __init__(self, master, command=None, on_bg="green", off_bg="red", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(width=100, height=50, borderwidth=0, highlightthickness=0)
        self.master = master
        self.on_bg = on_bg
        self.off_bg = off_bg
        
        self.oval = self.create_oval(0, 0, 0, 0, outline='black', width=2)
        self.btn = self.create_oval(0, 0, 0, 0, fill=self.on_bg, outline='black', width=2)
        self.btn_txt = self.create_text(10, 18, text="ON")

        self.bind('<Configure>', self._resize)
        self.bind('<Button>', self._animate, add='+')  
        self.bind('<Button>', command, add='+')

        self.state = 0


    def _resize(self, event):
        self.coords(self.oval, 5, 5, event.width-5, event.height-5)
        self.coords(self.btn, 5, 5, event.height-5, event.height-5)
        self.coords(self.btn_txt, 10, 18)
        self.moveto(self.btn_txt, 10, 18)

        if self.state:
            x, y, w, h = self.coords(self.btn)
            ox, oy, ow, oh = self.coords(self.oval)
            self.moveto(self.btn, ox+ow-w, 4)
            self.moveto(self.btn_txt, ox+ow-w+9, 18)
            self.itemconfig(self.btn, fill=self.off_bg)
            self.itemconfig(self.btn_txt, text="OFF")
            

    
    def _animate(self, event):
        x, y, w, h = self.coords(self.btn)
        ox, oy, ow, oh = self.coords(self.oval)
        x = int(x-1)
        y = int(y-1)
        
        if w == ow+1:
            self.moveto(self.btn, 4, 4)
            self.moveto(self.btn_txt, 10, 18)
            self.itemconfig(self.btn, fill=self.on_bg)
            self.itemconfig(self.btn_txt, text="ON")
            self.state = 0
        else:
            self.moveto(self.btn, ox+ow-w, 4)
            self.moveto(self.btn_txt, ox+ow-w+9, 18)
            self.itemconfig(self.btn, fill=self.off_bg)
            self.itemconfig(self.btn_txt, text="OFF")
            self.state = 1


    def get_state(self):
        return self.state



#Your own function
def hello(event='Nooo'):
    print(event)
    if bool(btn.get_state()):
        print('State is 1')

    elif not bool(btn.get_state()):
        print('State is 0')


if __name__ == "__main__":
    root = Tk()
    btn = ToggleButton(root, lambda _:hello('Hello'))
    btn.pack()
    root.mainloop()

