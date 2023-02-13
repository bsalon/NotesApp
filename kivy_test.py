'''
TabbedPanel
============

Test of the widget TabbedPanel.
'''

from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.lang import Builder

Builder.load_string("""

<Test>:
    size_hint: .5, .5
    pos_hint: {'center_x': .5, 'center_y': .5}
    do_default_tab: False

    TabbedPanelItem:
        text: 'Notes'
        Label:
            text: 'First tab content area'
    TabbedPanelItem:
        text: 'Tags'
        BoxLayout:
            Label:
                text: 'Second tab content area'
            Button:
                text: 'Button that does nothing'
    TabbedPanelItem:
        text: 'Categories'
        RstDocument:
            text:
                '\\n'.join(("Hello world", "-----------",
                "You are in the third tab."))
    TabbedPanelItem:
        text: 'Note filters'
        BoxLayout:
            Label:
                text: 'Second tab content area'
            Button:
                text: 'Button that does nothing'

""")


class Test(TabbedPanel):
    pass


class TabbedPanelApp(App):
    def build(self):
        return Test()


if __name__ == '__main__':
    TabbedPanelApp().run()

