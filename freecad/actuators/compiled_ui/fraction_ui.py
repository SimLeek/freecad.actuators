import re
import traceback
from fractions import Fraction
from PySide2.QtWidgets import QLineEdit
import ast
import math

class FractionTransformer(ast.NodeTransformer):
    def visit_Num(self, node):
        # Convert all numbers to Fraction
        return ast.copy_location(ast.Call(
            func=ast.Name(id='Fraction', ctx=ast.Load()),
            args=[ast.Str(s=str(node.n))],  # Pass as string to avoid float imprecision
            keywords=[]
        ), node)

    def visit_Constant(self, node):
        # Handle Python 3.8+ where numbers are under ast.Constant
        if isinstance(node.value, (int, float)):
            return ast.copy_location(ast.Call(
                func=ast.Name(id='Fraction', ctx=ast.Load()),
                args=[ast.Str(s=str(node.value))],
                keywords=[]
            ), node)
        return node

def safe_eval(text):
    tree = ast.parse(text, mode='eval')
    transformed_tree = FractionTransformer().visit(tree)
    ast.fix_missing_locations(transformed_tree)

    return eval(
        compile(transformed_tree, "<string>", mode="eval"),
        {"__builtins__": math.__dict__},  # Inject local math functions safely
        {"Fraction": Fraction}
    )


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
            return safe_eval(text)  # Safe eval with Fraction
        except Exception:
            return traceback.format_exc()  # Return full error traceback as a string

    def update_internal_value(self):
        """Updates the stored Fraction value based on user input."""
        result = self.parse_fraction(self.text())

        if isinstance(result, Fraction):
            self.internal_value = result
            self.setToolTip(f"{result.numerator}:{result.denominator}")
        else:
            try:
                self.internal_value = Fraction(result)
                self.setToolTip(f"{self.internal_value.numerator}:{self.internal_value.denominator}")
            except (ValueError, TypeError):
                self.internal_value = Fraction(0)


    def get_value(self):
        """Returns the stored Fraction value."""
        return self.internal_value

    def set_value(self, fraction):
        """Sets the displayed value while keeping the internal Fraction representation."""
        if isinstance(fraction, Fraction):
            self.internal_value = fraction
            self.blockSignals(True)  # Prevent triggering update_internal_value
            self.setText(f"{fraction.numerator}:{fraction.denominator}")
            self.setToolTip(f"{fraction.numerator}:{fraction.denominator}")
            self.blockSignals(False)
