import re
import traceback
try:
    from PySide2.QtWidgets import QLineEdit
    from PySide2.QtGui import QWheelEvent
    from PySide2.QtCore import Qt
except ImportError:
    from PySide.QtWidgets import QLineEdit
    from PySide.QtGui import QWheelEvent
    from PySide.QtCore import Qt
import math

class QForceEdit(QLineEdit):
    """A QLineEdit that parses force values and stores them internally in Newtons (N)."""

    FORCE_CONVERSIONS = {
        "n": "*1.0",
        "kn": "*1000.0",
        "mn": "*1000000.0",
        "gf": "*0.00980665",
        "kgf": "*9.80665",
        "lbf": "*4.44822",
        "kip": "*4448.22",
        "dyn": "*0.00001"
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.internal_n = 0.0  # Store force in Newtons
        self.display_unit = "N"  # Default display unit
        self._current_unit = None  # Last parsed unit
        self.textChanged.connect(self.update_internal_value)
        self.setFocusPolicy(Qt.WheelFocus)  # Enable wheel events

    def parse_force(self, text):
        """Parses the input, replacing unit names with their Newton multipliers and evaluating the expression."""
        text = text.lower().replace(" ", "")  # Remove spaces for uniform parsing
        self._current_unit = None  # Reset current unit
        max_pos = 0
        for unit, multiplier in self.FORCE_CONVERSIONS.items():
            last_pos = text.rfind(unit)
            if last_pos != -1:
                if last_pos > max_pos:
                    max_pos = last_pos
                    self._current_unit = unit
                text = text.replace(unit, multiplier)

        try:
            return eval(text, {"__builtins__": math.__dict__})  # Safe eval (no built-ins)
        except Exception:
            return traceback.format_exc()  # Return the full error traceback as a string

    def update_internal_value(self):
        """Parses input, updates internal N value, and sets tooltip if there's an error."""
        text = self.text().strip()
        value = self.parse_force(text)

        if isinstance(value, str):
            self.setToolTip(value)
            self.setStyleSheet("border: 1px solid red;")
        else:
            self.internal_n = value
            self.setToolTip(f"{self.internal_n:.4f}N")  # Clear error tooltip
            self.setStyleSheet("")  # Clear red border

    def get_n_value(self):
        """Returns the internally stored force in Newtons."""
        return self.internal_n

    def set_n_value(self, n_value):
        """Sets the internal N value and updates the displayed text without triggering update_internal_value."""
        self.internal_n = n_value
        self.blockSignals(True)  # Prevent triggering textChanged
        self.update_display()
        self.blockSignals(False)

    def set_display_unit(self, unit):
        """Sets the display unit and updates the displayed text."""
        if unit.lower() in self.FORCE_CONVERSIONS:
            self.display_unit = unit
            self.update_display()

    def update_display(self):
        """Updates the text to reflect the current N value in the chosen display unit."""
        converted_value = self.internal_n / eval('1.0'+self.FORCE_CONVERSIONS[self.display_unit.lower()], {"__builtins__": math.__dict__})
        self.setText(f"{converted_value:.2f}{self.display_unit}")  # 4 decimal places for small units
        self.setToolTip(f"{converted_value:.2f}{self.display_unit}")  # 4 decimal places for small units

    def wheelEvent(self, event: QWheelEvent):
        """Handles mouse wheel events to increment/decrement the displayed value by 1 in the current unit."""
        unit = self._current_unit if self._current_unit else self.display_unit
        multiplier = eval('1.0'+self.FORCE_CONVERSIONS[unit.lower()], {"__builtins__": math.__dict__})
        delta = event.angleDelta().y()
        if delta > 0:
            self.internal_n += 1.0 * multiplier  # Scroll up: add 1 in display unit
        elif delta < 0:
            self.internal_n -= 1.0 * multiplier  # Scroll down: subtract 1 in display unit
        event.accept()
        self.update_display()
