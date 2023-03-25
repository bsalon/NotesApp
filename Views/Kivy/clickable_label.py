from kivy.lang import Builder
from kivy.uix import label


class ClickableLabel(label.Label):
    def __init__(self, *args, **kwargs):
        super(ClickableLabel, self).__init__(*args, **kwargs)
        self.click_command = None


    def on_ref_press(self, press):
        self.click_command()

   # def on_touch_down(self, touch):
   #     print(touch)
   #     if touch.is_touch:
   #         self.click_command()


   # def on_press(self):
   #     print(touch)
   #     self.click_command()
