import tkinter
from tkinter import ttk 


class NotesAccordion(tkinter.Frame):
    def __init__(self, master, notes, *args, **kwargs):
        super(CollapsableFrame, self).__init__(master, *args, **kwargs)
        self.master = master
        self.notes = notes
        self._add_rows(notes)


    def replace_rows(self, notes):
        self.destroy()
        super(CollapsableFrame, self).__init__(self.master, *args, **kwargs)
        self._add_rows(notes)


    def get_selected_notes(self):
        selected_notes = []
        for (index, row) in enumerate(self.rows):
            if row.check_button.checked_row == 1:
                selected_notes.append(self.notes[index])
        return selected_notes


    def _add_rows(self, notes):
        self.notes = notes
        self.rows = []
        for note in notes:
            row = CollapsableFrameRow(self)
            self._add_note_to_row(row, note)
            row.check_button.bind("<ButtonRelease-1>", lambda e: self.event_generate("<<RowCheck>>"))
            self.rows.append(row)


    def _add_note_to_row(self, row, note):
        row.add_title_content(note)
        row.add_content(note)
    


class CollapsableFrameRow(tkinter.Frame):
    def __init__(self, master, *args, **kwargs):
        super(CollapsableFrame, self).__init__(master, *args, **kwargs)
        self.show = tkinter.IntVar()
        self.show.set(1)

        self.title_frame = tkinter.Frame(self)
        self.title_frame.pack(fill="x", expand=1)

        self.content_frame = tkinter.Frame(self, relief="sunken", borderwidth=1)


    def add_title_content(self, note):
        name_label = tkinter.Label(self.title_frame, text = note.name)
        note_time = tkinter.Label(self.title_frame, text = note.time.strftime("%d/%m/%Y %H:%M"))
        self.checked_row = Tkinter.IntVar()
        self.check_button = Tkinter.Checkbutton(self.title_frame, variable=self.checked_row)
        self.check_button.state(['!alternate']) 
        self.toggle_button = tkinter.Button(self.title_frame, text=" + ", command=self.toggle)

        name_label.pack(side="left", fill="x", expand=1)
        note_time.pack(side="left", fill="x", expand=1)
        self.check_button.pack(side="left")
        self.toggle_button.pack(side="left")


    def add_content(self, note):
        text_label = tkinter.Label(self.content_frame, text = f"Text: {note.text}")
        priority_label = tkinter.Label(self.content_frame, text = f"Priority: {note.priority}")
        category_label = tkinter.Label(self.content_frame, text = f"Category: {note.category.name}")
        tags_string = " ".join(note.tags)
        tags_label = tkinter.Label(self.content_frame, text = f"Tags: {tags_string}")

        text_label.pack()
        priority_label.pack()
        category_label.pack()
        tags_label.pack()


    def toggle(self):
        if bool(self.show.get()):
            self.content.pack(fill="x", expand=1)
            self.toggle_button.configure(text=" - ")
            self.show.set(0)
        else:
            self.content.forget()
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
