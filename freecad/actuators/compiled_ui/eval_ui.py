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

class QEvalEdit(QLineEdit):
    """A QLineEdit that evaluates mathematical expressions and stores the result internally."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.internal_value = 0.0  # Store computed value
        self.textChanged.connect(self.update_internal_value)
        self.setFocusPolicy(Qt.WheelFocus)  # Enable wheel events

    def parse_expression(self, text):
        """Parses the input and evaluates the mathematical expression safely."""
        text = text.replace(":", "/")  # Convert ratios to division
        text = text.replace("^", "**")  # Convert exponents

        try:
            return eval(text, {"__builtins__": math.__dict__})  # Safe eval
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

    def update_display(self):
        """Updates the text to reflect the current N value in the chosen display unit."""
        self.setText(f"{self.internal_value}")  # 4 decimal places for small units
        self.setToolTip(f"{self.internal_value}")  # 4 decimal places for small units

    def wheelEvent(self, event: QWheelEvent):
        """Handles mouse wheel events to increment/decrement the internal value by 0.1."""
        delta = event.angleDelta().y()
        if delta > 0:
            self.set_value(self.internal_value+1)
        elif delta < 0:
            self.set_value(self.internal_value-1)  # Update display
        event.accept()
        self.update_display()
