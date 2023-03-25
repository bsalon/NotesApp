from kivy.lang import Builder
from kivy.uix import button, label


import clickable_label
import time_label


Builder.load_file("styled_widgets.kv")


# LABELS

class ClickableLabel(clickable_label.ClickableLabel):
    def __init__(self, *args, **kwargs):
        super(ClickableLabel, self).__init__(*args, **kwargs)


class FastFilterLabel(label.Label):
    def __init__(self, *args, **kwargs):
        super(FastFilterLabel, self).__init__(*args, **kwargs)


class TimeLabel(time_label.TimeLabel):
    def __init__(self, *args, **kwargs):
        super(TimeLabel, self).__init__(*args, **kwargs)


class TodaysNotesLabel(label.Label):
    def __init__(self, *args, **kwargs):
        super(TodaysNotesLabel, self).__init__(*args, **kwargs)


# BUTTONS

class TodaysNotesButton(button.Button):
    def __init__(self, *args, **kwargs):
        super(TodaysNotesButton, self).__init__(*args, **kwargs)


class ToolbarButton(button.Button):
    def __init__(self, *args, **kwargs):
        super(ToolbarButton, self).__init__(*args, **kwargs)
