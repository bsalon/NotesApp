from kivy import properties
from kivy.uix import boxlayout, button, checkbox, label, popup, slider, spinner, textinput
from kivymd.uix import pickers

import datetime
import math



class AdvancedFilterDialog(popup.Popup):
    def __init__(self, **kwargs):
        super(AdvancedFilterDialog, self).__init__(**kwargs)
        self.accepted = False

        layout = boxlayout.BoxLayout(orientation="vertical")

        # Note Name
        note_name_label = label.Label(text="Note name:", color="black", size_hint=(1/2, 1))
        self.note_name_input = textinput.TextInput(size_hint=(1/2, 1), multiline=False)
        note_name_layout = boxlayout.BoxLayout(orientation="horizontal")
        note_name_layout.add_widget(note_name_label)
        note_name_layout.add_widget(self.note_name_input)

        # Note date
        today = self._create_str_date(datetime.date.today())

        note_date_label = label.Label(text="Note date range:", color="black", size_hint=(1/2, 1))
        self.date_from_button = button.Button(text=today, size_hint=(1/6, 1), on_release=self._show_date_from_picker)
        note_date_divider_label = label.Label(text="  -  ", color="black", size_hint=(1/6, 1))
        self.date_to_button = button.Button(text=today, size_hint=(1/6, 1), on_release=self._show_date_to_picker)

        note_date_layout = boxlayout.BoxLayout(orientation="horizontal")
        note_date_layout.add_widget(note_date_label)
        note_date_layout.add_widget(self.date_from_button)
        note_date_layout.add_widget(note_date_divider_label)
        note_date_layout.add_widget(self.date_to_button)

        # Note time
        note_time_label = label.Label(text="Note time range:", color="black", size_hint=(1/2, 1))
        self.time_from_button = button.Button(text="00:00", size_hint=(1/6, 1), on_release=self._show_time_from_picker)
        note_time_divider_label = label.Label(text="  -  ", color="black", size_hint=(1/6, 1))
        self.time_to_button = button.Button(text="23:59", size_hint=(1/6, 1), on_release=self._show_time_to_picker)

        note_time_layout = boxlayout.BoxLayout(orientation="horizontal")
        note_time_layout.add_widget(note_time_label)
        note_time_layout.add_widget(self.time_from_button)
        note_time_layout.add_widget(note_time_divider_label)
        note_time_layout.add_widget(self.time_to_button)

        # Note text
        note_text_label = label.Label(text="Note text:", color="black", size_hint=(1/2, 1))
        self.note_text_input = textinput.TextInput(size_hint=(1/2, 1), multiline=False)
        note_text_layout = boxlayout.BoxLayout(orientation="horizontal")
        note_text_layout.add_widget(note_text_label)
        note_text_layout.add_widget(self.note_text_input)

        # Note priority
        note_priority_label = label.Label(text="Note priority range:", color="black", size_hint=(1/2, 1))
        self.note_min_priority_input = textinput.TextInput(size_hint=(1/6, 1), multiline=False, input_filter="int", text="0")
        note_priority_divider_label = label.Label(text="  -  ", color="black", size_hint=(1/6, 1))
        self.note_max_priority_input = textinput.TextInput(size_hint=(1/6, 1), multiline=False, input_filter="int", text="100")

        note_priority_layout = boxlayout.BoxLayout(orientation="horizontal")
        note_priority_layout.add_widget(note_priority_label)
        note_priority_layout.add_widget(self.note_min_priority_input)
        note_priority_layout.add_widget(note_priority_divider_label)
        note_priority_layout.add_widget(self.note_max_priority_input)

        # Category
        category_name_label = label.Label(text="Category name contains:", color="black", size_hint=(1/2, 1))
        self.category_name_input = textinput.TextInput(size_hint=(1/2, 1), multiline=False)
        category_name_layout = boxlayout.BoxLayout(orientation="horizontal")
        category_name_layout.add_widget(category_name_label)
        category_name_layout.add_widget(self.category_name_input)
        
        category_description_label = label.Label(text="Category description contains:", color="black", size_hint=(1/2, 1))
        self.category_description_input = textinput.TextInput(size_hint=(1/2, 1), multiline=False)
        category_description_layout = boxlayout.BoxLayout(orientation="horizontal")
        category_description_layout.add_widget(category_description_label)
        category_description_layout.add_widget(self.category_description_input)

        # Tag
        tag_name_label = label.Label(text="Tag name contains:", color="black", size_hint=(1/2, 1))
        self.tag_name_input = textinput.TextInput(size_hint=(1/2, 1), multiline=False)
        tag_name_layout = boxlayout.BoxLayout(orientation="horizontal")
        tag_name_layout.add_widget(tag_name_label)
        tag_name_layout.add_widget(self.tag_name_input)
        
        tag_description_label = label.Label(text="Tag description contains:", color="black", size_hint=(1/2, 1))
        self.tag_description_input = textinput.TextInput(size_hint=(1/2, 1), multiline=False)
        tag_description_layout = boxlayout.BoxLayout(orientation="horizontal")
        tag_description_layout.add_widget(tag_description_label)
        tag_description_layout.add_widget(self.tag_description_input)

        # Buttons
        save_button = button.Button(text="Save", size_hint=(1/2, 1), on_release=self._save)
        close_button = button.Button(text="Close", size_hint=(1/2, 1), on_release=self._close)
        buttons_layout = boxlayout.BoxLayout(orientation="horizontal")
        buttons_layout.add_widget(save_button)
        buttons_layout.add_widget(close_button)

        # Layout
        layout.add_widget(note_name_layout)
        layout.add_widget(note_date_layout)
        layout.add_widget(note_time_layout)
        layout.add_widget(note_text_layout)
        layout.add_widget(note_priority_layout)
        layout.add_widget(category_name_layout)
        layout.add_widget(category_description_layout)
        layout.add_widget(tag_name_layout)
        layout.add_widget(tag_description_layout)
        layout.add_widget(buttons_layout)

        self.content = layout


    def _create_str_date(self, datepicker):
        return f"{datepicker.day:02d}-{datepicker.month:02d}-{datepicker.year:04d}"


    def _show_date_to_picker(self, instance):
        previous_date = datetime.datetime.strptime(self.date_to_button.text, "%d-%m-%Y").date()
        date_picker = pickers.MDDatePicker(
            year=previous_date.year,
            month=previous_date.month,
            day=previous_date.day
        )
        date_picker.bind(on_save=self._set_date_to_button)
        date_picker.open()


    def _set_date_to_button(self, instance, time, date_range):
        # instance has wrong day and time has wrong year so we have to combine them
        instance.day = time.day
        self.date_to_button.text = self._create_str_date(instance)


    def _show_date_from_picker(self, instance):
        previous_date = datetime.datetime.strptime(self.date_from_button.text, "%d-%m-%Y").date()
        date_picker = pickers.MDDatePicker(
            year=previous_date.year,
            month=previous_date.month,
            day=previous_date.day
        )
        date_picker.bind(on_save=self._set_date_from_button)
        date_picker.open()


    def _set_date_from_button(self, instance, time, date_range):
        # instance has wrong day and time has wrong year so we have to combine them
        instance.day = time.day
        self.date_from_button.text = self._create_str_date(instance)


    def _show_time_from_picker(self, instance):
        previous_time = datetime.datetime.strptime(self.time_from_button.text, "%H:%M").time()
        time_picker = pickers.MDTimePicker()
        time_picker.set_time(previous_time)
        time_picker.bind(time=self._set_time_from_button)
        time_picker.open()


    def _set_time_from_button(self, instance, time):
        self.time_from_button.text = time.strftime("%H:%M")


    def _show_time_to_picker(self, instance):
        previous_time = datetime.datetime.strptime(self.time_to_button.text, "%H:%M").time()
        time_picker = pickers.MDTimePicker()
        time_picker.set_time(previous_time)
        time_picker.bind(time=self._set_time_to_button)
        time_picker.open()


    def _set_time_to_button(self, instance, time):
        self.time_to_button.text = time.strftime("%H:%M")


    def _save(self, instance):
        self.accepted = True
        self.data_dict = {
            "note_name" : self.note_name_input.text,
            "note_from_date" : datetime.datetime.strptime(f"{self.date_from_button.text} {self.time_from_button.text}", "%d-%m-%Y %H:%M"),
            "note_to_date" : datetime.datetime.strptime(f"{self.date_to_button.text} {self.time_to_button.text}", "%d-%m-%Y %H:%M"),
            "note_min_priority" : self._get_min_priority(),
            "note_max_priority" : self._get_max_priority(),
            "note_text" : self.note_text_input.text,
            "category_name" : self.category_name_input.text,
            "category_description" : self.category_description_input.text,
            "tag_name" : self.tag_name_input.text,
            "tag_description" : self.tag_description_input.text
        }
        self.dismiss()


    def _close(self, instance):
        self.accepted = False
        self.dismiss()


    def _get_min_priority(self):
        if self.note_min_priority_input.text == "" or self.note_min_priority_input.text == "-":
            return 0
        num = int(self.note_min_priority_input.text)
        if num > 100:
            return 100
        if num < 0:
            return 0
        return num


    def _get_max_priority(self):
        if self.note_max_priority_input.text == "" or self.note_max_priority_input.text == "-":
            return 100
        num = int(self.note_max_priority_input.text)
        if num > 100:
            return 100
        if num < 0:
            return 0
        return num

