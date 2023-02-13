import sys
from PySide6.QtWidgets import QApplication, QWidget, QTableView, QMainWindow, QVBoxLayout, QLineEdit, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QSortFilterProxyModel, QAbstractTableModel, QSize, Slot
from PySide6.QtGui import QIcon


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QTableView()

        data = [
            [4, 9, 2],
            [1, "hello", 0],
            [3, 5, 0],
            [3, 3, "what"],
            ["this", 8, 9],
        ]

        self.model = TableModel(data)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setFilterKeyColumn(-1) # Search all columns.
        self.proxy_model.setSourceModel(self.model)

        self.proxy_model.sort(0, Qt.AscendingOrder)

        self.table.setModel(self.proxy_model)

        self.searchWidget = QWidget(objectName="search_container")
        self.searchWidget.setStyleSheet(
'''
QWidget#search_container
{
    border: 1px solid black;
    border-radius: 12px;
    background-color: white;
}
QWidget#search_bar
{
    border: none;
    background-color: white;
}
''')
        self.searchLayout = QHBoxLayout(self.searchWidget)
        
        icon = QIcon()
        icon.addFile("/home/benjaminsalon/diplom/NotesApp/Views/PyQt6/icons/SearchIcon.png")
        searchicon = QLabel(objectName="search_icon")
        searchicon.setPixmap(icon.pixmap(QSize(24, 24)))

        self.searchbar = QLineEdit(objectName="search_bar")
        self.searchbar.setPlaceholderText("Filter by name...")

        self.searchbutton = QPushButton("Filter")
        self.searchbutton.clicked.connect(self.magic) 

        self.searchLayout.addWidget(searchicon)
        self.searchLayout.addWidget(self.searchbar)
        self.searchLayout.addWidget(self.searchbutton)

        layout = QVBoxLayout()
        layout.addWidget(self.searchWidget)
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    @Slot()
    def magic(self):
        # You can choose the type of search by connecting to a different slot here.
        # see https://doc.qt.io/qt-5/qsortfilterproxymodel.html#public-slots
        # self.searchbar.textChanged.connect(self.proxy_model.setFilterFixedString)
        self.proxy_model.setFilterFixedString(self.searchbar.text())


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
