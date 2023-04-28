from tkinter import ttk

class CustomTtkStyle(ttk.Style):
    def __init__(self, *args, **kwargs):
        super(CustomTtkStyle, self).__init__(*args, **kwargs)
        self.theme_use("clam")

        self.configure("window.TFrame",
            background="black",
            bordercolor="white",
            relief="groove"
        )

        self.configure("todays_notes_container.TFrame",
            background="#d7eb5a",
            borderwidth=1,
            relief="groove",
            bordercolor="black"
        )
        
        self.configure("toolbar_container.TFrame",
            background="#ffc957",
            borderwidth=1,
            relief="groove",
            bordercolor="black"
        )

        self.configure("tabs_content_container.TFrame",
            background="#f1f6be",
            borderwidth=1,
            relief="groove",
            bordercolor="black"
        )
        
        self.configure("collapsable_frame_row.TFrame",
            background="#e9f29b",
            borderwidth=1,
            relief="groove",
            bordercolor="black",
        )
        
        self.configure("collapsable_frame_row_check.TFrame",
            background="#d7eb5a",
            borderwidth=1,
            relief="groove",
            bordercolor="black",
        )

        self.configure("scrollable_interior.TFrame",
            background="#f1f6be",
            borderwidth=1,
            relief="groove",
            bordercolor="black",
        )

        self.configure("search_container.TFrame",
            background="white",
            borderwidth=1,
            relief="groove",
            bordercolor="black"
        )



        self.configure("LoadingBar.Horizontal.TProgressbar",
            bordercolor="white",
            background="#92d36e",
            darkcolor="white",
            lightcolor="white",
            troughcolor="white"
        )


        self.element_create("Plain.Notebook.tab", "from", "default")
        self.layout("TNotebook.Tab",
            [('Plain.Notebook.tab', {'children':
                [('Notebook.padding', {'side': 'top', 'children':
                    [('Notebook.focus', {'side': 'top', 'children':
                        [('Notebook.label', {'side': 'top', 'sticky': ''})],
                    'sticky': 'nswe'})],
                'sticky': 'nswe'})],
            'sticky': 'nswe'})])
        self.configure("TNotebook",
            background="#f1f6be",
        )
        self.configure("TNotebook.Tab",
            foreground="black",
            borderwidth=3,
        )


        self.configure("Vertical.TScrollbar",
            gripcount=0,
            background="#d7eb5a",
            troughcolor="white",
            borderwidth=2,
            bordercolor="black",
            lightcolor="#d7eb5a",
            darkcolor="#d7eb5a",
            arrowsize=8
        )
        self.map("Vertical.TScrollbar",
            background=[('!active', '#d7eb5a'),
                        ('active', '#d7eb5a')],
        )


        self.configure("searchbar_entry.TEntry",
            background="white",
            borderwidth=0,
            highlightthickness=0,
            bordercolor="white"
        )
        self.map("searchbar_entry.TEntry",
                bordercolor=[('!active', 'white'),
                            ('active', 'white')]
        )
        self.configure("searchbar_placeholder.TEntry",
            background="white",
            borderwidth=0,
            highlightthickness=0,
            bordercolor="white",
            foreground="grey"
        )


        self.configure("today_notes_icon_button.TButton",
            foreground="black",
            background="#ffc957"
        )
        self.map("today_notes_icon_button.TButton",
                background=[('!active', '#ffc957'),
                            ('active', '#efb947')],
                relief=[('pressed', 'flat'),
                        ('!pressed', 'flat')]
        )

        self.configure("toolbar_icon_button.TButton",
            background="#ffc957",
        )
        self.map('toolbar_icon_button.TButton',
            background=[('disabled', '#ffc957'),
                        ('active', '#efb947')],
            relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')]
        )

        self.configure("collapsable_frame_button.TButton",
            background="#e9f29b"
        )
        self.map("collapsable_frame_button.TButton",
            background=[('!active', '#e9f29b'),
                        ('active', '#f1f6be')],
            relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')]
        )
        
        self.configure("collapsable_frame_button_check.TButton",
            background="#d7eb5a"
        )
        self.map("collapsable_frame_button_check.TButton",
            background=[('!active', '#d7eb5a'),
                        ('active', '#f1f6be')],
            relief=[('pressed', 'flat'),
                    ('!pressed', 'flat')]
        )


        self.configure("text_link.TLabel",
            background="#ffc957",
            foreground="#006ce5"
        )
        self.configure('hover_text_link.TLabel',
            background="#ffc957",
            foreground="#a65ee3"
        )

        self.configure("toolbar_time.TLabel",
            foreground="black",
            background="#ffc957"
        )

        self.configure("todays_notes_header.TLabel",
            foreground="black",
            background="#d7eb5a"
        )

        self.configure("pagination.TLabel",
            foreground="black",
            background="#f1f6be",
            borderwidth=2,
            relief="groove"
        )
        self.configure("pagination_current_page.TLabel",
            foreground="black",
            background="#ffc957",
            borderwidth=2,
            relief="groove"
        )

        self.configure("filterbar_label.TLabel",
            foreground="black",
            background="#f1f6be"
        )

        self.configure("collapsable_frame_label.TLabel",
            foreground="black",
            background="#e9f29b"
        )
        
        self.configure("collapsable_frame_label_check.TLabel",
            foreground="black",
            background="#d7eb5a"
        )
        
        self.configure("collapsable_frame_content_label.TLabel",
            foreground="black",
            background="#f7fade",
        )

        # Inspired by https://stackoverflow.com/questions/58559865/tkinter-checkbutton-different-image
        self.configure("no_indicatoron.TCheckbutton",
            background="white"
        )
        self.map('no_indicatoron.TCheckbutton',
            background=[('!active', 'white'),
                        ('active', 'white')],
        )
        self.layout('no_indicatoron.TCheckbutton',
            [('Checkbutton.padding', {'sticky': 'nswe', 'children': [
                ('Checkbutton.focus', {'side': 'left', 'sticky': 'w', 'children':
                      [('Checkbutton.label', {'sticky': 'nswe'})]})
            ]})],
        )

        self.configure("collapsable_frame_checkbutton.TCheckbutton",
            background="#e9f29b"
        )
        self.map("collapsable_frame_checkbutton.TCheckbutton",
            background=[('!active', '#e9f29b'),
                        ('active', '#e9f29b')],
        )

        self.configure("collapsable_frame_checkbutton_check.TCheckbutton",
            background="#d7eb5a"
        )
        self.map("collapsable_frame_checkbutton_check.TCheckbutton",
            background=[('!active', '#d7eb5a'),
                        ('active', '#d7eb5a')],
        )

        self.configure("Treeview",
            background="#e9f29b", 
            fieldbackground="#e9f29b",
            foreground="black"
        )
        self.configure('Treeview.Heading',
            background="#d7eb5a"
        )
        self.map("Treeview",
            background=[("selected", "#d7eb5a")],
            foreground=[("selected", "black")]
        )


