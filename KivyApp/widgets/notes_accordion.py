from kivy import metrics

from kivy.uix import accordion, scrollview

from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.boxlayout import BoxLayout

from kivy.lang import Builder

import pathlib


Builder.load_string(
"""
<NotesAccordionItemContent>:
    orientation: "vertical"
    spacing: 10
    canvas.before:
        Color:
            rgba: 247/255, 250/255, 222/255, 255/255
        Rectangle:
            pos: self.pos
            size: self.size


[CustomTemplate@BoxLayout]:
    selected:
        checkbox.active
    canvas.before:
        Color:
            rgb: 1, 1, 1
        BorderImage:
            source:
                ctx.item.background_selected if self.selected else ctx.item.background_normal
            pos: self.pos
            size: self.size
        PushMatrix
        Translate:
            xy: self.center_x, self.center_y
        Rotate:
            angle: 90 if ctx.item.orientation == 'horizontal' else 0
            axis: 0, 0, 1
        Translate:
            xy: -self.center_x, -self.center_y
    canvas.after:
        Color:
            rgba: 0, 0, 0, 1
        Line:
            width: 1
            rectangle: self.x, self.y, self.width, self.height
        PopMatrix
    Label:
        color: (0, 0, 0, 1)
        text: ctx.item.name_text
        halign: "left"
        on_size:
            self.text_size = self.size
        padding: (5, 10)
    Label:
        color: (0, 0, 0, 1)
        text: ctx.item.time_text
    CheckBox:
        id: checkbox
        color: (0, 0, 0, 1)
        on_active: ctx.item.check_function()
"""
)


class NotesAccordionBox(BoxLayout):
    def __init__(self, notes, row_selection_function, *args, **kwargs):
        super(NotesAccordionBox, self).__init__(*args, **kwargs)
        self.notes_accordion = NotesAccordion(notes, row_selection_function, size_hint_y=None, height=metrics.dp(600))
        
        scrollable_accordion = scrollview.ScrollView(size_hint=(1, 1))
        scrollable_accordion.add_widget(self.notes_accordion)
        
        self.add_widget(scrollable_accordion)


    def get_selected_notes(self):
        return self.notes_accordion.selected_rows


    def replace_rows(self, notes):
        self.notes_accordion.create_items(notes)



class NotesAccordion(accordion.Accordion):
    def __init__(self, notes, row_selection_function, *args, **kwargs):
        super(NotesAccordion, self).__init__(orientation="vertical", *args, **kwargs)
        self.create_items(notes)
        self.row_selection_function = row_selection_function
        self.selected_rows = []

    
    def create_items(self, notes):
        self.clear_widgets()
        self.selected_rows = []
        for note in notes:
            row = NotesAccordionItem(note)
            row.check_function = lambda n=note: self.row_checked(n)
            row.title_template = "CustomTemplate"

            content = NotesAccordionItemContent()
            
            note_text = Label(color="black", markup=True, halign="left", text=f"[b]Text:[/b] {note.text}", padding=(5, 10))
            note_text.bind(size=note_text.setter("text_size"))
            content.add_widget(note_text)
            
            note_priority = Label(color="black", markup=True, halign="left", text=f"[b]Priority:[/b] {note.priority}", padding=(5, 10))
            note_priority.bind(size=note_priority.setter("text_size"))
            content.add_widget(note_priority)
            
            note_category = Label(color="black", markup=True, halign="left", text=f"[b]Category:[/b] {note.category.name}", padding=(5, 10))
            note_category.bind(size=note_category.setter("text_size"))
            content.add_widget(note_category)
            
            tags_string = " ".join(note.tags)
            note_tags = Label(color="black", markup=True, halign="left", text=f"[b]Tags:[/b] {tags_string}", padding=(5, 10))
            note_tags.bind(size=note_tags.setter("text_size"))
            content.add_widget(note_tags)
            
            row.add_widget(content)
            self.add_widget(row)


    def row_checked(self, note):
        if note in self.selected_rows:
            index = self.selected_rows.index(note)
            self.selected_rows.pop(index)
        else:
            self.selected_rows.append(note)
        self.row_selection_function()


class NotesAccordionItem(accordion.AccordionItem):
    def __init__(self, note, *args, **kwargs):
        image_dir_path = pathlib.Path(__file__).parent.parent.parent / "Images"
        
        bg_normal_path = image_dir_path / "ColorE9F29B.png"
        bg_select_path = image_dir_path / "ColorD7EB5A.png"
        super(NotesAccordionItem, self).__init__(background_normal = bg_normal_path.resolve().as_posix(), background_selected = bg_select_path.resolve().as_posix(), *args, **kwargs)
        self.name_text = note.name
        self.time_text = note.time.strftime("%d/%m/%Y %H:%M")


class NotesAccordionItemContent(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(NotesAccordionItemContent, self).__init__(*args, **kwargs)

