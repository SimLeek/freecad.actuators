import sys
from fractions import Fraction
try:
    from PySide2.QtWidgets import QSlider, QApplication, QVBoxLayout, QWidget, QLabel
    from PySide2.QtCore import Qt, Signal, Property
except ImportError:
    from PySide.QtWidgets import QSlider, QApplication, QVBoxLayout, QWidget, QLabel
    from PySide.QtCore import Qt, Signal, Property

class FractionalSlider(QSlider):
    # A new signal that emits the fractional value whenever it changes.
    fractionalValueChanged = Signal(object)  # object will be a Fraction

    def __init__(self, orientation=Qt.Horizontal, parent=None,
                 fractionalMinimum=Fraction(0, 1),
                 fractionalMaximum=Fraction(1, 1),
                 fractionalSingleStep=Fraction(1, 10)):
        super().__init__(orientation, parent)
        # Store the Fraction values.
        self._fractionalMinimum = Fraction(fractionalMinimum)
        self._fractionalMaximum = Fraction(fractionalMaximum)

        self._half = Fraction(1,2)

        # allow full single step
        self._fractionalSingleStep = Fraction(fractionalSingleStep)
        self._update_range()
        self.setSingleStep(1)  # one step corresponds to fractionalSingleStep.
        # Initialize the slider value at minimum.
        self.setValue(int(self._fractionalMinimum * self._multiplier))

        # Connect the built-in valueChanged to our handler.
        self.valueChanged.connect(self._on_value_changed)

    def _on_value_changed(self, int_val):
        # Convert the integer value back to a Fraction.
        frac_val = Fraction(int_val, self._multiplier)
        self.fractionalValueChanged.emit(frac_val)

    def getFractionalValue(self):
        self._on_value_changed(self.value())  # if other value change events are triggering this, force us to be first
        return Fraction(self.value()) / self._multiplier

    def setFractionalValue(self, frac_val):
        # Expect frac_val is a Fraction and within the allowed range.
        int_val = int(frac_val * self._multiplier)
        self.setValue(int_val)

    def getFractionalMinimum(self):
        return self._fractionalMinimum

    def _update_range(self):
        self._multiplier = ((self._fractionalMaximum - self._fractionalMinimum) / self._fractionalSingleStep)
        if self._multiplier == 0:
            self._multiplier = Fraction(1,1)
        self.setMinimum(int(self._fractionalMinimum * self._multiplier))
        self.setMaximum(int(self._fractionalMaximum * self._multiplier + self._half))

    def setFractionalMinimum(self, frac_min):
        self._fractionalMinimum = Fraction(frac_min)
        self._update_range()

    def getFractionalMaximum(self):
        return self._fractionalMaximum

    def setFractionalMaximum(self, frac_max):
        self._fractionalMaximum = Fraction(frac_max)
        self._update_range()

    def getFractionalSingleStep(self):
        return self._fractionalSingleStep

    def setFractionalSingleStep(self, frac_step):
        self._fractionalSingleStep = Fraction(frac_step)
        if self._fractionalSingleStep==0:
            self._fractionalSingleStep = Fraction(1, 1)
        self._update_range()
        # Optionally update current value to match new scaling.
        self.setValue(int(self.getFractionalValue() * self._multiplier))

    # Expose these properties so they can be used from Designer or elsewhere.
    fractionalValue = Property(object, getFractionalValue, setFractionalValue)
    fractionalMinimum = Property(object, getFractionalMinimum, setFractionalMinimum)
    fractionalMaximum = Property(object, getFractionalMaximum, setFractionalMaximum)
    fractionalSingleStep = Property(object, getFractionalSingleStep, setFractionalSingleStep)


# Example usage in a simple GUI application.
def main():
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout(window)

    label = QLabel("Fractional Value:")
    layout.addWidget(label)

    # Create a FractionalSlider ranging from 0 to 1 with a step of 1/10.
    fs = FractionalSlider(Qt.Horizontal,
                          fractionalMinimum=Fraction(0, 1),
                          fractionalMaximum=Fraction(1, 1),
                          fractionalSingleStep=Fraction(1, 10))
    layout.addWidget(fs)

    # Update the label whenever the fractional value changes.
    def update_label(val):
        label.setText(f"Fractional Value: {val}")
    fs.fractionalValueChanged.connect(update_label)

    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
