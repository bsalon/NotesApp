import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *


# Copied from https://stackoverflow.com/questions/16188420/tkinter-scrollbar-for-frame
# Based on
#   https://web.archive.org/web/20170514022131id_/http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame

class ScrollableFrame(ttk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """
    def __init__(self, parent, *args, **kw):
        super(ScrollableFrame, self).__init__(parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)

        canvas = tk.Canvas(self, bd=0, highlightthickness=1, highlightbackground="black", yscrollcommand=vscrollbar.set, bg="#f1f6be")
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)

        vscrollbar.config(command=canvas.yview)

        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it
        self.interior = interior = ttk.Frame(canvas, style="scrollable_interior.TFrame")
        interior_id = canvas.create_window(0, 0, window=interior, anchor="nw")

        # Track changes to the canvas and frame width and sync them, also updating the scrollbar
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            # Update the inner frame's width to fill the canvas
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


if __name__ == "__main__":
    class SampleApp(tk.Tk):
        def __init__(self, *args, **kwargs):
            root = tk.Tk.__init__(self, *args, **kwargs)

            self.frame = VerticalScrolledFrame(root)
            self.frame.pack()
            self.label = ttk.Label(self, text="Shrink the window to activate the scrollbar.")
            self.label.pack()
            buttons = []
            for i in range(10):
                buttons.append(ttk.Button(self.frame.interior, text="Button " + str(i)))
                buttons[-1].pack()

    app = SampleApp()
    app.mainloop()
