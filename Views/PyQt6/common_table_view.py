import sys

from PySide6 import QtWidgets, QtCore, QtGui


class CommonTableView(QtWidgets.QTableView):
    def __init__(self, header, data, stretch_column, sort_column=0, order=QtCore.Qt.AscendingOrder, *args, **kwargs):
        super(CommonTableView, self).__init__(*args, **kwargs)
        self.header = header
        self.data = data
        self.stretch_column = stretch_column
        self.sort_column = sort_column
        self.order = order
        
        self.model = CommonTableModel(header, data)
        self._create_proxy_model()
        self.setModel(self.filter_proxy_model)

        self._resize_table()
        
        align_delegate = TableCellAlignDelegate(QtCore.Qt.AlignCenter, self)
        self.setItemDelegate(align_delegate)
        
        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        
        self.setSortingEnabled(True)


    def get_selected_rows(self): # Uses -42 index to get the whole row
        selected_rows = []
        for selected_model_index in self.selectionModel().selectedRows():
            selected_rows.append(selected_model_index.data(-42))
        return selected_rows


    def delete_selection(self):
        selected_indices = []
        
        for selected_model_index in self.selectionModel().selectedRows():
            # selected_model_index.column() == 0
            # .data() -> returns first column
            # .data(-42) -> returns whole row -- see hack in .data()
            item = selected_model_index.data(-42)
            data_index = self.model.find_data_index(item)
            selected_indices.append(data_index)
        
        for selected_index in reversed(sorted(selected_indices)):
            self.model.removeRows(selected_index, 1)


    def replace_data(self, new_data):
        self.model = CommonTableModel(self.header, new_data)
        self.__create_proxy_model()
        self.setModel(self.filter_proxy_model)


    def replace_row(self, old_row, new_row):
        self.model.removeRow(old_row)
        self.model.insertRows(new_row)
        self.sortByColumn(self.sort_column, self.order)


    def add_row(self, new_row):
        self.model.insertRows(new_row)
        self.sortByColumn(self.sort_column, self.order)


    def _create_proxy_model(self):
        self.filter_proxy_model = QtCore.QSortFilterProxyModel()
        self.filter_proxy_model.setFilterKeyColumn(0)
        self.filter_proxy_model.setSourceModel(self.model)
        self.filter_proxy_model.sort(self.sort_column, self.order)


    def _resize_table(self):
        self.verticalHeader().hide()

        header = self.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(self.stretch_column, QtWidgets.QHeaderView.Stretch)

        self.resizeRowsToContents()



class CommonTableModel(QtCore.QAbstractTableModel):
    def __init__(self, header, data):
        super().__init__()
        self._data = data
        self.header = header


    def find_data_index(self, item_id):
        for index in range(len(self._data)):
            if item_id == self._data[index]:
                return index
        return 0


    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]
        return None


    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole and index.isValid():
            return self._data[index.row()][index.column()]
        # ugly hack to retrieve row
        elif role == -42 and index.isValid():
            return self._data[index.row()]


    def rowCount(self, index):
        return len(self._data)


    def columnCount(self, index):
        return len(self._data[0]) if len(self._data) > 0 else 0


    def insertRows(self, new_row, rows=1, parent=QtCore.QModelIndex()):
        start = len(self._data) - 1
        end = start + rows - 1

        self.beginInsertRows(parent, start, end)
        for i in range(rows):
            self._data.append(new_row) 
        self.endInsertRows()
        return True


    def removeRow(self, row):
        for i in range(len(self._data)):
            if row == self._data[i]:
                self.removeRows(i)
                return i


    def removeRows(self, position, rows=1, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)
        del self._data[position : position + rows]
        self.endRemoveRows()
        return True



class TableCellAlignDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, alignment, *args, **kwargs):
        super(TableCellAlignDelegate, self).__init__(*args, **kwargs)
        self.alignment_option = alignment


    def initStyleOption(self, option, index):
        super(TableCellAlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = self.alignment_option



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        data = [
            ["Food garbage", "Food garbage is really bad I should rather eat it", 2],
            ["Music for my ears", "This music is something special I will save it here", 0],
            ["It specialization", "This guy is a specialist", 0],
            ["It is what it is", "It really is", "what"],
            ["It is what it is", "It really is", "what"],
            ["It is what it is", "It really is", "what"],
            ["It is what it is", "It really is", "what"],
            ["It is what it is", "It really is", "what"],
            ["It is what it is", "It really is", "what"],
            ["It is what it is", "It really is", "what"],
            ["It is what it is", "It really is", "what"],
            ["It is what it is", "It really is", "what"],
            ["It is what it is", "It really is", "what"],
            ["It is what it is", "It really is", "what"],
            ["It is what it is", "It really is", "what"],
            ["It is what it is", "It really is", "what"],
            ["It is what it is", "It really is", "what"],
            ["It is what it is", "It really is", "what"],
            ["It is what it is", "It really is", "what"],
            ["It is what it is", "It really is", "what"],
            ["It is what it is", "It really is", "what"],
            ["It is what it is", "It really is", "what"],
            ["This note is special", "This note is special because it doesnt act like the others", 9],
        ]
        header = [
            "Name",
            "Description",
            "Date"
        ]

        self.table = CommonTableView(header, data, objectName="common_table")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.table)

        container = QtWidgets.QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    stylesheet="style.qss"
    with open(stylesheet, "r") as f:
        app.setStyleSheet(f.read())
    window = MainWindow()
    window.show()
    app.exec()
