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
import math

class QAngleEdit(QLineEdit):
    """A QLineEdit that parses angle expressions with units and stores the value internally in degrees."""

    UNIT_CONVERSIONS = {
        "°": "*1.0", "deg": "*1.0", "degrees": "*1.0",  # Degrees
        "rad": f"*{180/math.pi}", "radians": f"*{180/math.pi}",  # Radians to Degrees
        "gon": "*0.9", "grad": "*0.9", "gradians": "*0.9"  # Gradians to Degrees
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.internal_degrees = 0.0  # Store value in degrees
        self.display_unit = "°"  # Default display unit
        self._current_unit = None  # Last parsed unit
        self.textChanged.connect(self.update_internal_value)
        self.setFocusPolicy(Qt.WheelFocus)  # Enable wheel events

    def parse_angle(self, text):
        """Parses the input, replacing unit names with their degree multipliers and evaluating the expression."""
        text = text.lower().replace(" ", "")  # Normalize input
        self._current_unit = None  # Reset current unit
        max_pos = 0
        for unit, multiplier in self.UNIT_CONVERSIONS.items():
            last_pos = text.rfind(unit)
            if last_pos!=-1:
                if last_pos>max_pos:
                    max_pos=last_pos
                    self._current_unit = unit
                text = text.replace(unit, multiplier)
        try:
            return eval(text, {"__builtins__": math.__dict__})  # Safe eval (no built-ins)
        except Exception:
            return traceback.format_exc()  # Return full error traceback as a string

    def update_internal_value(self):
        """Parses input, updates internal degrees value, and sets tooltip if there's an error."""
        text = self.text().strip()
        value = self.parse_angle(text)

        if isinstance(value, str):
            self.setToolTip(value)
            self.setStyleSheet("border: 1px solid red;")
        else:
            self.internal_degrees = value
            self.setToolTip(f"{self.internal_degrees:.4f}°")  # Clear error tooltip
            self.setStyleSheet("")  # Clear red border

    def get_degrees_value(self):
        """Returns the internally stored angle in degrees."""
        return self.internal_degrees

    def set_degrees_value(self, degrees_value):
        """Sets the internal degrees value and updates the displayed text without triggering update_internal_value."""
        self.internal_degrees = degrees_value
        self.blockSignals(True)  # Prevent triggering textChanged
        self.update_display()
        self.blockSignals(False)

    def set_display_unit(self, unit):
        """Sets the display unit and updates the displayed text."""
        if unit in self.UNIT_CONVERSIONS:
            self.display_unit = unit
            self.update_display()

    def update_display(self):
        """Updates the text to reflect the current degrees value in the chosen display unit."""
        converted_value = self.internal_degrees / eval('1.0'+self.UNIT_CONVERSIONS[self.display_unit], {"__builtins__": {}})
        self.setText(f"{converted_value:.4f}{self.display_unit}")

    def wheelEvent(self, event: QWheelEvent):
        """Handles mouse wheel events to increment/decrement the displayed value by 1 in the current unit."""
        unit = self._current_unit if self._current_unit else self.display_unit
        multiplier = eval('1.0'+self.UNIT_CONVERSIONS[unit], {"__builtins__": math.__dict__})
        delta = event.angleDelta().y()
        if delta > 0:
            self.internal_degrees += 1.0 * multiplier  # Scroll up: add 1 in display unit
        elif delta < 0:
            self.internal_degrees -= 1.0 * multiplier  # Scroll down: subtract 1 in display unit
        event.accept()
        self.update_display()
