from PySide2.QtWidgets import QToolButton
from PySide2.QtGui import QIcon
from PySide2.QtCore import Signal
import os


class LockUnlockButton(QToolButton):
    lock_state_changed = Signal(bool)  # Signal emitted when is_locked changes

    def __init__(self, parent=None):
        super().__init__(parent)

        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.unlock_icon_path = os.path.join(current_directory, 'unlock_icon.png')
        self.lock_icon_path = os.path.join(current_directory, 'lock_icon.png')

        self._is_locked = False
        self.update_icon()

        self.clicked.connect(self.toggle_lock)

    @property
    def is_locked(self):
        return self._is_locked

    @is_locked.setter
    def is_locked(self, bool_val):
        self._is_locked = bool_val
        self.update_icon()
        self.lock_state_changed.emit(self._is_locked)  # Emit signal

    def update_icon(self):
        icon_path = self.lock_icon_path if self._is_locked else self.unlock_icon_path
        icon = QIcon(icon_path)
        self.setIcon(icon)

    def toggle_lock(self):
        self._is_locked = not self._is_locked
        self.update_icon()
        self.lock_state_changed.emit(self._is_locked)  # Emit signal