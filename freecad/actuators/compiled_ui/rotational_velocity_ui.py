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

class QRotationalVelocityEdit(QLineEdit):
    """A QLineEdit that parses rotational velocity values and stores them internally in RPM."""

    UNIT_CONVERSIONS = {
        "rpm": "*1.0",
        "rad/s": f"*{60/(2*math.pi)}",  # rad/s to RPM: 1 rad/s = 60/(2π) RPM ≈ 9.54929658551372
        "deg/s": f"*{1.0/6}"  # deg/s to RPM: 1 deg/s = 1/6 RPM
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.internal_rpm = 0.0  # Store value in RPM
        self.display_unit = "rpm"  # Default display unit
        self._current_unit = None  # Last parsed unit
        self.textChanged.connect(self.update_internal_value)
        self.setFocusPolicy(Qt.WheelFocus)  # Enable wheel events

    def parse_rotational_velocity(self, text):
        """Parses the input, replacing unit names with their RPM multipliers and evaluating the expression."""
        text = text.lower().replace(" ", "")  # Remove spaces for uniform parsing
        self._current_unit = None  # Reset current unit
        max_pos = 0
        for unit, multiplier in self.UNIT_CONVERSIONS.items():
            last_pos = text.rfind(unit)
            if last_pos != -1:
                if last_pos > max_pos:
                    max_pos = last_pos
                    self._current_unit = unit
                text = text.replace(unit, multiplier)

        try:
            return eval(text, {"__builtins__": math.__dict__})  # Safe eval with math module
        except Exception:
            return traceback.format_exc()  # Return the full error traceback as a string

    def update_internal_value(self):
        """Parses input, updates internal RPM value, and sets tooltip if there's an error."""
        text = self.text().strip()
        value = self.parse_rotational_velocity(text)

        if isinstance(value, str):
            self.setToolTip(value)
            self.setStyleSheet("border: 1px solid red;")
        else:
            self.internal_rpm = value
            self.setToolTip(f"{self.internal_rpm:.2f}rpm")  # Clear error tooltip
            self.setStyleSheet("")  # Clear red border

    def get_rpm_value(self):
        """Returns the internally stored rotational velocity in RPM."""
        return self.internal_rpm

    def set_rpm_value(self, rpm_value):
        """Sets the internal RPM value and updates the displayed text without triggering update_internal_value."""
        self.internal_rpm = rpm_value
        self.blockSignals(True)  # Prevent triggering textChanged
        self.update_display()
        self.blockSignals(False)

    def set_display_unit(self, unit):
        """Sets the display unit and updates the displayed text."""
        if unit.lower() in self.UNIT_CONVERSIONS:
            self.display_unit = unit
            self.update_display()

    def update_display(self):
        """Updates the text to reflect the current RPM value in the chosen display unit."""
        converted_value = self.internal_rpm / eval('1.0'+self.UNIT_CONVERSIONS[self.display_unit.lower()], {"__builtins__": {}, "math": math})
        self.setText(f"{converted_value:.2f}{self.display_unit}")
        self.setToolTip(f"{converted_value:.2f}{self.display_unit}")

    def wheelEvent(self, event: QWheelEvent):
        """Handles mouse wheel events to increment/decrement the displayed value by 1 in the current unit."""
        unit = self._current_unit if self._current_unit else self.display_unit
        multiplier = eval('1.0'+self.UNIT_CONVERSIONS[unit.lower()], {"__builtins__": math.__dict__})
        delta = event.angleDelta().y()
        if delta > 0:
            self.internal_rpm += 1.0 * multiplier  # Scroll up: add 1 in display unit
        elif delta < 0:
            self.internal_rpm -= 1.0 * multiplier  # Scroll down: subtract 1 in display unit
        self.blockSignals(True)
        self.update_display()
        self.blockSignals(False)
        event.accept()