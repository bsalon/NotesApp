from tkinter import *


# Inspired by https://stackoverflow.com/questions/65480255/is-it-posible-to-create-toggle-switch-button-in-tkinter

class ToggleButton(Canvas):
    def __init__(self, master, command=None, fg='red', bg='green', *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configure(width=100, height=50, borderwidth=0, highlightthickness=0)
        self.master = master
        
        self.bg_left = self.create_arc((0, 0, 0, 0), start=90, extent=180, fill=bg, outline='')
        self.bg_right = self.create_arc((0, 0, 0, 0), start=-90, extent=180, fill=bg, outline='')
        self.rect = self.create_rectangle(0, 0, 0, 0, fill=bg, outline='')
        
        self.btn = self.create_oval(0, 0, 0, 0, fill=fg, outline='')
        self.btn_txt = self.create_text(6, 5, text="ON")

        self.bind('<Configure>', self._resize)
        self.bind('<Button>', self._animate, add='+')  
        self.bind('<Button>', command, add='+')

        self.state = 0


    def _resize(self, event):
        self.coords(self.bg_left, 5, 5, event.height-5, event.height-5)
        self.coords(self.bg_right, 5, 5, event.height, event.height-5)
       
        factor = event.width-(self.coords(self.bg_right)[2]-self.coords(self.bg_right)[0])-10
        self.move(self.bg_right, factor, 0)

        self.coords(self.rect, self.bbox(self.bg_left)[2]-2, 5, self.bbox(self.bg_right)[0]+2, event.height-5)
        self.coords(self.btn, 5, 5, event.height-5, event.height-5)
        
        self.coords(self.btn_txt, 7, 18)
        self.moveto(self.btn_txt, 7, 18)

        if self.state:
            self.moveto(self.btn, self.coords(self.bg_right)[0]+4, 4)
            self.moveto(self.btn_txt, self.coords(self.bg_right)[0]+9, 18)
            self.itemconfig(self.text_id, text="OFF")
            

    
    def _animate(self, event):
        x, y, w, h = self.coords(self.btn)
        x = int(x-1)
        y = int(y-1)
        
        if x == self.coords(self.bg_right)[0]+3:
            self.moveto(self.btn, 4, 4)
            self.moveto(self.btn_txt, 7, 18)
            self.itemconfig(self.btn_txt, text="ON")

            self.itemconfig(self.bg_left, fill="green")
            self.itemconfig(self.bg_right, fill="green")
            
            self.state = 0
        else:
            self.moveto(self.btn, self.coords(self.bg_right)[0]+4, 4)
            self.moveto(self.btn_txt, self.coords(self.bg_right)[0]+9, 18)
            self.itemconfig(self.btn_txt, text="OFF")
            
            self.itemconfig(self.bg_left, fill="green")
            self.itemconfig(self.bg_right, fill="green")
            
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
    
root = Tk()


btn = ToggleButton(root, lambda _:hello('Hello'), 'green', 'grey')
btn.pack()

root.mainloop() 
