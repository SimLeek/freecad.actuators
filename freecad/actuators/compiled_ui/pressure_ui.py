import traceback
from PySide2.QtWidgets import QLineEdit


class QPressureEdit(QLineEdit):
    """A QLineEdit that parses pressure values and stores them internally in Pascals (N/m²)."""

    PRESSURE_CONVERSIONS = {
        "kpa": "*1e3",
        "mpa": "*1e6",
        "gpa": "*1e9",
        "pa": "*1.0", "n/m²": "*1.0", "n/m^2": "*1.0",
        "psi": "*6894.76",
        "ksi": "*6.89476e6",
        "kgf/mm²": "*9.80665e6", "kgf⋅mm²": "*9.80665e6", "kgf/mm^2": "*9.80665e6", "kgf⋅mm^2": "*9.80665e6", "kgf*mm²": "*9.80665e6", "kgf*mm^2": "*9.80665e6",
        "atm": "*101325.0"
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.internal_pa = 0.0  # Store pressure in Pascals (N/m²)
        self.display_unit = "Pa"  # Default display unit
        self.textChanged.connect(self.update_internal_value)

    def parse_pressure(self, text):
        """Parses the input, replacing unit names with their Pascal multipliers and evaluating the expression."""
        text = text.lower().replace(" ", "")  # Remove spaces for consistent parsing

        for unit, multiplier in self.PRESSURE_CONVERSIONS.items():
            text = text.replace(unit, multiplier)

        try:
            return eval(text, {"__builtins__": {}})  # Safe eval (no built-ins)
        except Exception:
            return traceback.format_exc()  # Return full error traceback as a string

    def update_internal_value(self):
        """Parses input, updates internal Pa value, and sets tooltip if there's an error."""
        text = self.text().strip()
        value = self.parse_pressure(text)

        if isinstance(value, str):
            self.setToolTip(value)
            self.setStyleSheet("border: 1px solid red;")
        else:
            self.internal_pa = value
            self.setToolTip(f"{self.internal_pa:.4f}Pa")  # Clear error tooltip
            self.setStyleSheet("")  # Clear red border

    def get_pa_value(self):
        """Returns the internally stored pressure in Pascals (N/m²)."""
        return self.internal_pa

    def set_pa_value(self, pa_value):
        """Sets the internal Pa value and updates the displayed text without triggering update_internal_value."""
        self.internal_pa = pa_value
        self.blockSignals(True)  # Prevent triggering textChanged
        self.update_display()
        self.blockSignals(False)

    def set_display_unit(self, unit):
        """Sets the display unit and updates the displayed text."""
        if unit in self.PRESSURE_CONVERSIONS:
            self.display_unit = unit
            self.update_display()

    def update_display(self):
        """Updates the text to reflect the current Pa value in the chosen display unit."""
        converted_value = self.internal_pa / eval('1.0'+self.PRESSURE_CONVERSIONS[self.display_unit], {"__builtins__": {}})
        self.setText(f"{converted_value:.4f}{self.display_unit}")  # 4 decimal places for precision
