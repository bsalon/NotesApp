import sys

from PySide6 import QtWidgets, QtCore, QtGui


class CommonTableView(QtWidgets.QTableView):
    def __init__(self, header, data, *args, **kwargs):
        super(CommonTableView, self).__init__(*args, **kwargs)
        self.model = CommonTableModel(header, data)
        self.__create_proxy_model()
        self.setModel(self.filter_proxy_model)

        self.verticalHeader().hide()

        header = self.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

        self.resizeRowsToContents() # good enough

        align_delegate = TableCellAlignDelegate(QtCore.Qt.AlignCenter, self)
        self.setItemDelegate(align_delegate)
        
        self.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)


    def __create_proxy_model(self):
        self.filter_proxy_model = QtCore.QSortFilterProxyModel()
        self.filter_proxy_model.setFilterKeyColumn(0)
        self.filter_proxy_model.setSourceModel(self.model)
        self.filter_proxy_model.sort(0, QtCore.Qt.AscendingOrder)



class CommonTableModel(QtCore.QAbstractTableModel):
    def __init__(self, header, data):
        super().__init__()
        self._data = data
        self.header = header


    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]
        return None


    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole and index.isValid():
            return self._data[index.row()][index.column()]


    def rowCount(self, index):
        return len(self._data)


    def columnCount(self, index):
        return len(self._data[0])



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
