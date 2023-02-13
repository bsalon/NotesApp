from PySide6 import QtCore, QtGui, QtWidgets

import sys


class Window(QtWidgets.QMainWindow):

    def __init__(self, qtpy):
        super().__init__()
        self.qtpy = qtpy
        self.setMinimumSize(250, 150)
        self.resize(600, 450)

# widget has layout
# - sidebar has sidebar_layout
#   - sidebar_label

class ThemeTool(Window):

    def __init__(self, qtpy):
        super().__init__(qtpy)
        self.setWindowTitle("qtpy-rant Theme Tool")

        layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight)
        
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        sidebar = QtWidgets.QWidget()
        sidebar.setMaximumWidth(150)
        
        sidebar_layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.TopToBottom)
        sidebar.setLayout(sidebar_layout)
        layout.addWidget(sidebar)

        sidebar_label = QtWidgets.QLabel()
        sidebar_label.setWordWrap(True)
        sidebar_label.setText("The Theme Tool is used to preview a theme and detect errors The Theme Tool is used to preview a theme and detect errors The Theme Tool is used to preview a theme and detect errors The Theme Tool is used to preview a theme and detect errors The Theme Tool is used to preview a theme and detect errors The Theme Tool is used to preview a theme and detect errors The Theme Tool is used to preview a theme and detect errors The Theme Tool is used to preview a theme and detect errors The Theme Tool is used to preview a theme and detect errors")
        sidebar_layout.addWidget(sidebar_label, alignment=QtCore.Qt.AlignTop)

        #theme_area_layout = QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.TopToBottom)
        #theme_area = QtWidgets.QWidget()
        #theme_area.setLayout(theme_area_layout)
        #layout.addWidget(theme_area, 1)


qapplication = QtWidgets.QApplication(sys.argv)
main_window = ThemeTool(None)
main_window.show()
qapplication.exec_()
