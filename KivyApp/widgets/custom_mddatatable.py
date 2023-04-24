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


    def update_table_data(self, instance_data_table, data):
        super(CustomMDDataTable, self).update_row_data(instance_data_table, data)
        self.table_data.select_all("normal")
        self.selected_rows = []


    def update_row(self, old_data, new_data):
        super(CustomMDDataTable, self).update_row(old_data, new_data)
        self.table_data.select_all("normal")
        self.selected_rows = []


    def delete_selection(self):
        rows_to_delete = []
        for index, row in enumerate(self.selected_rows):
            row_data_value = [value for value in self.row_data if value[0] == row[0]]
            if len(row_data_value) > 0:
                rows_to_delete.append(row_data_value[0])

        for row in rows_to_delete:
            if row in self.row_data:
                self.remove_row(row)
        self.table_data.select_all("normal")
        self.selected_rows = []


    def delete_rows(self, rows):
        rows_to_delete = []
        for row in rows:
            row_data_value = [value for value in self.row_data if value[0] == row[0]]
            if len(row_data_value) > 0:
                rows_to_delete.append(row_data_value[0])
            
        for row in rows_to_delete:
            self.remove_row(row)
        
        self.table_data.select_all("normal")
        self.selected_rows = []
