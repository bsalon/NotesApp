from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

class ClickableLabel(QLabel):
    """
        A Label that emits a signal when clicked.
    """

    clicked = Signal()

    def __init__(self, *args):
        super().__init__(*args)

    def mousePressEvent(self, event):
        self.clicked.emit()

# example
app = QApplication([])
window = QWidget()
layout = QVBoxLayout(window)
labelA = ClickableLabel('Click on me for more.')
layout.addWidget(labelA)
labelB = QLabel('Here I am.')
layout.addWidget(labelB)
labelB.hide()
labelA.clicked.connect(labelB.show)
window.show()
app.exec_()
