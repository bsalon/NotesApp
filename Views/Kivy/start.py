import kivy

from kivy import app, lang
from kivy.core import window
from kivy.uix import boxlayout, button, image, label

from datetime import datetime

from Controllers import UseCases

import clickable_label
import loading_bar
import styled_widgets
import time_label


class KivyApplicationLayout(boxlayout.BoxLayout):
    def __init__(self, use_cases, *args, **kwargs):
        super(KivyApplicationLayout, self).__init__(*args, **kwargs)

        self.use_cases = use_cases

        self.current_note_filter = self.create_default_filter()
        self.grid_page = 1
        self.grid_notes = [note for note in self.use_cases.get_filtered_notes_paged(self.current_note_filter, page=self.grid_page, size=10)]

        use_cases_notes = [note for note in self.use_cases.get_notes()]
        self.table_notes = [(note.name, note.priority, note.time.strftime("%d/%m/%Y %H:%M"), note.text) for note in use_cases_notes]
        self.today_notes = [(note.time.strftime("%H:%M"), note.name) for note in use_cases_notes if note.time.date() == datetime.today().date()]
        self.today_notes.sort(key = lambda note: note[0])

        self.table_tags = [(tag.name, tag.description) for tag in self.use_cases.get_tags()]

        self.table_categories = [(category.name, category.description) for category in self.use_cases.get_categories()]

        self.table_filters = [(note_filter.name,
                               note_filter.order,
                               note_filter.note_name,
                               note_filter.category_name) for note_filter in self.use_cases.get_filters()]

        # toolbar layout on top
        self.toolbar_layout = boxlayout.BoxLayout(orientation="horizontal", size_hint=(1, 1/15))
        self._init_toolbar_layout()

        # todays notes layout
        self.todays_notes_layout = boxlayout.BoxLayout(orientation="vertical", size_hint=(1/8, 1))
        self._init_todays_notes_layout()

        # content layout
        self.tabs_content_layout = boxlayout.BoxLayout(orientation="vertical", size_hint=(7/8, 1))
        self._init_tabs_content_layout()

        # todays notes and content below toolbar
        todays_notes_and_content_layout = boxlayout.BoxLayout(orientation="horizontal", size_hint=(1, 14/15))
        todays_notes_and_content_layout.add_widget(self.todays_notes_layout)
        todays_notes_and_content_layout.add_widget(self.tabs_content_layout)
        
        # 15 rows : 8 columns
        self.add_widget(self.toolbar_layout)
        self.add_widget(todays_notes_and_content_layout)



    def _init_toolbar_layout(self):
        # Today's notes icon button
        self.todays_notes_icon_button = styled_widgets.TodaysNotesButton()
        #self.todays_notes_icon_button = button.Button(text="Today's notes", size_hint=(1, 1/4))
        todays_notes_icon = image.Image(source = "/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/TodaysNotesIcon.png", size_hint=(1, 3/4))

        todays_notes_icon_button_layout = boxlayout.BoxLayout(orientation="vertical", size_hint=(4/32, 1))
        todays_notes_icon_button_layout.add_widget(todays_notes_icon)
        todays_notes_icon_button_layout.add_widget(self.todays_notes_icon_button)

        self.toolbar_layout.add_widget(todays_notes_icon_button_layout)
        
        self.todays_notes_pane_visible = True


        # Use fast filter section
        self.toolbar_layout.add_widget(label.Label(text = "Use fast filters:", size_hint=(3/32, 1), color="black"))

        self.fast_filters_text_links = [clickable_label.ClickableLabel(text="#1", size_hint=(2/32, 1), color="black"),
                                        clickable_label.ClickableLabel(text="#2", size_hint=(2/32, 1), color="black"),
                                        clickable_label.ClickableLabel(text="#3", size_hint=(2/32, 1), color="black")]
        for order, fast_filter_text_link in enumerate(self.fast_filters_text_links):
            self.toolbar_layout.add_widget(fast_filter_text_link)
            fast_filter_text_link.click_command = lambda o=order: print(f"{o}") # TODO self.use_fast_filter(o+1)

        # Time widget
        self.time_widget = time_label.TimeLabel(halign="center", valign="center", size_hint=(6/32, 1), color="black")
        self.toolbar_layout.add_widget(self.time_widget)

        # Add icon button
        self.add_icon_button = button.Button(background_normal="/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/AddIcon.png", border=(0, 0, 0, 0), size_hint=(2/32, 1))
        self.toolbar_layout.add_widget(self.add_icon_button)

        # Edit icon button
        self.edit_icon_button = button.Button(background_normal="/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/EditIcon.png", border=(0, 0, 0, 0), size_hint=(2/32, 1))
        self.toolbar_layout.add_widget(self.edit_icon_button)

        # Delete icon button
        self.delete_icon_button = button.Button(background_normal="/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/DeleteIcon.png", border=(0, 0, 0, 0), size_hint=(2/32, 1))
        self.toolbar_layout.add_widget(self.delete_icon_button)

        # Loading bar
        self.loading_bar = loading_bar.LoadingBar(size_hint=(5/32, 1))
        self.toolbar_layout.add_widget(self.loading_bar)

        # Settings icon button
        self.settings_icon_button = button.Button(background_normal="/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/SettingsIcon.png", border=(0, 0, 0, 0), size_hint=(2/32, 1))
        self.toolbar_layout.add_widget(self.settings_icon_button)

    

    def _init_todays_notes_layout(self):
        pass



    def _init_tabs_content_layout(self):
        pass




    def create_default_filter(self):
        filters = lambda: None
        filters.note_name = ""
        filters.note_min_priority = 0
        filters.note_max_priority = 100
        filters.note_min_time = datetime.min
        filters.note_max_time = datetime.max
        filters.note_text = ""
        filters.category_name = ""
        filters.category_description = ""
        filters.tag_name = ""
        filters.tag_description = ""
        return filters



class KivyApplication(app.App):
    def build(self):
        window.Window.clearcolor = (50, 50, 50, 50)
        use_cases = UseCases.UseCases()
        return KivyApplicationLayout(use_cases, orientation="vertical")


if __name__ == "__main__":
    KivyApplication().run()


