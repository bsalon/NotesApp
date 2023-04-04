from kivy import app
from kivy.uix import boxlayout, image, textinput

import pathlib


class SearchBarWithIcon(boxlayout.BoxLayout):
    def __init__(self, *args, **kwargs):
        super(SearchBarWithIcon, self).__init__(orientation="horizontal", *args, **kwargs)

        image_path = pathlib.Path(__file__).parent.parent.parent / "Images" / "SearchIcon.png"
        icon = image.Image(source = image_path.resolve().as_posix(), size_hint=(1/6, 4/5), pos_hint={"x": 0, "y": 0.1})
        self.add_widget(icon)

        self.input = textinput.TextInput(size_hint=(5/6, 4/5), pos_hint={"x": 0, "y": 0.1}, background_normal="", background_active="", multiline=False, hint_text="Filter by name...", padding=(5, 5))
        self.add_widget(self.input)


class App(app.App):
    def build(self):
        return SearchBarWithIcon()


if __name__ == "__main__":
    App().run()
