from kivy.uix import label
from kivy import clock

from datetime import datetime


class TimeLabel(label.Label):
    def __init__(self, *args, **kwargs):
        super(TimeLabel, self).__init__(*args, **kwargs)
        self.tick(1.0)
        clock.Clock.schedule_interval(self.tick, 1.0)


    def tick(self, deltatime):
        time_text = datetime.now().strftime("%d-%m-%Y\n%H:%M:%S")
        self.text = time_text

