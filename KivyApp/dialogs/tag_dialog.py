from kivy.uix import boxlayout, button, label, popup, textinput


class TagDialog(popup.Popup):
    def __init__(self, **kwargs):
        """
        Initializes tag dialog with all its widgets
        """

        super(TagDialog, self).__init__(**kwargs)
        self.title = "Tag dialog"
        layout = boxlayout.BoxLayout(orientation="vertical")

        # Tag name
        name_label = label.Label(text="Name:", color="black", size_hint=(1/2, 1))
        self.name_input = textinput.TextInput(size_hint=(1/2, 1), multiline=False)
        name_layout = boxlayout.BoxLayout(orientation="horizontal")
        name_layout.add_widget(name_label)
        name_layout.add_widget(self.name_input)

        # Tag description
        description_label = label.Label(text="Description:", color="black", size_hint=(1/2, 1))
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
        """
        Fills dialog widgets with tag values

        :param category: Tag object
        """

        self.name_input.text = tag.name
        self.description_input.text = tag.description


    def _save(self, instance):
        """
        Saves dialog data into data_dict and closes the dialog

        :param instance: Instance causing this method
        """

        if not self._validate():
            return
        self.accepted = True
        self.data_dict = {
            "name" : self.name_input.text,
            "description" : self.description_input.text,
        }
        self.dismiss()


    def _close(self, instance):
        """
        Closes the dialog

        :param instance: Instance causing this method
        """

        self.accepted = False
        self.dismiss()


    def _validate(self):
        """
        Validates name field
        """

        return self._validate_field(self.name_input)


    def _validate_field(self, field):
        """
        Validates field value by testing if its empty

        :param field: Field to be validated

        :return: True if field value is not empty False otherwise
        """

        if field.text == "" or field.text.isspace():
            field.background_color = (1, 0.5, 0.5, 1)
            return False
        field.background_color = (1, 1, 1, 1)
        return True

