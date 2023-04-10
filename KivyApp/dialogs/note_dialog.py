from kivy import properties
from kivy.uix import boxlayout, button, checkbox, label, popup, slider, spinner, textinput
from kivymd.uix import pickers

import datetime
import math

from KivyApp.widgets import multi_select_spinner


class NoteDialog(popup.Popup):
    def __init__(self, categories_names, tags_names, **kwargs):
        super(NoteDialog, self).__init__(**kwargs)
        self.title = "Note dialog"
        layout = boxlayout.BoxLayout(orientation="vertical")

        # Name
        name_label = label.Label(text="Name:", color="black", size_hint=(1/2, 1))
        self.name_input = textinput.TextInput(size_hint=(1/2, 1), multiline=False)
        name_layout = boxlayout.BoxLayout(orientation="horizontal")
        name_layout.add_widget(name_label)
        name_layout.add_widget(self.name_input)

        # Date
        today = datetime.date.today()

        date_label = label.Label(text="Date:", color="black", size_hint=(1/2, 1))
        self.date_button = button.Button(text=today.strftime("%d-%m-%Y"), size_hint=(1/2, 1), on_release=self._show_date_picker)
        date_layout = boxlayout.BoxLayout(orientation="horizontal")
        date_layout.add_widget(date_label)
        date_layout.add_widget(self.date_button)

        # Time
        time_label = label.Label(text="Time:", color="black", size_hint=(1/2, 1))
        self.time_button = button.Button(text="00:00", size_hint=(1/2, 1), on_release=self._show_time_picker)
        time_layout = boxlayout.BoxLayout(orientation="horizontal")
        time_layout.add_widget(time_label)
        time_layout.add_widget(self.time_button)

        # Text
        text_label = label.Label(text="Text:", color="black", size_hint=(1/2, 1))
        self.text_input = textinput.TextInput(size_hint=(1/2, 1), multiline=False)
        text_layout = boxlayout.BoxLayout(orientation="horizontal")
        text_layout.add_widget(text_label)
        text_layout.add_widget(self.text_input)

        # Priority
        priority_label = label.Label(text="Assign priority:", color="black", size_hint=(1/2, 1))
        priority_yes_label = label.Label(text="Yes", color="black", size_hint=(1/8, 1))
        self.priority_yes_radiobutton = checkbox.CheckBox(group="priority", active=True, allow_no_selection=False, size_hint=(1/8, 1))
        priority_no_label = label.Label(text="No", color="black", size_hint=(1/8, 1))
        self.priority_no_radiobutton = checkbox.CheckBox(group="priority", allow_no_selection=False, size_hint=(1/8, 1))
        self.priority_no_radiobutton.bind(state=self._slider_enabling)
 
        priority_layout = boxlayout.BoxLayout(orientation="horizontal")
        priority_layout.add_widget(priority_label)
        priority_layout.add_widget(priority_yes_label)
        priority_layout.add_widget(self.priority_yes_radiobutton)
        priority_layout.add_widget(priority_no_label)
        priority_layout.add_widget(self.priority_no_radiobutton)

        # Priority slider
        priority_value = label.Label(text="0", color="black", size_hint=(1/2, 1))
        priority_slider_value = properties.NumericProperty(0)
        self.priority_slider = slider.Slider(min=0, max=100, value_track=True, size_hint=(1/2, 1))
        self.priority_slider.fbind("value", lambda ins, val: setattr(priority_value, "text", "{:02.0f}".format(val)))

        self.priority_slider_layout = boxlayout.BoxLayout(orientation="horizontal")
        self.priority_slider_layout.add_widget(priority_value)
        self.priority_slider_layout.add_widget(self.priority_slider)

        # Categories
        categories_label = label.Label(text="Select category:", color="black", size_hint=(1/2, 1))
        self.categories_spinner = spinner.Spinner(
            text=categories_names[0] if len(categories_names) > 0 else "",
            values=categories_names,
            size_hint=(1/2, 1)
        )
        categories_layout = boxlayout.BoxLayout(orientation="horizontal")
        categories_layout.add_widget(categories_label)
        categories_layout.add_widget(self.categories_spinner)


        # Tags
        tags_label = label.Label(text="Select tags:", color="black", size_hint=(1/2, 1))
        self.tags_spinner = multi_select_spinner.MultiSelectSpinner(
            values=tags_names,
            size_hint=(1/2, 1)
        )
        tags_layout = boxlayout.BoxLayout(orientation="horizontal")
        tags_layout.add_widget(tags_label)
        tags_layout.add_widget(self.tags_spinner)

        # Buttons
        save_button = button.Button(text="Save", size_hint=(1/2, 1), on_release=self._save)
        close_button = button.Button(text="Close", size_hint=(1/2, 1), on_release=self._close)
        buttons_layout = boxlayout.BoxLayout(orientation="horizontal")
        buttons_layout.add_widget(save_button)
        buttons_layout.add_widget(close_button)

        # Layout
        layout.add_widget(name_layout)
        layout.add_widget(date_layout)
        layout.add_widget(time_layout)
        layout.add_widget(text_layout)
        layout.add_widget(priority_layout)
        layout.add_widget(self.priority_slider_layout)
        layout.add_widget(categories_layout)
        layout.add_widget(tags_layout)
        layout.add_widget(buttons_layout)

        self.content = layout


    def fill_dialog(self, note):
        self.name_input.text = note.name
        self.date_button.text = note.time.date().strftime("%d-%m-%Y")
        self.time_button.text = note.time.time().strftime("%H:%M")
        self.text_input.text = note.text
        self.priority_slider.value = note.priority
        self.categories_spinner.text = note.category.name
        self.tags_spinner.update_selected_values(note.tags)


    def _show_date_picker(self, instance):
        previous_date = datetime.datetime.strptime(self.date_button.text, "%d-%m-%Y").date()
        date_picker = pickers.MDDatePicker(
            year=previous_date.year,
            month=previous_date.month,
            day=previous_date.day
        )
        date_picker.bind(on_save=self._set_date_button)
        date_picker.open()


    def _set_date_button(self, instance, time, date_range):
        self.date_button.text = time.strftime("%d-%m-%Y")


    def _show_time_picker(self, instance):
        previous_time = datetime.datetime.strptime(self.time_button.text, "%H:%M").time()
        time_picker = pickers.MDTimePicker()
        time_picker.set_time(previous_time)
        time_picker.bind(time=self._set_time_button)
        time_picker.open()


    def _set_time_button(self, instance, time):
        self.time_button.text = time.strftime("%H:%M")


    def _slider_enabling(self, instance, state):
        w = self.priority_slider_layout
        if state == "down":
            w.saved_attrs = w.width, w.size_hint_x, w.size_hint_y, w.opacity, w.disabled
            w.width, w.size_hint_x, w.size_hint_y, w.opacity, w.disabled = 0, None, None, 0, True
        else:
            w.width, w.size_hint_x, w.size_hint_y, w.opacity, w.disabled = w.saved_attrs
            del w.saved_attrs


    def _save(self, instance):
        if not self._validate():
            return
        self.accepted = True
        self.data_dict = {
            "name" : self.name_input.text,
            "time" : datetime.datetime.strptime(f"{self.date_button.text} {self.time_button.text}", "%d-%m-%Y %H:%M"),
            "text" : self.text_input.text,
            "priority" : math.ceil(self.priority_slider.value),
            "category" : self.categories_spinner.text,
            "tags" : self.tags_spinner.selected_values
        }
        self.dismiss()


    def _close(self, instance):
        self.accepted = False
        self.dismiss()


    def _validate(self):
        return self._validate_field(self.name_input)


    def _validate_field(self, field):
        if field.text == "" or field.text.isspace():
            field.background_color = (1, 0.5, 0.5, 1)
            return False
        field.background_color = (1, 1, 1, 1)
        return True



