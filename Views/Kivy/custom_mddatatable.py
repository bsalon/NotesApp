from kivymd.uix import datatables

class CustomMDDataTable(datatables.MDDataTable):
    def __init__(self, *args, **kwargs):
        super(CustomMDDataTable, self).__init__(*args, **kwargs)
        self.selected_rows = []
        self.header.ids.check.opacity = 0
        self.header.ids.check.disabled = True

    def on_check_press(self, current_row):
        if current_row in self.selected_rows:
            self.selected_rows.remove(current_row)
        else:
            self.selected_rows.append(current_row)
