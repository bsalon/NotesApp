import tkinter as tk
import tkinter.ttk as ttk


# Inspired by https://stackoverflow.com/questions/58559865/tkinter-checkbutton-different-image

def app():
    # Remove the indicator from a customised TCheckbutton style layout
    s = ttk.Style()
    s.layout('no_indicatoron.TCheckbutton',
             [('Checkbutton.padding', {'sticky': 'nswe', 'children': [
                 ('Checkbutton.focus', {'side': 'left', 'sticky': 'w',
                                        'children':
                                        [('Checkbutton.label', {'sticky': 'nswe'})]})]})]
             )

    on_image = tk.PhotoImage(width=48, height=24)
    off_image = tk.PhotoImage(width=48, height=24)
    on_image.put(("green",), to=(0, 0, 23, 23))
    off_image.put(("red",), to=(24, 0, 47, 23))

    var2 = tk.StringVar(value="OFF")


    def cb2_state():
        cb2['image'] = on_image if cb2.instate(['!disabled', 'selected']) else off_image


    # Use the customised style and functions
    cb2 = ttk.Checkbutton(root, image=off_image, onvalue="ON", offvalue="OFF",
                          variable=var2, style='no_indicatoron.TCheckbutton',
                          textvariable=var2,
                          command=cb2_state)
    cb2.pack(padx=20, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app()
    root['background'] = 'white'  # for linux distro
    
    
    root.mainloop()
