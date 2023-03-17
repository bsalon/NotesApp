from kivy.uix import progressbar

from kivy import clock


class LoadingBar(progressbar.ProgressBar):
    def __init__(self, *args, **kwargs):
        super(LoadingBar, self).__init__(*args, **kwargs)
        self.load_level = 0
        self.increase = True


    def stop(self):
        self.value = 0
        clock.Clock.unschedule(self.load)
        clock.Clock.schedule_interval(self.load, 0.1)


    def start(self):
        clock.Clock.unschedule(self.load)
        


    def load(self, deltatime):
        if self.value == self.max:
            self.increase = False
        if self.value == 0:
            self.increase = True

        self.value = self.value + self.max // 10 if self.increase else self.value + self.max // 10

