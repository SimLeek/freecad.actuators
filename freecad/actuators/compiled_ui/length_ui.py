import traceback
try:
    from PySide2.QtWidgets import QLineEdit, QApplication
    from PySide2.QtGui import QDoubleValidator
except ImportError:
    from PySide.QtWidgets import QLineEdit, QApplication
    from PySide.QtGui import QDoubleValidator

class QLengthEdit(QLineEdit):
    UNIT_CONVERSIONS = {
        "mm": "*1.0",
        "cm": "*10.0",
        "m": "*1000.0",
        "in": "*25.4",
        "ft": "*304.8"
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.internal_mm = 0.0  # Store value in mm
        self.display_unit = "mm"  # Default display unit
        self.textChanged.connect(self.update_internal_value)

    def parse_length(self, text):
        """Parses the input, replacing unit names with their mm multipliers and evaluating the expression."""
        # Replace all recognized units with their corresponding multipliers
        for unit, multiplier in self.UNIT_CONVERSIONS.items():
            text = text.lower().replace(unit, multiplier)
        try:
            return eval(text, {"__builtins__": {}})  # Safe eval (no built-ins)
        except Exception:
            return traceback.format_exc()  # Return the full error traceback as a string

    def update_internal_value(self):
        """Parses input, updates internal mm value, and sets tooltip if there's an error."""
        text = self.text().strip()
        value = self.parse_length(text)

        if isinstance(value, str):
            self.setToolTip(value)
            self.setStyleSheet("border: 1px solid red;")
        else:
            self.internal_mm = value
            self.setToolTip(f"{self.internal_mm:.2f}mm")  # Clear error tooltip
            self.setStyleSheet("")  # Clear red border

    def get_mm_value(self):
        """Returns the internally stored length in millimeters."""
        return self.internal_mm

    def set_mm_value(self, mm_value):
        """Sets the internal mm value and updates the displayed text without triggering update_internal_value."""
        self.internal_mm = mm_value
        self.blockSignals(True)  # Prevent triggering textChanged
        self.update_display()
        self.blockSignals(False)

    def set_display_unit(self, unit):
        """Sets the display unit and updates the displayed text."""
        if unit in self.UNIT_CONVERSIONS:
            self.display_unit = unit
            self.update_display()

    def update_display(self):
        """Updates the text to reflect the current mm value in the chosen display unit."""
        converted_value = self.internal_mm / eval('1.0'+self.UNIT_CONVERSIONS[self.display_unit], {"__builtins__": {}})
        self.setText(f"{converted_value:.2f}{self.display_unit}")
        self.setToolTip(f"{converted_value:.2f}{self.display_unit}")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    widget = QLengthEdit()
    widget.show()
    sys.exit(app.exec_())
