from kivymd.uix import datatables


class CustomMDDataTable(datatables.MDDataTable):
    def __init__(self, *args, **kwargs):
        super(CustomMDDataTable, self).__init__(*args, **kwargs)
        self.selected_rows = []
        
        self.header.ids.check.opacity = 0
        self.header.ids.check.disabled = True

        self.ids.container.padding = (0, 0, 0, 0)


    def on_check_press(self, current_row):
        if current_row in self.selected_rows:
            self.selected_rows.remove(current_row)
        else:
            self.selected_rows.append(current_row)


    def update_row_data(self, instance_data_table, data):
        super(CustomMDDataTable, self).update_row_data(instance_data_table, data)
        self.table_data.select_all("normal")
        self.selected_rows = []


    def update_row(self, old_data, new_data):
        super(CustomMDDataTable, self).update_row(old_data, new_data)
        self.table_data.select_all("normal")
        self.selected_rows = []


    def delete_selection(self):
        for row in self.selected_rows:
            row_data_value = next((v for i, v in enumerate(self.row_data) if v[0] == row[0]), None)
            if row_data_value:
                self.remove_row(row_data_value)
        self.table_data.select_all("normal")
        self.selected_rows = []


    def delete_rows(self, rows):
        for row in rows:
            row_data_value = next((v for i, v in enumerate(self.row_data) if v[0] == row[0]), None)
            if row_data_value:
                self.remove_row(row_data_value)
                if row in self.selected_rows:
                    self.selected_rows.pop(row)
        self.table_data.select_all("normal")
        self.selected_rows = []
