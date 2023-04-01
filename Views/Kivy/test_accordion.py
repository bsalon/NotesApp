from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.app import App

from kivy.lang import Builder

Builder.load_string(
"""
[CustomTemplate@BoxLayout]:
    active:
        checkbox.active
    canvas.before:
        Color:
            rgb: 1, 1, 1
        BorderImage:
            source:
                # ctx.item.background_normal if ctx.item.collapse else ctx.item.background_selected
                ctx.item.background_normal if self.active else ctx.item.background_selected
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
        PopMatrix
    Label:
        text: ctx.item.name_text
    Label:
        text: ctx.item.time_text
    CheckBox:
        id: checkbox
        on_active: ctx.item.selected()
"""
)



class AccordionApp(App):
    def build(self):
        root = Accordion(orientation="vertical")
        for x in range(5):
            item = AccordionItem(title="container_title")
            item.name_text = "Name original"
            item.time_text = "Name original"
            item.selected = lambda i=item: print(i)
            item.title_template = "CustomTemplate"
            
            item.add_widget(Label(text='Very big content\n' * 10))
            root.add_widget(item)
        return root


if __name__ == '__main__':
    AccordionApp().run()


