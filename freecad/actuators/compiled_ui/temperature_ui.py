import re
import math
import traceback
try:
    from PySide2.QtWidgets import QLineEdit
    from PySide2.QtGui import QWheelEvent
    from PySide2.QtCore import Qt
except ImportError:
    from PySide.QtWidgets import QLineEdit
    from PySide.QtGui import QWheelEvent
    from PySide.QtCore import Qt

# Temperature conversion functions (to Kelvin)
def celsius(x):
    return x + 273.15

def fahrenheit(x):
    return (float(x) - 32) * 5 / 9 + 273.15

# Reverse conversion functions (from Kelvin)
def kelvin_to_celsius(k):
    return k - 273.15

def kelvin_to_fahrenheit(k):
    return (k - 273.15) * 9 / 5 + 32

# Regex patterns
integer = r'(?:0[bB](?:[01_])+|0[oO](?:[0-7_])+|0[xX](?:[0-9a-fA-F_])+|[1-9](?:_?\d)*|0(?:_?0)*)(?!.)'
float_num = r'(?:(?:\d(?:_?\d)*)\.?(?:\d(?:_?\d)*)?)(?:[eE][+-]?\d(?:_?\d)*)?'
numeric = r'(?:' + integer + r'|' + float_num + r')'
number_unit = r'(' + numeric + r')([cfk])(?![a-zA-Z0-9])'

def replace_unit(match):
    number = match.group(1)
    unit = match.group(2)
    if unit == 'c':
        return f"celsius({number})"
    elif unit == 'f':
        return f"fahrenheit({number})"
    elif unit == 'k':
        return f"{number}"

def safe_eval(text):
    try:
        matches = list(re.finditer(number_unit, text))
        current_unit = matches[-1].group(2) if matches else None
        text = re.sub(number_unit, replace_unit, text)
        print(text)
        value = eval(text, {"__builtins__": math.__dict__}, {"celsius": celsius, "fahrenheit": fahrenheit, "kelvin": kelvin})
        return value, current_unit
    except Exception:
        return traceback.format_exc(), None

class QTemperatureEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.internal_k = 0.0  # Store value in Kelvin
        self.display_unit = "C"  # Default display unit
        self._current_unit = None  # Last parsed unit
        self.textChanged.connect(self.update_internal_value)
        self.setFocusPolicy(Qt.WheelFocus)  # Enable wheel events

    def parse_temperature(self, text):
        text = text.lower().replace(" ", "")  # Normalize input
        value, unit = safe_eval(text)
        if isinstance(value, str):
            return value
        self._current_unit = unit
        return value

    def update_internal_value(self):
        text = self.text().strip()
        value = self.parse_temperature(text)
        if isinstance(value, str):
            self.setToolTip(value)
            self.setStyleSheet("border: 1px solid red;")
        else:
            self.internal_k = value
            print(self.internal_k)
            self.setToolTip(f"{self.internal_k:.4f}K")
            self.setStyleSheet("")

    def get_k_value(self):
        return self.internal_k

    def set_k_value(self, k_value):
        self.internal_k = k_value
        self.blockSignals(True)
        self.update_display()
        self.blockSignals(False)

    def set_display_unit(self, unit):
        if unit.lower() in ['c', 'f', 'k']:
            self.display_unit = unit
            self.update_display()

    def update_display(self):
        if self.display_unit.lower() == "c":
            converted_value = kelvin_to_celsius(self.internal_k)
        elif self.display_unit.lower() == "f":
            converted_value = kelvin_to_fahrenheit(self.internal_k)
        else:  # Kelvin
            converted_value = self.internal_k
        self.setText(f"{converted_value:.2f}{self.display_unit}")
        self.setToolTip(f"{converted_value:.2f}{self.display_unit}")

    def wheelEvent(self, event: QWheelEvent):
        unit = self._current_unit if self._current_unit else self.display_unit.lower()
        multiplier = 5 / 9 if unit == 'f' else 1.0
        delta = event.angleDelta().y()
        if delta > 0:
            self.internal_k += 1.0 * multiplier
        elif delta < 0:
            self.internal_k -= 1.0 * multiplier
        self.blockSignals(True)
        self.update_display()
        self.blockSignals(False)
        event.accept()

if __name__ == "__main__":
    from PySide2.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    widget = QTemperatureEdit()
    widget.show()
    sys.exit(app.exec_())