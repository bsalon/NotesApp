from kivy.uix import boxlayout, button, label, popup, textinput


class TagDialog(popup.Popup): # AUTO DISMISS
    def __init__(self, **kwargs):
        super(TagDialog, self).__init__(**kwargs)
        self.title = "Tag dialog"

        layout = boxlayout.BoxLayout(orientation="vertical")

        # Name
        name_label = label.Label(text="Name:", size_hint=(1/2, 1))
        self.name_input = textinput.TextInput(size_hint=(1/2, 1), multiline=False)
        name_layout = boxlayout.BoxLayout(orientation="horizontal")
        name_layout.add_widget(name_label)
        name_layout.add_widget(self.name_input)

        # Text
        description_label = label.Label(text="Description:", size_hint=(1/2, 1))
        self.description_input = textinput.TextInput(size_hint=(1/2, 1), multiline=False)
        description_layout = boxlayout.BoxLayout(orientation="horizontal")
        description_layout.add_widget(description_label)
        description_layout.add_widget(self.description_input)

        # Buttons
        save_button = button.Button(text="Save", size_hint=(1/2, 1), on_release=self._save)
        close_button = button.Button(text="Close", size_hint=(1/2, 1), on_release=self._close)
        buttons_layout = boxlayout.BoxLayout(orientation="horizontal")
        buttons_layout.add_widget(save_button)
        buttons_layout.add_widget(close_button)

        # Layout
        layout.add_widget(name_layout)
        layout.add_widget(description_layout)
        layout.add_widget(buttons_layout)

        self.content = layout


    def fill_dialog(self, tag):
        self.name_input.text = tag.name
        self.description_input.text = tag.description


    def _save(self, instance):
        self.accepted = True
        self.data_dict = {
            "name" : self.name_input.text,
            "description" : self.description_input.text,
        }
        self.dismiss()


    def _close(self, instance):
        self.accepted = False
        self.dismiss()

