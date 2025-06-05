import math
import numpy as np
try:
    from PySide2.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                                  QFormLayout, QDoubleSpinBox, QPushButton, QTextEdit,
                                  QScrollArea)
    from PySide2.QtCore import Qt
except ImportError:
    from PySide.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                                   QFormLayout, QDoubleSpinBox, QPushButton, QTextEdit,
                                   QScrollArea)
    from PySide.QtCore import Qt
import pyqtgraph as pg
import sys
import logging
from typing import Optional, Tuple, Dict

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class CycloidalDriveCalculator:
    def __init__(self):
        self.min_roller_count = 4  # Minimum rollers (lobe >= 3)

    def validate_float(self, value: str, positive: bool = True, range_limit: Optional[Tuple[float, float]] = None) -> Tuple[bool, float, str]:
        """Validate a float input from string"""
        try:
            val = float(value)
            if positive and val <= 0:
                return False, 0, "Value must be positive."
            if range_limit and not (range_limit[0] < val < range_limit[1]):
                return False, 0, f"Value must be between {range_limit[0]} and {range_limit[1]}."
            return True, val, ""
        except ValueError:
            return False, 0, "Invalid number."

    def roller_to_ratio(self, r1: int, r2: int) -> float:
        """Calculate reduction ratio from roller counts"""
        if r1 == r2:
            return r2 - 1
        return ((r1 - 1) * r2) / (r1 - r2)

    def roller_to_factor(self, r1: int, r2: int) -> Tuple[float, float]:
        """Calculate torque factors u1 and u2"""
        if r1 == r2:
            return (r2 - 1, 1)
        l1 = r1 - 1
        u1 = -(l1 / (r1 - l1))
        l2 = r2 - 1
        u2 = -(r1 / (r2 - l2))
        return (u1, u2)

    def torque(self, r1: int, r2: int, tem_Nm: float) -> Tuple[float, float, float, float, float, float]:
        """Calculate torque for first and second stages"""
        u1, u2 = self.roller_to_factor(r1, r2)
        u1_ = 1 / (1 + u1)
        u1_dot = u1 * u1_
        udot = u1 * u2

        first_drive = tem_Nm * u1_
        first_ring = tem_Nm * (1 + udot)
        first_disc = tem_Nm * (u1_dot + udot)

        second_drive = tem_Nm * u1_dot
        second_ring = tem_Nm * udot
        second_disc = first_disc
        return (first_drive, first_ring, first_disc, second_drive, second_ring, second_disc)

    def disc_equation(self, N: int, R_mm: float, E_mm: float, Rr_mm: float) -> Tuple[str, str]:
        """Generate parametric equations for cycloidal disc"""
        R_EN = R_mm / (E_mm * N)
        _N = 1 - N
        X = f"({R_mm}*cos(t)) - ({Rr_mm}*cos(t+arctan(sin({_N}*t)/({R_EN} - cos({_N}*t)))) - ({E_mm}*cos({N}*t))"
        Y = f"(-{R_mm}*sin(t)) + ({Rr_mm}*sin(t+arctan(sin({_N}*t)/({R_EN} - cos({_N}*t)))) + ({E_mm}*sin({N}*t))"
        return X, Y

    def evaluate_disc_equation(self, N: int, R_mm: float, E_mm: float, Rr_mm: float, t: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Evaluate parametric equations for plotting"""
        R_EN = R_mm / (E_mm * N)
        _N = 1 - N
        try:
            term1_x = R_mm * np.cos(t)
            term2_x = Rr_mm * np.cos(t + np.arctan(np.sin(_N * t) / (R_EN - np.cos(_N * t))))
            term3_x = E_mm * np.cos(N * t)
            X = term1_x - term2_x - term3_x

            term1_y = -R_mm * np.sin(t)
            term2_y = Rr_mm * np.sin(t + np.arctan(np.sin(_N * t) / (R_EN - np.cos(_N * t))))
            term3_y = E_mm * np.sin(N * t)
            Y = term1_y + term2_y + term3_y

            return X, Y
        except Exception as e:
            logger.error(f"Error evaluating disc equation for N={N}: {str(e)}")
            return np.array([]), np.array([])

    def search(self, input_rotation: float, output_rotation: float, ratio_tolerance: float,
               ring_diameter_mm: float, eccentricity_mm: float, smallest_roller_diameter_mm: float,
               tem_Nm: float) -> Dict:
        """Search for roller counts that satisfy the reduction ratio and calculate torque"""
        try:
            target_ratio = input_rotation / output_rotation
            min_ratio = max(0.0, target_ratio - ratio_tolerance)
            max_ratio = target_ratio + ratio_tolerance
            max_n_roller = math.floor((ring_diameter_mm / 2) / eccentricity_mm)

            output = []
            output.append(f"Looking for R1 and R2 to achieve reduction ratio in range [{min_ratio:.2f}, {max_ratio:.2f}]")
            output.append(f"Maximum number of rollers from parameters: {max_n_roller}")
            output.append(f"Search space: {math.floor(max_n_roller * max_n_roller / 2)} combinations")

            for r1 in range(self.min_roller_count, max_n_roller + 1):
                for r2 in range(r1, max_n_roller + 1):
                    ratio = self.roller_to_ratio(r1, r2)
                    if min_ratio <= abs(ratio) <= max_ratio:
                        output.append(f"\n✅ Solution found: r1={r1}, r2={r2}, ratio={ratio:.2f}")
                        x1, y1 = self.disc_equation(r1, ring_diameter_mm / 2, eccentricity_mm, smallest_roller_diameter_mm)
                        x2, y2 = self.disc_equation(r2, ring_diameter_mm / 2, eccentricity_mm, smallest_roller_diameter_mm)
                        output.append(f"Disc equations for r1={r1}:")
                        output.append(f"X = {x1}")
                        output.append(f"Y = {y1}")
                        output.append(f"Disc equations for r2={r2}:")
                        output.append(f"X = {x2}")
                        output.append(f"Y = {y2}")

                        # Calculate torque
                        torque_vals = self.torque(r1, r2, tem_Nm)
                        output.append(f"\nTorque Results (Input Motor Torque = {tem_Nm:.2f} Nm):")
                        output.append(f"First Drive: {torque_vals[0]:.2f} Nm")
                        output.append(f"First Ring:  {torque_vals[1]:.2f} Nm")
                        output.append(f"First Disc:  {torque_vals[2]:.2f} Nm")
                        output.append(f"Second Drive: {torque_vals[3]:.2f} Nm")
                        output.append(f"Second Ring:  {torque_vals[4]:.2f} Nm")
                        output.append(f"Second Disc:  {torque_vals[5]:.2f} Nm")

                        return {
                            'output': "\n".join(output),
                            'r1': r1,
                            'r2': r2,
                            'ratio': ratio,
                            'success': True,
                            'plot_data': [
                                (r1, self.evaluate_disc_equation(r1, ring_diameter_mm / 2, eccentricity_mm, smallest_roller_diameter_mm, np.linspace(0, 2 * np.pi, 1000))),
                                (r2, self.evaluate_disc_equation(r2, ring_diameter_mm / 2, eccentricity_mm, smallest_roller_diameter_mm, np.linspace(0, 2 * np.pi, 1000)))
                            ]
                        }
            output.append("\n❌ No solution found within the given constraints.")
            return {'output': "\n".join(output), 'r1': 0, 'r2': 0, 'ratio': 0, 'success': False, 'plot_data': []}
        except Exception as e:
            logger.error(f"Error in search: {str(e)}")
            return {'output': f"Error: {str(e)}", 'r1': 0, 'r2': 0, 'ratio': 0, 'success': False, 'plot_data': []}

class CycloidalGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cycloidal Drive Calculator")
        self.calculator = CycloidalDriveCalculator()
        self.init_ui()

    def init_ui(self):
        """Initialize the GUI components"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Input form
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)

        # Input parameters
        self.input_rotation = QDoubleSpinBox()
        self.input_rotation.setRange(1, 1e6)
        self.input_rotation.setValue(2500 * 24)
        self.input_rotation.setSuffix(" rpm")
        form_layout.addRow("Input rotation:", self.input_rotation)

        self.output_rotation = QDoubleSpinBox()
        self.output_rotation.setRange(1, 1e6)
        self.output_rotation.setValue(60)
        self.output_rotation.setSuffix(" rpm")
        form_layout.addRow("Output rotation:", self.output_rotation)

        self.ratio_tolerance = QDoubleSpinBox()
        self.ratio_tolerance.setRange(0.1, 100)
        self.ratio_tolerance.setValue(5.0)
        form_layout.addRow("Ratio tolerance:", self.ratio_tolerance)

        self.ring_diameter = QDoubleSpinBox()
        self.ring_diameter.setRange(1, 1000)
        self.ring_diameter.setValue(200)
        self.ring_diameter.setSuffix(" mm")
        form_layout.addRow("Ring diameter:", self.ring_diameter)

        self.eccentricity = QDoubleSpinBox()
        self.eccentricity.setRange(0.1, 100)
        self.eccentricity.setValue(1)
        self.eccentricity.setSuffix(" mm")
        form_layout.addRow("Eccentricity:", self.eccentricity)

        self.roller_diameter = QDoubleSpinBox()
        self.roller_diameter.setRange(0.1, 100)
        self.roller_diameter.setValue(5)
        self.roller_diameter.setSuffix(" mm")
        form_layout.addRow("Smallest roller diameter:", self.roller_diameter)

        self.torque_input = QDoubleSpinBox()
        self.torque_input.setRange(0.01, 1000)
        self.torque_input.setValue(1.0)
        self.torque_input.setSuffix(" Nm")
        form_layout.addRow("Motor torque:", self.torque_input)

        # Scrollable form
        scroll_area = QScrollArea()
        scroll_area.setWidget(form_widget)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        # Calculate button
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate)
        main_layout.addWidget(self.calculate_button)

        # Results display
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        main_layout.addWidget(self.results_display)

        # Plot widget
        self.plot_widget = pg.PlotWidget(title="Cycloidal Disc Profiles")
        self.plot_widget.setBackground('w')
        self.plot_widget.showGrid(x=True, y=True)
        self.plot_widget.setLabel('left', 'Y (mm)')
        self.plot_widget.setLabel('bottom', 'X (mm)')
        main_layout.addWidget(self.plot_widget)

    def calculate(self):
        """Handle calculation and display results"""
        # Validate inputs
        valid, input_rotation, error = self.calculator.validate_float(str(self.input_rotation.value()), positive=True)
        if not valid:
            self.results_display.setText(f"Error in input rotation: {error}")
            return
        valid, output_rotation, error = self.calculator.validate_float(str(self.output_rotation.value()), positive=True)
        if not valid:
            self.results_display.setText(f"Error in output rotation: {error}")
            return
        valid, ratio_tolerance, error = self.calculator.validate_float(str(self.ratio_tolerance.value()), positive=True)
        if not valid:
            self.results_display.setText(f"Error in ratio tolerance: {error}")
            return
        valid, ring_diameter, error = self.calculator.validate_float(str(self.ring_diameter.value()), positive=True)
        if not valid:
            self.results_display.setText(f"Error in ring diameter: {error}")
            return
        valid, eccentricity, error = self.calculator.validate_float(str(self.eccentricity.value()), positive=True)
        if not valid:
            self.results_display.setText(f"Error in eccentricity: {error}")
            return
        valid, roller_diameter, error = self.calculator.validate_float(str(self.roller_diameter.value()), positive=True)
        if not valid:
            self.results_display.setText(f"Error in roller diameter: {error}")
            return
        valid, tem_Nm, error = self.calculator.validate_float(str(self.torque_input.value()), positive=True)
        if not valid:
            self.results_display.setText(f"Error in motor torque: {error}")
            return

        # Clear previous plot
        self.plot_widget.clear()

        # Perform calculation
        result = self.calculator.search(
            input_rotation, output_rotation, ratio_tolerance,
            ring_diameter, eccentricity, roller_diameter, tem_Nm
        )

        # Display text results
        self.results_display.setText(result['output'])

        # Plot cycloidal curves if solution found
        if result['success']:
            for r, (x_data, y_data) in result['plot_data']:
                if len(x_data) > 0 and len(y_data) > 0:
                    pen = pg.mkPen(color=('r' if r == result['r1'] else 'b'), width=2)
                    self.plot_widget.plot(x_data, y_data, pen=pen, name=f"Disc (r={r})")
            self.plot_widget.addLegend()

def main():
    app = QApplication(sys.argv)
    window = CycloidalGUI()
    window.resize(800, 1000)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()