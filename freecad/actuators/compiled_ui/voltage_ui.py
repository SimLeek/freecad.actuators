import re
import traceback
import math
try:
    from PySide2.QtWidgets import QLineEdit
    from PySide2.QtGui import QWheelEvent
    from PySide2.QtCore import Qt
except ImportError:
    from PySide.QtWidgets import QLineEdit
    from PySide.QtGui import QWheelEvent
    from PySide.QtCore import Qt

class QVoltageEdit(QLineEdit):
    """A QLineEdit that parses voltage values and stores them internally in volts (V)."""

    UNIT_CONVERSIONS = {
        "nv": "*1e9", "nV": "*1e9",
        "µv": "*1e6", "uv": "*1e6", "µV": "*1e6", "uV": "*1e6",
        "mv": "*1e3", "mV": "*1e3",
        "v": "*1.0", "V": "*1.0",
        "kv": "*1e-3", "kV": "*1e-3", "Kv": "*1e-3", "KV": "*1e-3",
        "Mv": "*1e-6", "MV": "*1e-6",
        "gv": "*1e-9", "gV": "*1e-9", "Gv": "*1e-9", "GV": "*1e-9",
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.internal_v = 0.0  # Store value in volts
        self.display_unit = "V"  # Default display unit
        self._current_unit = None  # Last parsed unit
        self.textChanged.connect(self.update_internal_value)
        self.setFocusPolicy(Qt.WheelFocus)  # Enable wheel events

    def parse_voltage(self, text):
        """Parses the input, replacing unit names with their volt multipliers and evaluating the expression."""
        text = text.replace(" ", "")  # Remove spaces for uniform parsing
        self._current_unit = None  # Reset current unit
        max_pos = 0
        for unit, multiplier in self.UNIT_CONVERSIONS.items():
            # Case-sensitive for MV and GV, case-insensitive for others
            last_pos = text.rfind(unit)
            if last_pos != -1 and last_pos > max_pos:
                max_pos = last_pos
                self._current_unit = unit
                text = text.replace(unit, multiplier)

        try:
            return eval(text, {"__builtins__": math.__dict__})  # Safe eval with math module
        except Exception:
            return traceback.format_exc()  # Return the full error traceback as a string

    def update_internal_value(self):
        """Parses input, updates internal volt value, and sets tooltip if there's an error."""
        text = self.text().strip()
        value = self.parse_voltage(text)

        if isinstance(value, str):
            self.setToolTip(value)
            self.setStyleSheet("border: 1px solid red;")
        else:
            self.internal_v = value
            self.setToolTip(f"{self.internal_v:.4f}V")  # Clear error tooltip
            self.setStyleSheet("")  # Clear red border

    def get_v_value(self):
        """Returns the internally stored voltage in volts."""
        return self.internal_v

    def set_v_value(self, v_value):
        """Sets the internal volt value and updates the displayed text without triggering update_internal_value."""
        self.internal_v = v_value
        self.blockSignals(True)  # Prevent triggering textChanged
        self.update_display()
        self.blockSignals(False)

    def set_display_unit(self, unit):
        """Sets the display unit and updates the displayed text."""
        if unit in self.UNIT_CONVERSIONS:
            self.display_unit = unit
            self.update_display()

    def update_display(self):
        """Updates the text to reflect the current volt value in the chosen display unit."""
        converted_value = self.internal_v / eval('1.0'+self.UNIT_CONVERSIONS[self.display_unit], {"__builtins__": math.__dict__})
        self.setText(f"{converted_value:.2f}{self.display_unit}")
        self.setToolTip(f"{converted_value:.2f}{self.display_unit}")

    def wheelEvent(self, event: QWheelEvent):
        """Handles mouse wheel events to increment/decrement the displayed value by 1 in the current unit."""
        unit = self._current_unit if self._current_unit else self.display_unit
        multiplier = eval('1.0'+self.UNIT_CONVERSIONS[unit], {"__builtins__": math.__dict__})
        delta = event.angleDelta().y()
        if delta > 0:
            self.internal_v += 1.0 * multiplier  # Scroll up: add 1 in display unit
        elif delta < 0:
            self.internal_v -= 1.0 * multiplier  # Scroll down: subtract 1 in display unit
        self.blockSignals(True)
        self.update_display()
        self.blockSignals(False)
        event.accept()