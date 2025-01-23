import re
import traceback
from fractions import Fraction
from PySide2.QtWidgets import QLineEdit


class QFractionEdit(QLineEdit):
    """A QLineEdit that parses fractions from user input and stores the value as a Fraction object."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.internal_value = Fraction(0)  # Store the value internally as a Fraction
        self.textChanged.connect(self.update_internal_value)

    def parse_fraction(self, text):
        """Parses the input, converts numbers to Fraction, and evaluates the expression."""
        text = text.replace(":", "/")  # Convert ratios to division
        # Regex to match numbers, including decimals and scientific notation
        number_regex = re.compile(r"(?<!\w)(-?\d+(\.\d+)?([eE][-+]?\d+)?)(?!\w)")

        # Replace all matched numbers with Fraction(number)
        text = number_regex.sub(lambda m: f"Fraction({m.group(0)})", text)

        try:
            return eval(text, {"__builtins__": {}}, {"Fraction": Fraction})  # Safe eval with Fraction
        except Exception:
            return traceback.format_exc()  # Return full error traceback as a string

    def update_internal_value(self):
        """Updates the stored Fraction value based on user input."""
        result = self.parse_fraction(self.text())

        if isinstance(result, Fraction):
            self.internal_value = result
            self.setToolTip(f"{result.numerator}:{result.denominator}")
        else:
            self.setToolTip(result)  # Show full error message in tooltip

    def get_value(self):
        """Returns the stored Fraction value."""
        return self.internal_value

    def set_value(self, fraction):
        """Sets the displayed value while keeping the internal Fraction representation."""
        if isinstance(fraction, Fraction):
            self.internal_value = fraction
            self.blockSignals(True)  # Prevent triggering update_internal_value
            self.setText(f"{fraction.numerator}:{fraction.denominator}")
            self.blockSignals(False)
