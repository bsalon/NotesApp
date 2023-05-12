import math

from kivy import app
from kivy.lang import Builder
from kivy.uix import gridlayout, label


Builder.load_string('''
<PageLabel>:
    markup: True
    color: "black"
    canvas.before:
        Color:
            rgba: 0, 0, 0, 1
        Line:
            dash_offset: 2
            dash_length: 2
            width: 1
            rectangle: self.x, self.y, self.width, self.height

<CurrentPageLabel>:
    markup: True
    color: "black"
    canvas.before:
        Color:
            rgba: (255/255, 201/255, 87/255, 255/255)
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: 0, 0, 0, 1
        Line: 
            width: 1
            rectangle: self.x, self.y, self.width, self.height
''')


class PaginationLabels(gridlayout.GridLayout):
    """
    Pagination for the accordion

    Methods are used to change the current page
    """

    def __init__(self, page_size, items_count, *args, **kwargs):
        super(PaginationLabels, self).__init__(*args, **kwargs)
        self.page_size = page_size
        self.items_count = items_count

        self.current_page = 1
        self.register_event_type("on_page_changed")
        self.create_labels()


    def create_labels(self):
        self.clear_widgets()

        last_page = self.pages_count()
        prev_page = 1 if self.current_page - 1 < 1 else self.current_page - 1
        next_page = last_page if self.current_page + 1 > last_page else self.current_page + 1

        list_pages = {1, prev_page, self.current_page, next_page, last_page}

        self.prev_page_label = PageLabel(text="[ref=prev]<<[/ref]")
        self.prev_page_label.bind(on_ref_press=self.go_to_prev_page)

        list_labels = [self.prev_page_label]
        for page in list_pages:
            page_label = CurrentPageLabel(text=f"[ref={page}]{page}[/ref]") if page == self.current_page else PageLabel(text=f"[ref={page}]{page}[/ref]")
            # p seems to be str in this case so we need to type it to int
            page_label.bind(on_ref_press=lambda _, p=page: self.go_to_page(int(p)))
            list_labels.append(page_label)

        self.next_page_label = PageLabel(markup=True, color="black", text="[ref=next]>>[/ref]")
        self.next_page_label.bind(on_ref_press=self.go_to_next_page)
        list_labels.append(self.next_page_label)

        for l in list_labels:
            self.add_widget(l)


    def pages_count(self):
        return math.ceil(self.items_count / self.page_size)


    def go_to_prev_page(self, instance_label, ref):
        self.current_page -= 1
        self.current_page = self.current_page if self.current_page >= 1 else 1
        self.dispatch("on_page_changed")
        self.create_labels()


    def go_to_next_page(self, instance_label, ref):
        last_page = self.pages_count()
        self.current_page += 1
        self.current_page = self.current_page if self.current_page <= last_page else last_page
        self.dispatch("on_page_changed")
        self.create_labels()


    def go_to_page(self, page):
        self.current_page = page
        self.dispatch("on_page_changed")
        self.create_labels()


    def on_page_changed(self):
        pass


class PageLabel(label.Label):
    def __init__(self, *args, **kwargs):
        super(PageLabel, self).__init__(*args, **kwargs)

class CurrentPageLabel(label.Label):
    def __init__(self, *args, **kwargs):
        super(CurrentPageLabel, self).__init__(*args, **kwargs)



class LabelsApp(app.App):
    def build(self):
        return PaginationLabels(10, 45)


if __name__ == "__main__":
    LabelsApp().run()

