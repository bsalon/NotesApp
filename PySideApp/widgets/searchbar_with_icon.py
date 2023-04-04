import pathlib
import sys

from PySide6 import QtWidgets, QtCore, QtGui



class SearchBarWithIcon(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(SearchBarWithIcon, self).__init__(*args, **kwargs)
        image_path = pathlib.Path(__file__).parent.parent.parent / "Images" / "SearchIcon.png"

        icon = QtGui.QIcon()
        icon.addFile(image_path.resolve().as_posix())
        searchicon = QtWidgets.QLabel(objectName="search_icon")
        searchicon.setPixmap(icon.pixmap(QtCore.QSize(20, 20)))

        self.searchbar = QtWidgets.QLineEdit(objectName="search_bar")
        self.searchbar.setPlaceholderText("Filter by name...")

        searchLayout = QtWidgets.QHBoxLayout(self)
        searchLayout.addWidget(searchicon)
        searchLayout.addWidget(self.searchbar)


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
        self.searchWidget = SearchBarWithIcon(objectName="search_container")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.searchWidget)

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
