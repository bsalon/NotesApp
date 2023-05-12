from kivy.uix import boxlayout, button, checkbox, label, popup


class SettingsDialog(popup.Popup):
    def __init__(self, **kwargs):
        """
        Initializes settings dialog with all its widgets
        """

        super(SettingsDialog, self).__init__(**kwargs)
        layout = boxlayout.BoxLayout(orientation="vertical")

        # Info label
        info_label = label.Label(text="Saving with different than current library will stop this application", color="red", size_hint=(1, None))
        layout.add_widget(info_label)

        # Radio buttons
        self.radio_buttons = [checkbox.CheckBox(group="library", allow_no_selection=False, size_hint=(6/7, 1)),
                              checkbox.CheckBox(group="library", allow_no_selection=False, size_hint=(6/7, 1)),
                              checkbox.CheckBox(group="library", active=True, allow_no_selection=False, size_hint=(6/7, 1))]
 
        labels = [label.Label(text="PySide", color="black", size_hint=(1/7, 1)),
                  label.Label(text="Tkinter", color="black", size_hint=(1/7, 1)),
                  label.Label(text="Kivy", color="black", size_hint=(1/7, 1))]


        for i in range(len(self.radio_buttons)):
            rb_layout = boxlayout.BoxLayout(orientation="horizontal")
            rb_layout.add_widget(labels[i])
            rb_layout.add_widget(self.radio_buttons[i])
            layout.add_widget(rb_layout)
        
        # Warning label
        warn_label = label.Label(text="WARNING: This library doesn't support application reopening.\nIf you choose different library and then this library again, it will not work!", color="red", size_hint=(1, None))
        layout.add_widget(warn_label)

        # Buttons
        save_button = button.Button(text="Save", size_hint=(1/2, 1), on_release=self._save)
        close_button = button.Button(text="Close", size_hint=(1/2, 1), on_release=self._close)
        
        buttons_layout = boxlayout.BoxLayout(orientation="horizontal")
        buttons_layout.add_widget(save_button)
        buttons_layout.add_widget(close_button)
        layout.add_widget(buttons_layout)

        self.content = layout


    def _save(self, instance):
        """
        Saves dialog data into data_dict and closes the dialog

        :param instance: Instance causing this method
        """

        index = 0
        for i, rb in enumerate(self.radio_buttons):
            if rb.state == "down":
                index = i
                break

        self.accepted = True
        self.data_dict = {
            "library" : index,
        }
        self.dismiss()


    def _close(self, instance):
        """
        Closes the dialog

        :param instance: Instance causing this method
        """

        self.accepted = False
        self.dismiss()


