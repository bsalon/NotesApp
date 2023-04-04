import math
import sys

from PySideApp.widgets import clickable_label

from PySide6 import QtCore, QtWidgets, QtGui


class PaginationLabels(QtWidgets.QWidget):
    page_changed = QtCore.Signal()

    def __init__(self, page_size, items_count, *args, **kwargs):
        super(PaginationLabels, self).__init__(*args, **kwargs)
        self.page_size = page_size
        self.items_count = items_count

        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.current_page = 1
        self.create_labels()


    def create_labels(self):
        self.clear_layout()

        last_page = self.pages_count()
        prev_page = 1 if self.current_page - 1 < 1 else self.current_page - 1
        next_page = last_page if self.current_page + 1 > last_page else self.current_page + 1

        list_pages = {1, prev_page, self.current_page, next_page, last_page}

        self.prev_page_label = clickable_label.ClickableQLabel("<<", objectName="pagination")
        self.prev_page_label.clicked.connect(self.go_to_prev_page)
        
        list_labels = [self.prev_page_label]
        for page in list_pages:
            page_label = clickable_label.ClickableQLabel(str(page), objectName="pagination")
            if page == self.current_page:
                page_label.setObjectName("pagination_current_page")
            page_label.clicked.connect(lambda p=page: self.go_to_page(p))
            list_labels.append(page_label)

        self.next_page_label = clickable_label.ClickableQLabel(">>", objectName="pagination")
        self.next_page_label.clicked.connect(self.go_to_next_page)
        list_labels.append(self.next_page_label)

        for label in list_labels:
            self.layout.addWidget(label)


    def pages_count(self):
        return math.ceil(self.items_count / self.page_size)


    # https://stackoverflow.com/questions/4528347/clear-all-widgets-in-a-layout-in-pyqt
    def clear_layout(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)


    @QtCore.Slot()
    def go_to_prev_page(self):
        self.current_page -= 1
        self.current_page = self.current_page if self.current_page >= 1 else 1
        self.page_changed.emit()
        self.create_labels()


    @QtCore.Slot()
    def go_to_next_page(self):
        last_page = self.pages_count()
        self.current_page += 1
        self.current_page = self.current_page if self.current_page <= last_page else last_page
        self.page_changed.emit()
        self.create_labels()


    @QtCore.Slot()
    def go_to_page(self, page):
        self.current_page = page
        self.page_changed.emit()
        self.create_labels()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet('''
    QLabel#pagination {
        border: 1px dotted black;
    }
    
    QLabel#pagination_current_page {
        border: 1px dotted black;
        background-color: #ffc957;
    }
    ''')
    pagination = PaginationLabels(10, 35)
    pagination.show()
    sys.exit(app.exec())
