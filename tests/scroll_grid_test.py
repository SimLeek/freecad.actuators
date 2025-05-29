from PySide2.QtWidgets import QMainWindow, QTableView, QAbstractItemView, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QApplication, QPushButton
from PySide2.QtCore import QAbstractTableModel, Qt, QModelIndex
from PySide2.QtGui import QColor, QKeyEvent

class InfiniteGridModel(QAbstractTableModel):
    def __init__(self, rows=10, cols=10, x_offset=-50, y_offset=-50, cell_callback=None):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.cell_callback = cell_callback

    def rowCount(self, parent=QModelIndex()):
        return self.rows

    def columnCount(self, parent=QModelIndex()):
        return self.cols

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not self.cell_callback:
            return None
        row = index.row()
        col = index.column()
        x = col + self.x_offset
        y = row + self.y_offset
        selectable, text, bg_color = self.cell_callback(x, y)
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
        selectable, _, _ = self.cell_callback(x, y)
        if not selectable:
            return Qt.NoItemFlags
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(section + self.x_offset)
            else:
                return str(section + self.y_offset)
        return None

    def shift_left(self):
        self.beginRemoveColumns(QModelIndex(), self.cols - 1, self.cols - 1)
        self.endRemoveColumns()
        self.beginInsertColumns(QModelIndex(), 0, 0)
        self.x_offset -= 1
        self.endInsertColumns()
        self.headerDataChanged.emit(Qt.Horizontal, 0, self.cols - 1)

    def shift_right(self):
        self.beginRemoveColumns(QModelIndex(), 0, 0)
        self.endRemoveColumns()
        self.beginInsertColumns(QModelIndex(), self.cols - 1, self.cols - 1)
        self.x_offset += 1
        self.endInsertColumns()
        self.headerDataChanged.emit(Qt.Horizontal, 0, self.cols - 1)

    def shift_up(self):
        self.beginRemoveRows(QModelIndex(), self.rows - 1, self.rows - 1)
        self.endRemoveRows()
        self.beginInsertRows(QModelIndex(), 0, 0)
        self.y_offset -= 1
        self.endInsertRows()
        self.headerDataChanged.emit(Qt.Vertical, 0, self.rows - 1)

    def shift_down(self):
        self.beginRemoveRows(QModelIndex(), 0, 0)
        self.endRemoveRows()
        self.beginInsertRows(QModelIndex(), self.rows - 1, self.rows - 1)
        self.y_offset += 1
        self.endInsertRows()
        self.headerDataChanged.emit(Qt.Vertical, 0, self.rows - 1)

    def set_position(self, x, y):
        # Shift grid to center (x, y) at (size//2, size//2)
        target_col = self.cols // 2
        target_row = self.rows // 2
        current_x = target_col + self.x_offset
        current_y = target_row + self.y_offset
        x_diff = x - current_x
        y_diff = y - current_y
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
            self.setCurrentIndex(self.model.index(col, self.model.cols - 1))
        elif event.key() == Qt.Key_Up and row == 0:
            self.model.shift_up()
            self.setCurrentIndex(self.model.index(0, col))
        elif event.key() == Qt.Key_Down and row == self.model.rows - 1:
            self.model.shift_down()
            self.setCurrentIndex(self.model.index(self.model.rows - 1, row))
        else:
            super().keyPressEvent(event)

def sample_cell_callback(x, y):
    # Sample callback for testing
    selectable = (x + y) % 2 != 0  # Selectable if x + y is odd
    if (x + y) % 3 == 0:
        text = f"[{x},{y}]"
        bg_color = QColor('lightblue')
    elif (x + y) % 3 == 1:
        text = f"({x},{y})"
        bg_color = QColor('lightgreen')
    else:
        text = f"{x},{y}"
        bg_color = None  # No background color
    return selectable, text, bg_color

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Infinite Selectable Grid")
        self.resize(800, 600)

        # Setup model and view
        self.cell_callback = sample_cell_callback
        self.model = InfiniteGridModel(rows=16, cols=10, x_offset=-10, y_offset=-10, cell_callback=self.cell_callback)
        self.view = CustomTableView(self.model)
        self.view.setModel(self.model)
        self.view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.view.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.view.setShowGrid(True)
        self.view.horizontalHeader().setDefaultSectionSize(50)
        self.view.verticalHeader().setDefaultSectionSize(12)
        # Disable scrollbars
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Connect selection signal
        self.view.selectionModel().selectionChanged.connect(self.on_selection_changed)

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

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Start at (0,0)
        self.set_selection(0, 0)

    def on_selection_changed(self, selected, deselected):
        indexes = selected.indexes()
        if indexes:
            index = indexes[0]
            x = index.column() + self.model.x_offset
            y = index.row() + self.model.y_offset
            print(f"Selected: ({x}, {y})")
            self.x_spin.blockSignals(True)
            self.y_spin.blockSignals(True)
            self.x_spin.setValue(x)
            self.y_spin.setValue(y)
            self.x_spin.blockSignals(False)
            self.y_spin.blockSignals(False)

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

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())