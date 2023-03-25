from kivy import base, lang, metrics, properties
from kivy.uix import button, dropdown, togglebutton


# Taken from https://stackoverflow.com/questions/36609017/kivy-spinner-widget-with-multiple-selection

class MultiSelectSpinner(button.Button):
    """Widget allowing to select multiple text options."""

    dropdown = properties.ObjectProperty(None)
    """(internal) DropDown used with MultiSelectSpinner."""

    values = properties.ListProperty([])
    """Values to choose from."""

    selected_values = properties.ListProperty([])
    """List of values selected by the user."""


    def __init__(self, *args, **kwargs):
        self.toggles = []
        self.bind(dropdown=self.update_dropdown)
        self.bind(values=self.update_dropdown)
        super(MultiSelectSpinner, self).__init__(*args, **kwargs)
        self.bind(on_release=self.toggle_dropdown)


    def toggle_dropdown(self, *args):
        if self.dropdown.parent:
            self.dropdown.dismiss()
        else:
            self.dropdown.open(self)


    def update_selected_values(self, selected_values):
        self.selected_values = selected_values
        for toggle in self.toggles:
            toggle.state = "down" if toggle.text in self.selected_values else "normal"


    def update_dropdown(self, *args):
        if not self.dropdown:
            self.dropdown = dropdown.DropDown()
        values = self.values
        if values:
            if self.dropdown.children:
                self.dropdown.clear_widgets()
            for value in values:
                toggle = togglebutton.ToggleButton(text=value, size_hint=(1, None), height=metrics.dp(48))
                toggle.bind(state=self.select_value)
                self.toggles.append(toggle)
                self.dropdown.add_widget(toggle)


    def select_value(self, instance, value):
        if value == "down":
            if instance.text not in self.selected_values:
                self.selected_values.append(instance.text)
        else:
            if instance.text in self.selected_values:
                self.selected_values.remove(instance.text)


    def on_selected_values(self, instance, value):
        if value:
            self.text = ", ".join(value)
        else:
            self.text = ""


#kv = '''
#BoxLayout:
#    orientation: 'vertical'
#
#    BoxLayout:
#
#        Label:
#            text: 'Select city'
#
#        MultiSelectSpinner:
#            id: city
#            values: 'Sydney', 'Moscow', 'Warsaw', 'New York', 'Tokio', 'Orlando', 'Los Angeles', 'Beyrut'
#
#    Label:
#        text: 'You selected {} cities.'.format(city.text)
#    '''
#    
#base.runTouchApp(lang.Builder.load_string(kv))


