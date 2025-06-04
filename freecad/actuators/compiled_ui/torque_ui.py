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

class QTorqueEdit(QLineEdit):
    """A QLineEdit that parses torque values and stores them internally in Newton-meters (N·m)."""

    TORQUE_CONVERSIONS = {
        "nm": "*1.0", "n⋅m": "*1.0", "n*m": "*1.0",
        "kgm": "*9.80665", "kg·m": "*9.80665", "kg*m": "*9.80665",
        "lbft": "*1.3558", "lb⋅ft": "*1.3558", "lb*ft": "*1.3558",
        "kgf.m": "*9.80665", "kgf⋅m": "*9.80665", "kgf*m": "*9.80665",
        "lbfft": "*1.3558", "lbf⋅ft": "*1.3558", "lbf*ft": "*1.3558",
        "lb-fft": "*1.3558",
        "kg*cm": "*0.0980665", "kg⋅cm": "*0.0980665", "kgcm": "*0.0980665",
        "lb*in": "*0.113", "lb⋅in": "*0.113", "lbin": "*0.113",
        "g*mm": "*0.00000980665", "g⋅mm": "*0.00000980665", "gmm": "*0.00000980665",
        "g*cm": "*0.0000980665", "g⋅cm": "*0.0000980665", "gcm": "*0.0000980665",
        "n*cm": "*0.01", "n⋅cm": "*0.01", "ncm": "*0.01"
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.internal_nm = 0.0  # Store torque in Newton-meters
        self.display_unit = "Nm"  # Default display unit
        self._current_unit = None  # Last parsed unit
        self.textChanged.connect(self.update_internal_value)
        self.setFocusPolicy(Qt.WheelFocus)  # Enable wheel events

    def parse_torque(self, text):
        """Parses the input, replacing unit names with their Newton-meter multipliers and evaluating the expression."""
        text = text.lower().replace(" ", "")  # Remove spaces for uniform parsing
        self._current_unit = None  # Reset current unit
        max_pos = 0
        for unit, multiplier in self.TORQUE_CONVERSIONS.items():
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
        """Parses input, updates internal Nm value, and sets tooltip if there's an error."""
        text = self.text().strip()
        value = self.parse_torque(text)

        if isinstance(value, str):
            self.setToolTip(value)
            self.setStyleSheet("border: 1px solid red;")
        else:
            self.internal_nm = value
            self.setToolTip(f"{self.internal_nm:.4f}Nm")  # Clear error tooltip
            self.setStyleSheet("")  # Clear red border

    def get_nm_value(self):
        """Returns the internally stored torque in Newton-meters."""
        return self.internal_nm

    def set_nm_value(self, nm_value):
        """Sets the internal Nm value and updates the displayed text without triggering update_internal_value."""
        self.internal_nm = nm_value
        self.blockSignals(True)  # Prevent triggering textChanged
        self.update_display()
        self.blockSignals(False)

    def set_display_unit(self, unit):
        """Sets the display unit and updates the displayed text."""
        if unit.lower() in self.TORQUE_CONVERSIONS:
            self.display_unit = unit
            self.update_display()

    def update_display(self):
        """Updates the text to reflect the current Nm value in the chosen display unit."""
        converted_value = self.internal_nm / eval('1.0'+self.TORQUE_CONVERSIONS[self.display_unit.lower()], {"__builtins__": {}})
        self.setText(f"{converted_value:.2f}{self.display_unit}")  # 4 decimal places for small units
        self.setToolTip(f"{converted_value:.2f}{self.display_unit}")  # 4 decimal places for small units

    def wheelEvent(self, event: QWheelEvent):
        """Handles mouse wheel events to increment/decrement the displayed value by 1 in the current unit."""
        unit = self._current_unit if self._current_unit else self.display_unit
        multiplier = eval('1.0'+self.TORQUE_CONVERSIONS[unit.lower()], {"__builtins__": math.__dict__})
        delta = event.angleDelta().y()
        if delta > 0:
            self.internal_nm += 1.0 * multiplier  # Scroll up: add 1 in display unit
        elif delta < 0:
            self.internal_nm -= 1.0 * multiplier  # Scroll down: subtract 1 in display unit
        self.blockSignals(True)
        self.update_display()
        self.blockSignals(False)
        event.accept()