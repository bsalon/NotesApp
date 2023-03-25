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


    def update_row(self, old_data, new_data):
        super(CustomMDDataTable, self).update_row(old_data, new_data)
        self.selected_rows = [new_data]


    def delete_selection(self):
        for row in self.selected_rows:
            row_data_value = next((v for i, v in enumerate(self.row_data) if v[0] == row[0]), None)
            self.remove_row(row_data_value)
        self.table_data.select_all("normal")
        self.selected_rows = []


    def delete_rows(self, rows):
        for row in rows:
            row_data_value = next((v for i, v in enumerate(self.row_data) if v[0] == row[0]), None)
            self.remove_row(row_data_value)
            if row in self.selected_rows:
                self.selected_rows.pop(row)
        self.table_data.select_all("normal")
