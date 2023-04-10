from kivy.core import window
from kivy.lang import Builder
from kivy.uix import boxlayout, button, label, switch, tabbedpanel

from KivyApp.dialogs import advanced_filter_dialog, category_dialog, filter_dialog, note_dialog, settings_dialog, tag_dialog
from KivyApp.widgets import custom_mddatatable, pagination_labels, searchbar_with_icon, time_label

import pathlib

Builder.load_file((pathlib.Path(__file__).parent / "styled_widgets.kv").resolve().as_posix())


# LABELS

class FastFilterLabel(label.Label):
    def __init__(self, *args, **kwargs):
        super(FastFilterLabel, self).__init__(*args, **kwargs)


class FastFilterRefLabel(label.Label):
    def __init__(self, *args, **kwargs):
        super(FastFilterRefLabel, self).__init__(*args, **kwargs)
        window.Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, window, pos):
        if self.collide_point(*pos):
            self.color = (166/255, 94/255, 227/255, 255/255)
        else:
            self.color = (0/255, 108/255, 229/255, 255/255)


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
        window.Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, window, pos):
        if self.collide_point(*pos):
            self.background_color = (239/255, 185/255, 71/255, 255/255)
            self.bold = True
        else:
            self.background_color = (255/255, 201/255, 87/255, 255/255)
            self.bold = False


class ToolbarButton(button.Button):
    def __init__(self, background_image, *args, **kwargs):
        super(ToolbarButton, self).__init__(*args, **kwargs)
        self.background_normal = background_image
        self.background_disabled_normal = background_image
        self.background_disabled_down = background_image
        window.Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, window, pos):
        if self.collide_point(*pos) and not self.disabled:
            self.background_color = (239/255, 185/255, 71/255, 255/255)
        else:
            self.background_color = (255/255, 201/255, 87/255, 255/255) if not self.disabled else (255/255, 201/255, 87/255, 60/255)


# SWITCH

class NotesToggleSwitch(switch.Switch):
    def __init__(self, *args, **kwargs):
        super(NotesToggleSwitch, self).__init__(*args, **kwargs)


# LAYOUTS

class ToolbarButtonBox(boxlayout.BoxLayout):
    def __init__(self, *args, **kwargs):
        super(ToolbarButtonBox, self).__init__(*args, **kwargs)


class ToolbarLayout(boxlayout.BoxLayout):
    def __init__(self, *args, **kwargs):
        super(ToolbarLayout, self).__init__(*args, **kwargs)


class TodaysNotesLayout(boxlayout.BoxLayout):
    def __init__(self, *args, **kwargs):
        super(TodaysNotesLayout, self).__init__(*args, **kwargs)


class TabsContentLayout(boxlayout.BoxLayout):
    def __init__(self, *args, **kwargs):
        super(TabsContentLayout, self).__init__(*args, **kwargs)


class TabToolbarLayout(boxlayout.BoxLayout):
    def __init__(self, *args, **kwargs):
        super(TabToolbarLayout, self).__init__(*args, **kwargs)


class SearchBarWithIcon(searchbar_with_icon.SearchBarWithIcon):
    def __init__(self, *args, **kwargs):
        super(SearchBarWithIcon, self).__init__(*args, **kwargs)


class NotesTabLayout(boxlayout.BoxLayout):
    def __init__(self, *args, **kwargs):
        super(NotesTabLayout, self).__init__(*args, **kwargs)


class PaginationLabels(pagination_labels.PaginationLabels):
    def __init__(self, page_size, items_count, *args, **kwargs):
        super(PaginationLabels, self).__init__(page_size, items_count, *args, **kwargs)


# TAB

class NotesTabbedPanel(tabbedpanel.TabbedPanel):
    def __init__(self, *args, **kwargs):
        super(NotesTabbedPanel, self).__init__(*args, **kwargs)


class NotesTabbedPanelItem(tabbedpanel.TabbedPanelItem):
    def __init__(self, *args, **kwargs):
        super(NotesTabbedPanelItem, self).__init__(*args, **kwargs)


# TABLE

class CustomMDDataTable(custom_mddatatable.CustomMDDataTable):
    def __init__(self, *args, **kwargs):
        super(CustomMDDataTable, self).__init__(*args, **kwargs)
    

# POPUPS / DIALOGS

class AdvancedFilterDialog(advanced_filter_dialog.AdvancedFilterDialog):
    def __init__(self, *args, **kwargs):
        super(AdvancedFilterDialog, self).__init__(*args, **kwargs)


class NoteDialog(note_dialog.NoteDialog):
    def __init__(self, *args, **kwargs):
        super(NoteDialog, self).__init__(*args, **kwargs)


class CategoryDialog(category_dialog.CategoryDialog):
    def __init__(self, *args, **kwargs):
        super(CategoryDialog, self).__init__(*args, **kwargs)


class TagDialog(tag_dialog.TagDialog):
    def __init__(self, *args, **kwargs):
        super(TagDialog, self).__init__(*args, **kwargs)


class FilterDialog(filter_dialog.FilterDialog):
    def __init__(self, *args, **kwargs):
        super(FilterDialog, self).__init__(*args, **kwargs)


class SettingsDialog(settings_dialog.SettingsDialog):
    def __init__(self, *args, **kwargs):
        super(SettingsDialog, self).__init__(*args, **kwargs)

