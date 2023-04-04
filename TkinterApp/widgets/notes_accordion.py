import tkinter
from tkinter import ttk 

from TkinterApp.widgets import scrollable_frame


class NotesAccordion(scrollable_frame.ScrollableFrame):
    def __init__(self, master, notes, *args, **kwargs):
        super(NotesAccordion, self).__init__(master, *args, **kwargs)
        self.notes = notes
        self._add_rows(notes)


    def replace_rows(self, notes):
        for widget in self.interior.winfo_children():
            widget.destroy()
        self._add_rows(notes)


    def get_selected_notes(self):
        selected_notes = []
        for (index, row) in enumerate(self.rows):
            if row.checked_row.get() == 1:
                selected_notes.append(self.notes[index])
        return selected_notes


    def _add_rows(self, notes):
        self.notes = notes
        self.rows = []
        for (index, note) in enumerate(notes):
            row = CollapsableFrameRow(self.interior)
            self._add_note_to_row(row, note)
            row.bind("<<CollapsableFrameRowCheck>>", lambda e: self.event_generate("<<RowCheck>>"))
            row.grid(row=index, column=0, sticky="nsew")
            self.rows.append(row)
        self.interior.grid_columnconfigure(0, weight=1)
        if len(notes) > 0:
            self.interior.grid_rowconfigure(tuple(range(len(notes))), weight=1)


    def _add_note_to_row(self, row, note):
        row.add_title_content(note)
        row.add_content(note)
    


class CollapsableFrameRow(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super(CollapsableFrameRow, self).__init__(master, *args, **kwargs)
        self.show = tkinter.IntVar()
        self.show.set(1)

        self.title_frame = ttk.Frame(self, style="collapsable_frame_row.TFrame")
        self.title_frame.grid(sticky="news")
        
        self.title_frame.grid_columnconfigure((0, 1), weight=1)
        self.title_frame.grid_rowconfigure(0, weight=1)

        self.content_frame = ttk.Frame(self, relief="sunken", borderwidth=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(tuple(range(4)), weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


    def add_title_content(self, note):
        name_label = ttk.Label(self.title_frame, text=note.name, style="collapsable_frame_label.TLabel", anchor="w")
        note_time = ttk.Label(self.title_frame, text=note.time.strftime("%d/%m/%Y %H:%M"), style="collapsable_frame_label.TLabel")
        self.checked_row = tkinter.IntVar()
        self.check_button = ttk.Checkbutton(self.title_frame, variable=self.checked_row, style="collapsable_frame_checkbutton.TCheckbutton", command = lambda: self.event_generate("<<CollapsableFrameRowCheck>>"))
        self.toggle_button = ttk.Button(self.title_frame, text=" + ", command=self.toggle, style="collapsable_frame_button.TButton")

        name_label.grid(row=0, column=0, sticky="news", padx=(5, 0), pady=(2, 2))
        note_time.grid(row=0, column=1, sticky="news", pady=(2, 2))
        self.check_button.grid(row=0, column=2, sticky="news", pady=(2, 2))
        self.toggle_button.grid(row=0, column=3, sticky="news", padx=(4, 4), pady=(4, 4))


    def add_content(self, note):
        text_label = ttk.Label(self.content_frame, text = f"Text:   {note.text}", style="collapsable_frame_content_label.TLabel", anchor="w")
        priority_label = ttk.Label(self.content_frame, text = f"Priority:   {note.priority}", style="collapsable_frame_content_label.TLabel", anchor="w")
        category_label = ttk.Label(self.content_frame, text = f"Category:   {note.category.name}", style="collapsable_frame_content_label.TLabel", anchor="w")
        tags_string = " ".join(note.tags)
        tags_label = ttk.Label(self.content_frame, text = f"Tags:   {tags_string}", style="collapsable_frame_content_label.TLabel", anchor="w")

        text_label.grid(row=0, column=0, sticky="news")
        priority_label.grid(row=1, column=0, sticky="news")
        category_label.grid(row=2, column=0, sticky="news")
        tags_label.grid(row=3, column=0, sticky="news")


    def toggle(self):
        if bool(self.show.get()):
            self.content_frame.grid(sticky="news")
            self.toggle_button.configure(text=" - ")
            self.show.set(0)
        else:
            self.content_frame.grid_forget()
            self.toggle_button.configure(text=" + ")
            self.show.set(1)



if __name__ == "__main__":
    root = tkinter.Tk()
    
    t = CollapsableFrame(root, text='Rotate', relief="raised", borderwidth=1)
    t.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
    ttk.Label(t.content_frame, text='Rotation [deg]:').pack(side="left", fill="x", expand=1)
    ttk.Entry(t.content_frame).pack(side="left")

    t2 = CollapsableFrame(root, text='Resize', relief="raised", borderwidth=1)
    t2.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
    for i in range(10):
        ttk.Label(t2.content_frame, text='Test' + str(i)).pack()

    root.mainloop()
