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

        # TODO: self.resizeRowsToContents() # good enough

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



class SearchBarWithIcon(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(SearchBarWithIcon, self).__init__(*args, **kwargs)

        icon = QtGui.QIcon()
        icon.addFile("/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/SearchIcon.png")
        searchicon = QtWidgets.QLabel(objectName="search_icon")
        searchicon.setPixmap(icon.pixmap(QtCore.QSize(24, 24)))

        self.searchbar = QtWidgets.QLineEdit(objectName="search_bar")
        self.searchbar.setPlaceholderText("Filter by name...")

        self.searchbutton = QtWidgets.QPushButton("Filter")
        # self.searchbutton.clicked.connect(self.magic)

        searchLayout = QtWidgets.QHBoxLayout(self)
        searchLayout.addWidget(searchicon)
        searchLayout.addWidget(self.searchbar)
        searchLayout.addWidget(self.searchbutton)


    # issue explained here - https://stackoverflow.com/questions/7276330/qt-stylesheet-for-custom-widget
    def paintEvent(self, event):
        option = QtWidgets.QStyleOption()
        option.initFrom(self)
        painter = QtGui.QPainter(self)
        style = self.style()
        style.drawPrimitive(QtWidgets.QStyle.PE_Widget, option, painter, self)



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

        self.searchWidget = SearchBarWithIcon(objectName="search_container")


        self.searchWidget.searchbutton.clicked.connect(self.magic)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.searchWidget)
        layout.addWidget(self.table)

        container = QtWidgets.QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


    @QtCore.Slot()
    def magic(self):
        # You can choose the type of search by connecting to a different slot here.
        # see https://doc.qt.io/qt-5/qsortfilterproxymodel.html#public-slots
        # self.searchbar.textChanged.connect(self.proxy_model.setFilterFixedString)
        self.table.filter_proxy_model.setFilterFixedString(self.searchWidget.searchbar.text())


app = QtWidgets.QApplication(sys.argv)
stylesheet="style.qss"
with open(stylesheet, "r") as f:
    app.setStyleSheet(f.read())
window = MainWindow()
window.show()
app.exec()
