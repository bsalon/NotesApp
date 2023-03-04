import tkinter

root = tkinter.Tk()
root.geometry("800x600")

image = tkinter.PhotoImage("TodaysNotesIcon.png")
tkinter.Label(root, image=image).pack()

root.mainloop()
