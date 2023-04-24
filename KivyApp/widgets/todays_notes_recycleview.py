from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix import boxlayout


Builder.load_string('''
<TodaysNotesRecycleview>:
    canvas.before:
        Color:
            rgba: (241/255, 246/255, 190/255, 255/255)
        Rectangle:
            pos: self.pos
            size: self.size

    RecycleBoxLayout:
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
''')


# https://stackoverflow.com/questions/45830039/kivy-python-multiple-widgets-in-recycleview-row

class TodaysNotesRow(RecycleDataViewBehavior, GridLayout):
    def __init__(self, *args, **kwargs):
        super(TodaysNotesRow, self).__init__(*args, **kwargs)
        self.cols = 1
        self.index = None
        self.padding = (0, 10, 0, 20)

        self.time_label = Label(bold=True, color="black")
        self.add_widget(self.time_label)
        
        self.name_label = Label(halign="center", color="black")
        
        # Taken from https://stackoverflow.com/questions/43666381/wrapping-the-text-of-a-kivy-label
        self.name_label.bind(
            width=lambda *x: self.name_label.setter('text_size')(self.name_label, (self.name_label.width, None)),
            texture_size=lambda *x: self.name_label.setter('height')(self.name_label, self.name_label.texture_size[1])
        )
        self.add_widget(self.name_label)


    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.time_label.text = data["time"]
        self.name_label.text = data["name"]
        return super(TodaysNotesRow, self).refresh_view_attrs(rv, index, data)



class TodaysNotesRecycleview(RecycleView):
    def __init__(self, items, *args, **kwargs):
        super(TodaysNotesRecycleview, self).__init__(*args, **kwargs)
        self.viewclass = TodaysNotesRow

        self.data = [{"time": time, "name": name} for time, name in items]


class TestApp(App):
    def build(self):
        return TodaysNotesRecycleview()

if __name__ == '__main__':
    TestApp().run()

