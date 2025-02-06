import traceback

try:
    from PySide2.QtWidgets import QLineEdit
except:
    from PySide.QtWidgets import QLineEdit

class QEvalEdit(QLineEdit):
    """A QLineEdit that evaluates mathematical expressions and stores the result internally."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.internal_value = 0.0  # Store computed value
        self.textChanged.connect(self.update_internal_value)

    def parse_expression(self, text):
        """Parses the input and evaluates the mathematical expression safely."""
        text = text.replace(":", "/")  # Convert ratios to division
        text = text.replace("^", "**")  # Convert exponents

        try:
            return eval(text, {"__builtins__": {}})  # Safe eval (no built-ins)
        except Exception:
            return traceback.format_exc()  # Return full error traceback as a string

    def update_internal_value(self):
        """Parses input, updates internal value, and sets tooltip if there's an error."""
        text = self.text().strip()
        value = self.parse_expression(text)

        if isinstance(value, str):
            self.setToolTip(value)
            self.setStyleSheet("border: 1px solid red;")
        else:
            self.internal_value = value
            self.setToolTip(f"{value:.4f}")  # Clear error tooltip
            self.setStyleSheet("")  # Clear red border

    def get_value(self):
        """Returns the internally stored numeric value."""
        return self.internal_value

    def set_value(self, value):
        """Sets the internal value and updates the displayed text without triggering update_internal_value."""
        self.internal_value = value
        self.blockSignals(True)  # Prevent triggering textChanged
        self.setText(f"{value:.4f}")  # Display value with 4 decimal places
        self.setToolTip(f"{value:.4f}")  # Clear error tooltip
        self.blockSignals(False)
