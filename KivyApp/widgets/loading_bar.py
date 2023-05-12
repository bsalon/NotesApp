from kivy.uix import progressbar

from kivy import clock


class LoadingBar(progressbar.ProgressBar):
    """
    Infinite loading bar
    """

    def __init__(self, *args, **kwargs):
        super(LoadingBar, self).__init__(*args, **kwargs)
        self.load_level = 0
        self.increase = True


    def start(self):
        self.value = 0
        clock.Clock.unschedule(self.load)
        clock.Clock.schedule_interval(self.load, 0.1)


    def stop(self):
        clock.Clock.unschedule(self.load)
        self.value = 0


    def load(self, deltatime):
        if self.value >= self.max:
            self.increase = False
        if self.value <= 0:
            self.increase = True

        self.value = self.value + self.max // 10 if self.increase else self.value - self.max // 10

