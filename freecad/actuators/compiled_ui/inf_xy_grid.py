from PySide2.QtWidgets import QMainWindow, QTableView, QAbstractItemView, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QApplication, QPushButton
from PySide2.QtCore import QAbstractTableModel, Qt, QModelIndex
from PySide2.QtGui import QColor, QKeyEvent

class InfiniteGridModel(QAbstractTableModel):
    def __init__(self, rows=10, cols=10, x_offset=-50, y_offset=-50, cell_callback=None, row_header_callback=lambda x: x, col_header_callback=lambda x: x):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.cell_callback = cell_callback
        self.row_header_callback = row_header_callback
        self.col_header_callback = col_header_callback
        self.bounds = [None, None, None, None]  # tlbr

    def rowCount(self, parent=QModelIndex()):
        return self.rows

    def columnCount(self, parent=QModelIndex()):
        return self.cols

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not self.cell_callback:
            return None
        row = index.row()
        col = index.column()
        x = self.col_header_callback(col + self.x_offset)
        y = self.row_header_callback(row + self.y_offset)
        if (self.bounds[0] is not None and y<self.bounds[0]) or (self.bounds[1] is not None and x<self.bounds[1]) or (self.bounds[2] is not None and y>=self.bounds[2]) or (self.bounds[3] is not None and x>=self.bounds[3]):
            selectable, text, bg_color = False, "", QColor(127, 127, 127)
            #print(x, y, self.bounds)
        else:
            selectable, text, bg_color = self.cell_callback(x, y)
            if not isinstance(bg_color, QColor):
                if isinstance(bg_color, str):
                    bg_color = QColor(bg_color)
                elif isinstance(bg_color, (tuple, list)):
                    bg_color = QColor(*bg_color)
                else:  # guess
                    bg_color = QColor(bg_color)
        if role == Qt.DisplayRole:
            return text
        elif role == Qt.BackgroundRole and bg_color:
            return bg_color
        return None

    def flags(self, index):
        if not index.isValid() or not self.cell_callback:
            return Qt.NoItemFlags
        row = index.row()
        col = index.column()
        x = col + self.x_offset
        y = row + self.y_offset
        selectable, _, _ = self.cell_callback(self.col_header_callback(x), self.row_header_callback(y))
        if not selectable:
            return Qt.NoItemFlags
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self.col_header_callback(section + self.x_offset))
            else:
                return str(self.row_header_callback(section + self.y_offset))
        return None

    def shift_left(self):
        #print('l')
        if self.bounds[1] is None or self.col_header_callback(self.x_offset)>=self.bounds[1]:
            #print("shift_left")
            self.beginRemoveColumns(QModelIndex(), self.cols - 1, self.cols - 1)
            self.endRemoveColumns()
            self.beginInsertColumns(QModelIndex(), 0, 0)
            self.x_offset -= 1
            self.endInsertColumns()
            self.headerDataChanged.emit(Qt.Horizontal, 0, self.cols - 1)

    def shift_right(self):
        #print('r')
        if self.bounds[3] is None or self.col_header_callback(self.x_offset)<self.bounds[3]:
            #print("shift_right")
            self.beginRemoveColumns(QModelIndex(), 0, 0)
            self.endRemoveColumns()
            self.beginInsertColumns(QModelIndex(), self.cols - 1, self.cols - 1)
            self.x_offset += 1
            self.endInsertColumns()
            self.headerDataChanged.emit(Qt.Horizontal, 0, self.cols - 1)

    def shift_up(self):
        #print('u')
        if self.bounds[0] is None or self.row_header_callback(self.y_offset)>=self.bounds[0]:
            print("shift_up")
            self.beginRemoveRows(QModelIndex(), self.rows - 1, self.rows - 1)
            self.endRemoveRows()
            self.beginInsertRows(QModelIndex(), 0, 0)
            self.y_offset -= 1
            self.endInsertRows()
            self.headerDataChanged.emit(Qt.Vertical, 0, self.rows - 1)

    def shift_down(self):
        #print('d')
        #print(self.bounds[2], self.row_header_callback(self.y_offset))
        if self.bounds[2] is None or self.row_header_callback(self.y_offset)<self.bounds[2]:
            #print("shift_down")
            self.beginRemoveRows(QModelIndex(), 0, 0)
            self.endRemoveRows()
            self.beginInsertRows(QModelIndex(), self.rows - 1, self.rows - 1)
            self.y_offset += 1
            self.endInsertRows()
            self.headerDataChanged.emit(Qt.Vertical, 0, self.rows - 1)

    def set_position(self, x, y):
        # Shift grid to center (x, y) at (size//2, size//2)
        #target_col = self.cols // 2
        #target_row = self.rows // 2
        #current_x = target_col + self.x_offset
        #current_y = target_row + self.y_offset
        #x_diff = x - current_x
        #y_diff = y - current_y
        x_diff = x - self.x_offset
        y_diff = y - self.y_offset
        print(x_diff, y_diff)
        for _ in range(abs(x_diff)):
            if x_diff > 0:
                self.shift_right()
            elif x_diff < 0:
                self.shift_left()
        for _ in range(abs(y_diff)):
            if y_diff > 0:
                self.shift_down()
            elif y_diff < 0:
                self.shift_up()

class CustomTableView(QTableView):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def keyPressEvent(self, event: QKeyEvent):
        current = self.currentIndex()
        row = current.row()
        col = current.column()
        if event.key() == Qt.Key_Left and col == 0:
            self.model.shift_left()
            self.setCurrentIndex(self.model.index(row, 0))
        elif event.key() == Qt.Key_Right and col == self.model.cols - 1:
            self.model.shift_right()
            self.setCurrentIndex(self.model.index(row, self.model.cols - 1))
        elif event.key() == Qt.Key_Up and row == 0:
            self.model.shift_up()
            self.setCurrentIndex(self.model.index(0, col))
        elif event.key() == Qt.Key_Down and row == self.model.rows - 1:
            self.model.shift_down()
            self.setCurrentIndex(self.model.index(self.model.rows - 1, col))
        else:
            super().keyPressEvent(event)

'''def sample_cell_callback(x, y):
    """Sample callback for testing"""
    selectable = (x + y) % 2 != 0  # Selectable if x + y is odd
    if (x + y) % 3 == 0:
        text = f"[{x},{y}]"
        bg_color = QColor('lightblue')
    elif (x + y) % 3 == 1:
        text = f"({x},{y})"
        bg_color = QColor('lightgreen')
    else:
        text = f"{x},{y}"
        bg_color = None
    return selectable, text, bg_color'''

class InfXYGridWidget(QWidget):
    def __init__(self, parent=None, callback=lambda x, y:(True, f"{x},{y}", QColor(255, 255, 255)), rows=16, cols=10, x_offset=-10, y_offset=-10):
        super().__init__(parent)
        self.model = InfiniteGridModel(rows=rows, cols=cols, x_offset=x_offset, y_offset=y_offset, cell_callback=callback)
        self.view = CustomTableView(self.model)
        self.view.setModel(self.model)
        self.view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.view.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.view.setShowGrid(True)
        self.view.horizontalHeader().setDefaultSectionSize(60)
        self.view.verticalHeader().setDefaultSectionSize(12)
        # Disable scrollbars
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Connect selection signal
        self.view.selectionModel().selectionChanged.connect(self.on_selection_changed)
        self.selection_changed_callback = None

        # Shift buttons
        self.left_button = QPushButton("← Left")
        self.right_button = QPushButton("Right →")
        self.up_button = QPushButton("↑ Up")
        self.down_button = QPushButton("Down ↓")
        self.left_button.clicked.connect(self.model.shift_left)
        self.right_button.clicked.connect(self.model.shift_right)
        self.up_button.clicked.connect(self.model.shift_up)
        self.down_button.clicked.connect(self.model.shift_down)

        # Spinboxes
        self.x_spin = QSpinBox()
        self.x_spin.setRange(-1000000, 1000000)
        self.y_spin = QSpinBox()
        self.y_spin.setRange(-1000000, 1000000)
        self.x_spin.valueChanged.connect(self.on_spin_changed)
        self.y_spin.valueChanged.connect(self.on_spin_changed)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.left_button)
        button_layout.addWidget(self.right_button)
        button_layout.addWidget(self.up_button)
        button_layout.addWidget(self.down_button)
        layout.addLayout(button_layout)
        spin_layout = QHBoxLayout()
        spin_layout.addWidget(QLabel("X:"))
        spin_layout.addWidget(self.x_spin)
        spin_layout.addWidget(QLabel("Y:"))
        spin_layout.addWidget(self.y_spin)
        layout.addLayout(spin_layout)

        self.setLayout(layout)
        self.set_selection(0, 0)

    def set_callback(self, callback):
        self.model.cell_callback = callback
        # update for new callback
        self.update_cell_callback()

    def get_callback(self):
        return self.model.cell_callback

    def update_cell_callback(self):
        for c in range(self.model.cols):
            for r in range(self.model.rows):
                index = self.model.index(r, c)
                self.model.dataChanged.emit(index, Qt.DisplayRole)

    def on_selection_changed(self, selected, deselected):
        indexes = selected.indexes()
        if indexes:
            index = indexes[0]
            x = index.column() + self.model.x_offset
            y = index.row() + self.model.y_offset
            #print(f"Selected: ({x}, {y})")
            self.x_spin.blockSignals(True)
            self.y_spin.blockSignals(True)
            self.x_spin.setValue(x)
            self.y_spin.setValue(y)
            self.x_spin.blockSignals(False)
            self.y_spin.blockSignals(False)
        if self.selection_changed_callback is not None:
            self.selection_changed_callback(selected, deselected)

    def on_spin_changed(self):
        x = self.x_spin.value()
        y = self.y_spin.value()
        self.set_selection(x, y)

    def set_selection(self, x, y):
        self.model.set_position(x, y)
        row = self.model.rows // 2
        col = self.model.cols // 2
        index = self.model.index(row, col)
        self.view.setCurrentIndex(index)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Infinite Grid Demo")
        self.resize(800, 600)
        self.grid_widget = InfXYGridWidget()
        self.setCentralWidget(self.grid_widget)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())