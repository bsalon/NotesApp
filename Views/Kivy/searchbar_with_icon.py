from kivy import app
from kivy.uix import boxlayout, image, textinput



class SearchBarWithIcon(boxlayout.BoxLayout):
    def __init__(self, *args, **kwargs):
        super(SearchBarWithIcon, self).__init__(orientation="horizontal", *args, **kwargs)

        icon = image.Image(source = "/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/TodaysNotesIcon.png", size_hint=(1/6, 1))
        self.add_widget(icon)

        text_input = textinput.TextInput(size_hint=(5/6, 1), multiline=False)
        self.add_widget(text_input)


class App(app.App):
    def build(self):
        return SearchBarWithIcon()


if __name__ == "__main__":
    App().run()
