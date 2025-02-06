import re
import traceback
try:
    from PySide2.QtWidgets import QLineEdit
except ImportError:
    from PySide.QtWidgets import QLineEdit

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
        self.textChanged.connect(self.update_internal_value)

    def parse_force(self, text):
        """Parses the input, replacing unit names with their Newton multipliers and evaluating the expression."""
        text = text.lower().replace(" ", "")  # Remove spaces for uniform parsing

        for unit, multiplier in self.FORCE_CONVERSIONS.items():
            text = text.replace(unit, multiplier)

        try:
            return eval(text, {"__builtins__": {}})  # Safe eval (no built-ins)
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
        if unit in self.FORCE_CONVERSIONS:
            self.display_unit = unit
            self.update_display()

    def update_display(self):
        """Updates the text to reflect the current N value in the chosen display unit."""
        converted_value = self.internal_n / eval('1.0'+self.FORCE_CONVERSIONS[self.display_unit.lower()], {"__builtins__": {}})
        self.setText(f"{converted_value:.2f}{self.display_unit}")  # 4 decimal places for small units
        self.setToolTip(f"{converted_value:.2f}{self.display_unit}")  # 4 decimal places for small units
