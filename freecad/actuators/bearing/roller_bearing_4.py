import math
import logging
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from scipy.optimize import fsolve
from PySide2.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QFormLayout, QDoubleSpinBox, QPushButton, QTextEdit,
                               QScrollArea)
from PySide2.QtCore import Qt
import sys
import numpy as np

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class BearingConfig:
    """Configuration parameters for bearing design, adjusted for smaller bearings"""
    min_rollers: int = 6  # Reduced to allow fewer rollers
    max_rollers: int = 20  # Reduced max to fit smaller geometry
    taper_angle_deg: float = 12.0
    load_distribution_factor: float = 0.9
    max_iterations: int = 20
    LOAD_FACTOR_AXIAL: float = 0.92
    TYPICAL_L_TO_D_RATIO: float = 1.5
    TYPICAL_DM_TO_D_RATIO: float = 4.0  # Reduced from 8.0 for smaller pitch diameter
    ROLLER_SPACING_FACTOR: float = 1.1  # Reduced from 1.3 for tighter roller spacing
    SCALING_FACTOR_INITIAL: float = 1.05
    SCALING_FACTOR_AGGRESSIVE: float = 1.1

    @property
    def taper_angle_rad(self) -> float:
        return math.radians(self.taper_angle_deg)


class TaperedRollerBearingDesign:
    def __init__(self, config: Optional[BearingConfig] = None):
        self.config = config or BearingConfig()

    def validate_float(self, value: str, positive: bool = True, range_limit: Optional[Tuple[float, float]] = None) -> \
    Tuple[bool, float, str]:
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

    def calculate_requirements(self, Fr: float, Fa: float, n: float, desired_life: float) -> Tuple[float, float]:
        """Calculate equivalent load and required dynamic capacity"""
        P = math.sqrt(Fr ** 2 + (self.config.LOAD_FACTOR_AXIAL * Fa) ** 2)
        L10 = (desired_life * n * 60) / 1e6
        C_req = P * (L10) ** (3 / 10)
        logger.info(f"Equivalent load: {P:.2f} N, Required capacity: {C_req:.2f} N")
        return P, C_req

    def stribeck_equation(self, z: int, D: float, L: float, dm: float) -> float:
        """Stribeck's equation for dynamic capacity"""
        return self.fmax * z * L * (D ** 1.8) * (dm ** 0.2)

    def hertz_contact_pressure(self, F: float, D: float, L: float, R: float) -> float:
        """Calculate maximum Hertzian contact pressure"""
        if any(val <= 0 for val in [F, D, L, R]) or any(math.isnan(val) for val in [F, D, L, R]):
            return float('inf')
        try:
            E_reduced = self.E / (1 - self.v ** 2)
            b_squared = (4 * F * R) / (math.pi * L * E_reduced)
            if b_squared <= 0:
                return float('inf')
            b = math.sqrt(b_squared)
            pressure = (2 * F) / (math.pi * b * L)
            if pressure < 0 or math.isnan(pressure) or math.isinf(pressure):
                return float('inf')
            return pressure
        except (ValueError, ZeroDivisionError, OverflowError):
            return float('inf')

    def setup_equations(self, C_req: float):
        """Set up the system of equations for the solver with debugging"""

        def equations(vars):
            D_mm, L_mm, dm_mm, z = vars  # Work in mm for numerical stability
            D, L, dm = D_mm / 1000, L_mm / 1000, dm_mm / 1000  # Convert to meters for calculations
            if (D_mm < -1e-3 or L_mm < -1e-3 or dm_mm < -1e-3 or z < -1 or
                    z < self.config.min_rollers or z > self.config.max_rollers):
                residuals = [abs(D_mm+1), abs(L_mm+1), abs(z), abs(z+1)]
                return residuals
            eq1 = (self.stribeck_equation(z, D, L, dm) / C_req) - 1  # Normalize Stribeck
            eq2 = L_mm - self.config.TYPICAL_L_TO_D_RATIO * D_mm
            eq3 = dm_mm - self.config.TYPICAL_DM_TO_D_RATIO * D_mm
            eq4 = z - (math.pi * dm_mm / (self.config.ROLLER_SPACING_FACTOR * D_mm))
            residuals = [eq1, eq2, eq3, eq4]
            #logger.debug(f"Residuals: eq1={eq1:.2e}, eq2={eq2:.2e}, eq3={eq3:.2e}, eq4={eq4:.2e}")
            return residuals

        return equations

    def solve_with_multiple_attempts(self, C_req: float) -> Tuple[float, float, float, int]:
        """Try multiple initial guesses to find a solution with debugging"""
        equations = self.setup_equations(C_req)
        scale = (C_req / 0.1) ** 0.5 if C_req > 0 else 1  # Scale guesses based on C_req
        initial_guesses = [
            (2.0 * scale, 3.0 * scale, 8.0 * scale, 8),  # Smaller bearing
            (1.0 * scale, 1.5 * scale, 4.0 * scale, 10),
            (3.0 * scale, 4.5 * scale, 12.0 * scale, 6),
            (1.5 * scale, 2.25 * scale, 6.0 * scale, 12),
            (0.5 * scale, 0.75 * scale, 2.0 * scale, 15)
        ]
        for i, guess in enumerate(initial_guesses):
            try:
                logger.info(
                    f"Attempting solution with guess {i + 1}: D={guess[0]:.1f}mm, L={guess[1]:.1f}mm, dm={guess[2]:.1f}mm, z={guess[3]}")
                solution, infodict, ier, mesg = fsolve(equations, guess, full_output=True, xtol=1e-8, maxfev=1000,
                                                       factor=0.1)
                logger.debug(f"fsolve output: ier={ier}, message={mesg}")
                logger.debug(f"Final residuals: {infodict['fvec']}")
                if ier == 1:
                    D_mm, L_mm, dm_mm, z = solution
                    D, L, dm = D_mm / 1000, L_mm / 1000, dm_mm / 1000
                    if self.validate_solution(D, L, dm, z):
                        logger.info(
                            f"Solution found with guess {i + 1}: D={D_mm:.3f}mm, L={L_mm:.3f}mm, dm={dm_mm:.3f}mm, z={z:.1f}")
                        return D, L, dm, max(min(round(z), self.config.max_rollers), self.config.min_rollers)
                    else:
                        logger.warning(f"Solution invalid: D={D_mm:.3f}mm, L={L_mm:.3f}mm, dm={dm_mm:.3f}mm, z={z:.1f}")
                else:
                    logger.warning(f"Guess {i + 1} failed to converge: {mesg}")
            except Exception as e:
                logger.warning(f"Guess {i + 1} raised exception: {str(e)}")
                continue
        raise RuntimeError("Could not find valid solution with any initial guess")

    def validate_solution(self, D: float, L: float, dm: float, z: float) -> bool:
        """Validate that the solution is physically meaningful"""
        valid = (D > 0 and L > 0 and dm > 0 and
                 z >= self.config.min_rollers and
                 not any(math.isnan(val) for val in [D, L, dm, z]))
        logger.debug(
            f"Solution validation: D={D * 1000:.3f}mm, L={L * 1000:.3f}mm, dm={dm * 1000:.3f}mm, z={z:.1f}, valid={valid}")
        return valid

    def refine_for_contact_pressure(self, D: float, L: float, dm: float, z: int, P: float) -> Tuple[
        float, float, float, int]:
        """Iteratively refine dimensions to meet contact pressure requirements"""
        F_roller = P / (self.config.load_distribution_factor * z)
        R = D / 2
        contact_pressure = self.hertz_contact_pressure(F_roller, D, L, R)
        iteration = 0
        scaling_factor = self.config.SCALING_FACTOR_INITIAL
        while (contact_pressure > self.contact_pressure_limit and
               iteration < self.config.max_iterations):
            logger.info(f"Iteration {iteration + 1}: Contact pressure {contact_pressure / 1e6:.1f} MPa > limit")
            D *= scaling_factor
            L = self.config.TYPICAL_L_TO_D_RATIO * D
            dm = self.config.TYPICAL_DM_TO_D_RATIO * D
            z = max(min(round(math.pi * dm / (self.config.ROLLER_SPACING_FACTOR * D)),
                        self.config.max_rollers), self.config.min_rollers)
            F_roller = P / (self.config.load_distribution_factor * z)
            R = D / 2
            contact_pressure = self.hertz_contact_pressure(F_roller, D, L, R)
            iteration += 1
            if iteration > self.config.max_iterations // 2:
                scaling_factor = self.config.SCALING_FACTOR_AGGRESSIVE
        if contact_pressure > self.contact_pressure_limit:
            logger.warning("Could not satisfy contact pressure requirement within iteration limit")
        return D, L, dm, z

    def validate_design(self, results: Dict) -> List[str]:
        """Check if design is manufacturable and reasonable"""
        warnings = []
        if results['roller_diameter'] < 1:  # Adjusted for smaller bearings
            warnings.append("Roller diameter may be too small for practical manufacturing")
        if results['roller_diameter'] > 30:  # Adjusted for your requirement
            warnings.append("Roller diameter exceeds 30 mm - verify manufacturing feasibility")
        if results['number_of_rollers'] < 6:
            warnings.append("Low number of rollers may cause high individual loads")
        if results['bearing_pitch_diameter'] > 30:  # Adjusted for your requirement
            warnings.append("Bearing pitch diameter exceeds 30 mm - consider application constraints")
        aspect_ratio = results['roller_length'] / results['roller_diameter']
        if aspect_ratio < 1.2 or aspect_ratio > 2.0:
            warnings.append(f"Unusual roller aspect ratio: {aspect_ratio:.2f}")
        return warnings

    def solve_geometry(self, E: float, v: float, Fr: float, Fa: float, n: float,
                       fmax: float, desired_life: float, contact_pressure_limit: float) -> Dict:
        """Main geometry solving method"""
        try:
            self.E = E * 1e9
            self.v = v
            self.Fr = Fr
            self.Fa = Fa
            self.n = n
            self.fmax = fmax
            self.desired_life = desired_life
            self.contact_pressure_limit = contact_pressure_limit * 1e6
            P, C_req = self.calculate_requirements(Fr, Fa, n, desired_life)
            logger.debug(f"Calculated P={P:.2f} N, C_req={C_req:.2f} N")
            D, L, dm, z = self.solve_with_multiple_attempts(C_req)
            d = dm - D * math.cos(self.config.taper_angle_rad)
            D_outer = dm + D * math.cos(self.config.taper_angle_rad)
            D, L, dm, z = self.refine_for_contact_pressure(D, L, dm, z, P)
            d = dm - D * math.cos(self.config.taper_angle_rad)
            D_outer = dm + D * math.cos(self.config.taper_angle_rad)
            F_roller = P / (self.config.load_distribution_factor * z)
            R = D / 2
            contact_pressure = self.hertz_contact_pressure(F_roller, D, L, R)
            results = {
                'roller_diameter': D * 1000,
                'roller_length': L * 1000,
                'inner_raceway_diameter': d * 1000,
                'outer_raceway_diameter': D_outer * 1000,
                'bearing_pitch_diameter': dm * 1000,
                'number_of_rollers': int(z),
                'actual_contact_pressure': contact_pressure / 1e6,
                'dynamic_capacity': self.stribeck_equation(z, D, L, dm),
                'required_capacity': C_req,
                'pressure_limit': contact_pressure_limit,
                'equivalent_load': P
            }
            logger.info("Geometry calculation completed successfully")
            return results
        except Exception as e:
            logger.error(f"Error in geometry calculation: {str(e)}")
            return {
                'error': str(e),
                'roller_diameter': 0,
                'roller_length': 0,
                'inner_raceway_diameter': 0,
                'outer_raceway_diameter': 0,
                'bearing_pitch_diameter': 0,
                'number_of_rollers': 0,
                'actual_contact_pressure': 0,
                'dynamic_capacity': 0,
                'required_capacity': 0,
                'pressure_limit': contact_pressure_limit
            }

    def format_results(self, results: Dict) -> str:
        """Format results for GUI display"""
        if 'error' in results:
            return f"\n❌ Error in calculation: {results['error']}"
        output = []
        output.append("=" * 50)
        output.append("         CALCULATED BEARING GEOMETRY")
        output.append("=" * 50)
        output.append(f"Roller diameter:          {results['roller_diameter']:8.2f} mm")
        output.append(f"Roller length:            {results['roller_length']:8.2f} mm")
        output.append(f"Inner raceway diameter:   {results['inner_raceway_diameter']:8.2f} mm")
        output.append(f"Outer raceway diameter:   {results['outer_raceway_diameter']:8.2f} mm")
        output.append(f"Bearing pitch diameter:   {results['bearing_pitch_diameter']:8.2f} mm")
        output.append(f"Number of rollers:        {results['number_of_rollers']:8d}")
        output.append("\n" + "=" * 50)
        output.append("           VERIFICATION RESULTS")
        output.append("=" * 50)
        output.append(f"Equivalent load:          {results['equivalent_load']:8.2f} N")
        output.append(f"Required dynamic capacity:{results['required_capacity']:8.2f} N")
        output.append(f"Calculated capacity:      {results['dynamic_capacity']:8.2f} N")
        output.append(f"Contact pressure:         {results['actual_contact_pressure']:8.2f} MPa")
        output.append(f"Pressure limit:           {results['pressure_limit']:8.2f} MPa")
        output.append("\n" + "=" * 50)
        output.append("              DESIGN STATUS")
        output.append("=" * 50)
        capacity_ok = results['dynamic_capacity'] >= results['required_capacity']
        pressure_ok = results['actual_contact_pressure'] <= results['pressure_limit']
        output.append(f"Dynamic capacity:    {'✅ PASS' if capacity_ok else '❌ FAIL'}")
        output.append(f"Contact pressure:    {'✅ PASS' if pressure_ok else '❌ FAIL'}")
        warnings = self.validate_design(results)
        if warnings:
            output.append("\n⚠️  Design Warnings:")
            for warning in warnings:
                output.append(f"   • {warning}")
        if capacity_ok and pressure_ok and not warnings:
            output.append(f"\n🎉 Design is acceptable for the given requirements!")
        elif capacity_ok and pressure_ok:
            output.append(f"\n✅ Design meets requirements but has minor concerns.")
        else:
            output.append(f"\n⚠️  Design needs further refinement.")
        return "\n".join(output)


class BearingCalculatorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tapered Roller Bearing Calculator")
        self.designer = TaperedRollerBearingDesign()
        self.init_ui()

    def init_ui(self):
        """Initialize the GUI components"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Input form
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)

        # Material Properties
        self.E_input = QDoubleSpinBox()
        self.E_input.setRange(0.1, 1000)
        self.E_input.setValue(70)  # Aluminum Young's modulus
        self.E_input.setSuffix(" GPa")
        form_layout.addRow("Young's modulus:", self.E_input)

        self.v_input = QDoubleSpinBox()
        self.v_input.setRange(0.01, 0.49)
        self.v_input.setValue(0.33)  # Aluminum Poisson's ratio
        self.v_input.setSingleStep(0.01)
        form_layout.addRow("Poisson's ratio:", self.v_input)

        # Loading Conditions
        self.Fr_input = QDoubleSpinBox()
        self.Fr_input.setRange(0.01, 1e6)
        self.Fr_input.setValue(0.1)  # Low load
        self.Fr_input.setSuffix(" N")
        form_layout.addRow("Radial load:", self.Fr_input)

        self.Fa_input = QDoubleSpinBox()
        self.Fa_input.setRange(0.01, 1e6)
        self.Fa_input.setValue(0.1)  # Low load
        self.Fa_input.setSuffix(" N")
        form_layout.addRow("Axial load:", self.Fa_input)

        self.n_input = QDoubleSpinBox()
        self.n_input.setRange(0.1, 1e5)
        self.n_input.setValue(1000)
        self.n_input.setSuffix(" rpm")
        form_layout.addRow("Rotational speed:", self.n_input)

        # Design Parameters
        self.fmax_input = QDoubleSpinBox()
        self.fmax_input.setRange(0.1, 1000)
        self.fmax_input.setValue(100)  # Increased for small bearings
        form_layout.addRow("fmax (Stribeck):", self.fmax_input)

        self.desired_life_input = QDoubleSpinBox()
        self.desired_life_input.setRange(0.1, 1e6)
        self.desired_life_input.setValue(1)  # Short lifespan
        self.desired_life_input.setSuffix(" hours")
        form_layout.addRow("Desired life:", self.desired_life_input)

        self.contact_pressure_input = QDoubleSpinBox()
        self.contact_pressure_input.setRange(0.1, 10000)
        self.contact_pressure_input.setValue(500)  # Lower for aluminum
        self.contact_pressure_input.setSuffix(" MPa")
        form_layout.addRow("Max contact pressure:", self.contact_pressure_input)

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

    def calculate(self):
        """Handle calculation and display results"""
        valid, E, error = self.designer.validate_float(str(self.E_input.value()), positive=True)
        if not valid:
            self.results_display.setText(f"Error in Young's modulus: {error}")
            return
        valid, v, error = self.designer.validate_float(str(self.v_input.value()), positive=True, range_limit=(0, 0.5))
        if not valid:
            self.results_display.setText(f"Error in Poisson's ratio: {error}")
            return
        valid, Fr, error = self.designer.validate_float(str(self.Fr_input.value()), positive=True)
        if not valid:
            self.results_display.setText(f"Error in radial load: {error}")
            return
        valid, Fa, error = self.designer.validate_float(str(self.Fa_input.value()), positive=True)
        if not valid:
            self.results_display.setText(f"Error in axial load: {error}")
            return
        valid, n, error = self.designer.validate_float(str(self.n_input.value()), positive=True)
        if not valid:
            self.results_display.setText(f"Error in rotational speed: {error}")
            return
        valid, fmax, error = self.designer.validate_float(str(self.fmax_input.value()), positive=True)
        if not valid:
            self.results_display.setText(f"Error in fmax: {error}")
            return
        valid, desired_life, error = self.designer.validate_float(str(self.desired_life_input.value()), positive=True)
        if not valid:
            self.results_display.setText(f"Error in desired life: {error}")
            return
        valid, contact_pressure_limit, error = self.designer.validate_float(str(self.contact_pressure_input.value()),
                                                                            positive=True)
        if not valid:
            self.results_display.setText(f"Error in contact pressure limit: {error}")
            return

        results = self.designer.solve_geometry(
            E, v, Fr, Fa, n, fmax, desired_life, contact_pressure_limit
        )
        self.results_display.setText(self.designer.format_results(results))


def main():
    app = QApplication(sys.argv)
    window = BearingCalculatorGUI()
    window.resize(600, 800)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()