from PySide2.QtWidgets import QDialog, QApplication, QComboBox
from PySide2.QtGui import QColor
import sys
from fractions import Fraction
import math

# AWG table for copper (current in A, approximate safe values for insulated wire)
AWG_TABLE = [
    (30, 0.5), (28, 0.8), (26, 1.3), (24, 2.1), (22, 3.3),
    (20, 5.2), (18, 8.3), (16, 13.0), (14, 21.0), (12, 33.0),
    (10, 52.0), (8, 83.0), (6, 133.0)
]

class BLDCDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Assuming Ui_BLDCDialog is defined in a UI file
        # Assumption: Ui_BLDCDialog has all UI elements (line edits, spinbox, lock buttons, combobox)
        self.ui = Ui_BLDCDialog()
        self.ui.setupUi(self)

        # Prevent recursive updates
        self.computing = False

        # Set permanent read-only states
        self.ui.back_emf_constant_lineedit.setReadOnly(True)
        self.ui.current_lineedit.setReadOnly(True)
        self.ui.phase_resistance_lineedit.setReadOnly(True)
        self.ui.wire_awg_lineedit.setReadOnly(True)

        self.ui.magnet_count_lineedit.setReadOnly(True)
        self.ui.magnet_width_lineedit.setReadOnly(True)
        self.ui.magnet_thickness_lineedit.setReadOnly(True)
        self.ui.magnet_length_lineedit.setReadOnly(True)

        self.ui.slot_pole_ratio_lineedit.setReadOnly(True)
        self.ui.winding_factor_lineedit.setReadOnly(True)

        # Initialize wire material combobox
        self.ui.wire_material_combobox.addItems(['Copper', 'Copper-Clad Aluminum'])

        # Initialize num_phases_spinbox
        self.ui.num_phases_spinbox.setMinimum(3)
        self.ui.num_phases_spinbox.setValue(3)

        # Connect UI signals
        self.ui.wire_material_combobox.currentIndexChanged.connect(self.on_wire_material_changed)

        self.ui.torque_lineedit.textChanged.connect(self.on_torque_changed)
        self.ui.torque_lineedit_lock.lock_state_changed.connect(self.on_torque_lock_changed)
        self.ui.speed_lineedit.textChanged.connect(self.on_speed_changed)
        self.ui.speed_lineedit_lock.lock_state_changed.connect(self.on_speed_lock_changed)
        self.ui.power_lineedit.textChanged.connect(self.on_power_changed)
        self.ui.power_lineedit_lock.lock_state_changed.connect(self.on_power_lock_changed)

        self.ui.efficiency_lineedit.textChanged.connect(self.on_efficiency_changed)
        self.ui.efficiency_lineedit_lock.lock_state_changed.connect(self.on_efficiency_lock_changed)
        self.ui.voltage_lineedit.textChanged.connect(self.on_voltage_changed)
        self.ui.voltage_lineedit_lock.lock_state_changed.connect(self.on_voltage_lock_changed)
        self.ui.max_current_lineedit.textChanged.connect(self.on_max_current_changed)
        self.ui.max_current_lineedit_lock.lock_state_changed.connect(self.on_max_current_lock_changed)

        self.ui.stator_diameter_lineedit.textChanged.connect(self.on_stator_diameter_changed)
        self.ui.stator_diameter_lineedit_lock.lock_state_changed.connect(self.on_stator_diameter_lock_changed)
        self.ui.stator_length_lineedit.textChanged.connect(self.on_stator_length_changed)
        self.ui.stator_length_lineedit_lock.lock_state_changed.connect(self.on_stator_length_lock_changed)
        self.ui.turns_per_phase_lineedit.textChanged.connect(self.on_turns_changed)
        self.ui.turns_per_phase_lineedit_lock.lock_state_changed.connect(self.on_turns_lock_changed)
        self.ui.num_phases_spinbox.valueChanged.connect(self.on_num_phases_changed)
        self.ui.num_phases_spinbox_lock.valueChanged.connect(self.on_num_phases_lock_changed)
        self.ui.num_poles_spinbox.valueChanged.connect(self.on_num_poles_changed)
        self.ui.num_poles_spinbox_lock.lock_state_changed.connect(self.on_num_poles_lock_changed)
        self.ui.num_slots_spinbox.valueChanged.connect(self.on_num_slots_changed)
        self.ui.num_slots_spinbox_lock.lock_state_changed.connect(self.on_num_slots_lock_changed)
        self.ui.stator_diameter_min_lineedit.textChanged.connect(self.on_stator_diameter_min_changed)
        self.ui.stator_diameter_max_lineedit.textChanged.connect(self.on_stator_diameter_max_changed)
        self.ui.stator_length_min_lineedit.textChanged.connect(self.on_stator_length_min_changed)
        self.ui.stator_length_max_lineedit.textChanged.connect(self.on_stator_length_max_changed)

        self.ui.rotor_diameter_lineedit.textChanged.connect(self.on_rotor_diameter_changed)
        self.ui.rotor_length_lineedit.textChanged.connect(self.on_rotor_length_changed)
        self.ui.rotor_thickness_lineedit.textChanged.connect(self.on_rotor_thickness_changed)
        self.ui.rotor_thickness_lineedit_lock.lock_state_changed.connect(self.on_rotor_thickness_lock_changed)

        self.ui.magnet_strength_lineedit.textChanged.connect(self.on_magnet_strength_changed)
        self.ui.air_gap_lineedit.textChanged.connect(self.on_air_gap_changed)
        self.ui.magnet_coverage_lineedit.textChanged.connect(self.on_magnet_coverage_changed)  # percent tube filled with magnets
        self.ui.magnet_thickness_lineedit_lock.lock_state_changed.connect(self.on_magnet_thickness_lock_changed)

        #self.ui.axle_support_length_lineedit.textChanged.connect(self.on_axle_support_length_changed)

    # region utility
    def set_error_state(self, widget, error_message):
        """Set red background and tooltip for error."""
        widget.setStyleSheet("background-color: rgb(255, 200, 200);")
        widget.setToolTip(error_message)

    def clear_error_state(self, widget):
        """Clear error state."""
        widget.setStyleSheet("")
        widget.setToolTip("")

    # endregion

    def calculate_winding_factor(self, num_slots, num_poles, num_phases):
        """Calculate winding factor for any slot-pole combination."""
        p = num_poles // 2  # Number of pole pairs
        q = num_slots / (2 * p * num_phases) if p != 0 and num_phases != 0 else 0

        # Display p and q
        self.ui.slot_pole_ratio_lineedit.set_value(q)

        # Validate slot-pole combination
        if q < 0.25:
            self.ui.winding_factor_lineedit.setText("")
            return 0, False, "Slot/pole ratio q < 0.25"
        if num_slots % num_phases != 0:
            self.ui.winding_factor_lineedit.setText("")
            return 0, False, f"Slots must be multiple of {num_phases}"
        if num_poles % 2 != 0:
            self.ui.winding_factor_lineedit.setText("")
            return 0, False, "Poles must be even"
        if self.gcd(num_slots, p) > 1:
            self.ui.winding_factor_lineedit.setText("")
            return 0, False, "High GCD may cause unbalanced pull"

        # Slot pitch (mechanical angle per slot)
        slot_pitch = 2 * math.pi * p / num_slots if num_slots != 0 else 0

        # Approximate coil pitch (slots per pole per phase)
        coil_pitch_slots = num_slots / (p * num_phases) if p != 0 and num_phases != 0 else 0
        coil_pitch_angle = coil_pitch_slots * slot_pitch

        # Pitch factor (k_p) for concentrated windings
        k_p = math.sin(coil_pitch_angle / 2) if coil_pitch_angle != 0 else 0.8

        # Distribution factor (k_d) ≈ 1 for concentrated windings
        k_d = 1.0

        # Winding factor (k_w = k_p * k_d)
        k_w = k_p * k_d
        k_w = min(max(k_w, 0.1), 1.0)

        # Display k_w
        self.ui.winding_factor_lineedit.set_value(k_w)

        return k_w, True, ""

    def calculate_motor_constants(self, T, omega, eta, V, I_max):
        """Calculate and set Ke and current, check constraints."""
        if omega == 0:
            self.set_error_state(self.ui.back_emf_constant_lineedit, "Zero speed")
            self.set_error_state(self.ui.current_lineedit, "Zero speed")
            self.ui.back_emf_constant_lineedit.setText("")
            self.ui.current_lineedit.setText("")
            return False
        Ke = (eta * V) / omega
        I = T / Ke if Ke != 0 else 0
        if I == 0:
            self.set_error_state(self.ui.current_lineedit, "Zero current")
            self.ui.back_emf_constant_lineedit.setText("")
            self.ui.current_lineedit.setText("")
            return False
        if I > I_max:
            self.set_error_state(self.ui.current_lineedit, "Current exceeds max")
            self.ui.back_emf_constant_lineedit.setText("")
            self.ui.current_lineedit.setText("")
            return False
        self.ui.back_emf_constant_lineedit.set_v_per_rad_s_value(Ke)
        self.ui.current_lineedit.set_a_value(I)
        self.clear_error_state(self.ui.back_emf_constant_lineedit)
        self.clear_error_state(self.ui.current_lineedit)
        return True

    def calculate_phase_resistance(self, V, eta, I):
        """Calculate and set phase resistance."""
        if I == 0:
            self.set_error_state(self.ui.phase_resistance_lineedit, "Zero current")
            self.ui.phase_resistance_lineedit.setText("")
            return False
        R = V * (1 - eta) / I
        self.ui.phase_resistance_lineedit.set_ohm_value(R)
        self.clear_error_state(self.ui.phase_resistance_lineedit)
        return True

    def calculate_stator_dimensions(self, T, p, N, B):
        """Calculate and set stator diameter and length."""
        try:
            D_min = self.ui.stator_diameter_min_lineedit.get_mm_value()
            D_max = self.ui.stator_diameter_max_lineedit.get_mm_value()
            L_min = self.ui.stator_length_min_lineedit.get_mm_value()
            L_max = self.ui.stator_length_max_lineedit.get_mm_value()

            if D_min >= D_max or L_min >= L_max:
                self.set_error_state(self.ui.stator_diameter_lineedit, "Invalid D min/max")
                self.set_error_state(self.ui.stator_length_lineedit, "Invalid L min/max")
                return False

            D_locked = self.ui.stator_diameter_lineedit_lock.is_locked()
            L_locked = self.ui.stator_length_lineedit_lock.is_locked()

            if D_locked and L_locked:
                D = self.ui.stator_diameter_lineedit.get_mm_value()
                L = self.ui.stator_length_lineedit.get_mm_value()
                # Torque ∝ p * N * B * D * L
                if abs(T - (p * N * B * D * L / 1000)) > 1e-6:  # Convert D, L to m
                    self.set_error_state(self.ui.stator_diameter_lineedit, "Locked D, L inconsistent with torque")
                    self.set_error_state(self.ui.stator_length_lineedit, "Locked D, L inconsistent with torque")
                    return False
            elif D_locked:
                D = self.ui.stator_diameter_lineedit.get_mm_value()
                if D < D_min or D > D_max:
                    self.set_error_state(self.ui.stator_diameter_lineedit, "Locked D outside range")
                    return False
                L = (T * 1000) / (p * N * B * D) if (p * N * B * D) != 0 else 0
                if L == 0 or L < L_min or L > L_max:
                    self.set_error_state(self.ui.stator_length_lineedit, "Calculated L outside range")
                    return False
                self.ui.stator_length_lineedit.set_mm_value(L)
            elif L_locked:
                L = self.ui.stator_length_lineedit.get_mm_value()
                if L < L_min or L > L_max:
                    self.set_error_state(self.ui.stator_length_lineedit, "Locked L outside range")
                    return False
                D = (T * 1000) / (p * N * B * L) if (p * N * B * L) != 0 else 0
                if D == 0 or D < D_min or D > D_max:
                    self.set_error_state(self.ui.stator_diameter_lineedit, "Calculated D outside range")
                    return False
                self.ui.stator_diameter_lineedit.set_mm_value(D)
            else:
                D = D_min
                L = (T * 1000) / (p * N * B * D) if (p * N * B * D) != 0 else 0
                if L == 0 or L < L_min or L > L_max:
                    self.set_error_state(self.ui.stator_length_lineedit, "Calculated L outside range")
                    return False
                self.ui.stator_diameter_lineedit.set_mm_value(D)
                self.ui.stator_length_lineedit.set_mm_value(L)

            self.clear_error_state(self.ui.stator_diameter_lineedit)
            self.clear_error_state(self.ui.stator_length_lineedit)
            return True
        except ValueError:
            self.set_error_state(self.ui.stator_diameter_lineedit, "Invalid input values")
            self.set_error_state(self.ui.stator_length_lineedit, "Invalid input values")
            return False

    def calculate_magnet_parameters(self, rotor_diameter, stator_diameter, stator_length, num_poles, B):
        """Calculate and set magnet count, width, thickness, and length."""
        try:
            air_gap = self.ui.air_gap_lineedit.get_mm_value()
            coverage = self.ui.magnet_coverage_lineedit.get_fraction_value()
            magnet_thickness_locked = self.ui.magnet_thickness_lineedit_lock.is_locked()
            rotor_thickness_locked = self.ui.rotor_thickness_lineedit_lock.is_locked()

            # Validate inputs
            if coverage <= 0 or coverage > 1:
                self.set_error_state(self.ui.magnet_coverage_lineedit, "Coverage must be 0 to 1")
                self.ui.magnet_count_lineedit.setText("")
                self.ui.magnet_width_lineedit.setText("")
                self.ui.magnet_length_lineedit.setText("")
                return False

            # Geometry constraints
            available_space = (rotor_diameter - stator_diameter - 2 * air_gap) / 2  # Space for magnet + rotor thickness
            if available_space <= 0:
                self.set_error_state(self.ui.rotor_diameter_lineedit, "Rotor diameter too small for air gap")
                self.ui.magnet_count_lineedit.setText("")
                self.ui.magnet_width_lineedit.setText("")
                self.ui.magnet_length_lineedit.setText("")
                return False

            # Number of magnets equals number of rotor poles
            magnet_count = num_poles
            self.ui.magnet_count_lineedit.set_value(magnet_count)

            # Magnet width: Arc length along rotor inner circumference
            rotor_inner_diameter = rotor_diameter - 2 * air_gap
            rotor_inner_circumference = math.pi * rotor_inner_diameter
            magnet_width = (rotor_inner_circumference / num_poles) * coverage
            self.ui.magnet_width_lineedit.set_mm_value(magnet_width)

            # Magnet thickness: Based on required magnetic field strength
            # Assume B = k * thickness (simplified, k depends on material, ~0.1 T/mm for neodymium)
            k = 0.1  # T/mm, typical for neodymium or Alnico
            magnet_thickness = B / k if k != 0 else 0
            magnet_thickness = min(max(magnet_thickness, 0.5), 10)  # Constrain: 0.5 mm to 10 mm

            # Rotor thickness: Remaining space after magnet thickness
            if magnet_thickness_locked and rotor_thickness_locked:
                magnet_thickness = self.ui.magnet_thickness_lineedit.get_mm_value()
                rotor_thickness = self.ui.rotor_thickness_lineedit.get_mm_value()
                if abs(available_space - (magnet_thickness + rotor_thickness)) > 1e-6:
                    self.set_error_state(self.ui.magnet_thickness_lineedit, "Locked thicknesses inconsistent with rotor diameter")
                    self.set_error_state(self.ui.rotor_thickness_lineedit, "Locked thicknesses inconsistent with rotor diameter")
                    self.ui.magnet_count_lineedit.setText("")
                    self.ui.magnet_width_lineedit.setText("")
                    self.ui.magnet_length_lineedit.setText("")
                    return False
            elif magnet_thickness_locked:
                magnet_thickness = self.ui.magnet_thickness_lineedit.get_mm_value()
                rotor_thickness = available_space - magnet_thickness
                if rotor_thickness < 0.5:  # Minimum rotor thickness
                    self.set_error_state(self.ui.magnet_thickness_lineedit, "Magnet thickness too large for rotor")
                    self.ui.magnet_count_lineedit.setText("")
                    self.ui.magnet_width_lineedit.setText("")
                    self.ui.magnet_length_lineedit.setText("")
                    return False
                self.ui.rotor_thickness_lineedit.set_mm_value(rotor_thickness)
            elif rotor_thickness_locked:
                rotor_thickness = self.ui.rotor_thickness_lineedit.get_mm_value()
                magnet_thickness = available_space - rotor_thickness
                if magnet_thickness < 0.5 or magnet_thickness > 10:
                    self.set_error_state(self.ui.rotor_thickness_lineedit, "Calculated magnet thickness out of range")
                    self.ui.magnet_count_lineedit.setText("")
                    self.ui.magnet_width_lineedit.setText("")
                    self.ui.magnet_length_lineedit.setText("")
                    return False
                self.ui.magnet_thickness_lineedit.set_mm_value(magnet_thickness)
            else:
                self.ui.magnet_thickness_lineedit.set_mm_value(magnet_thickness)
                rotor_thickness = available_space - magnet_thickness
                if rotor_thickness < 0.5:
                    rotor_thickness = 0.5
                    magnet_thickness = available_space - rotor_thickness
                    if magnet_thickness < 0.5 or magnet_thickness > 10:
                        self.set_error_state(self.ui.magnet_thickness_lineedit, "Calculated magnet thickness out of range")
                        self.ui.magnet_count_lineedit.setText("")
                        self.ui.magnet_width_lineedit.setText("")
                        self.ui.magnet_length_lineedit.setText("")
                        return False
                self.ui.rotor_thickness_lineedit.set_mm_value(rotor_thickness)

            # Magnet length: Matches stator length
            magnet_length = stator_length
            self.ui.magnet_length_lineedit.set_mm_value(magnet_length)

            self.clear_error_state(self.ui.magnet_count_lineedit)
            self.clear_error_state(self.ui.magnet_width_lineedit)
            self.clear_error_state(self.ui.magnet_thickness_lineedit)
            self.clear_error_state(self.ui.rotor_thickness_lineedit)
            self.clear_error_state(self.ui.magnet_length_lineedit)
            return True
        except ValueError:
            self.set_error_state(self.ui.magnet_count_lineedit, "Invalid input values")
            self.set_error_state(self.ui.magnet_width_lineedit, "Invalid input values")
            self.set_error_state(self.ui.magnet_thickness_lineedit, "Invalid input values")
            self.set_error_state(self.ui.rotor_thickness_lineedit, "Invalid input values")
            self.set_error_state(self.ui.magnet_length_lineedit, "Invalid input values")
            self.ui.magnet_count_lineedit.setText("")
            self.ui.magnet_width_lineedit.setText("")
            self.ui.magnet_length_lineedit.setText("")
            return False

    def calculate_wire_awg(self, current):
        """Calculate and set wire AWG based on current and material."""
        try:
            if current <= 0:
                self.set_error_state(self.ui.wire_awg_lineedit, "Invalid current")
                self.ui.wire_awg_lineedit.setText("")
                return False

            material = self.ui.wire_material_combobox.currentText()
            if material == 'Copper-Clad Aluminum':
                # CCA has ~61% conductivity of copper, needs ~1.64x cross-sectional area
                current *= 1.64

            # Find smallest AWG that can handle the current
            for awg, max_current in AWG_TABLE:
                if current <= max_current:
                    self.ui.wire_awg_lineedit.set_value(awg)
                    self.clear_error_state(self.ui.wire_awg_lineedit)
                    return True

            self.set_error_state(self.ui.wire_awg_lineedit, "Current too high for AWG table")
            self.ui.wire_awg_lineedit.setText("")
            return False
        except ValueError:
            self.set_error_state(self.ui.wire_awg_lineedit, "Invalid input values")
            self.ui.wire_awg_lineedit.setText("")
            return False

    def update_power_speed_torque(self):
        """Update power, speed, or torque based on lock states."""
        if self.computing:
            return
        self.computing = True
        try:
            T_locked = self.ui.torque_lineedit_lock.is_locked()
            omega_locked = self.ui.speed_lineedit_lock.is_locked()
            P_locked = self.ui.power_lineedit_lock.is_locked()

            T = self.ui.torque_lineedit.get_nm_value()
            omega = self.ui.speed_lineedit.get_rad_per_s_value()
            P = self.ui.power_lineedit.get_w_value()

            if sum([T_locked, omega_locked, P_locked]) >= 2:
                if T_locked and omega_locked and not P_locked:
                    self.ui.power_lineedit.set_w_value(T * omega)
                    self.clear_error_state(self.ui.power_lineedit)
                elif T_locked and P_locked and not omega_locked:
                    if T != 0:
                        self.ui.speed_lineedit.set_rad_per_s_value(P / T)
                        self.clear_error_state(self.ui.speed_lineedit)
                    else:
                        self.set_error_state(self.ui.speed_lineedit, "Zero torque")
                elif omega_locked and P_locked and not T_locked:
                    if omega != 0:
                        self.ui.torque_lineedit.set_nm_value(P / omega)
                        self.clear_error_state(self.ui.torque_lineedit)
                    else:
                        self.set_error_state(self.ui.torque_lineedit, "Zero speed")
                elif T_locked and omega_locked and P_locked:
                    if abs(P - T * omega) > 1e-6:
                        self.set_error_state(self.ui.power_lineedit, "Power inconsistent with torque * speed")
                    else:
                        self.clear_error_state(self.ui.power_lineedit)
            self.update_motor_constants()
        except ValueError:
            pass
        finally:
            self.computing = False

    def update_motor_constants(self):
        """Update motor constants and dependent parameters."""
        if self.computing:
            return
        self.computing = True
        try:
            T = self.ui.torque_lineedit.get_nm_value()
            omega = self.ui.speed_lineedit.get_rad_per_s_value()
            eta = self.ui.efficiency_lineedit.get_fraction_value()
            V = self.ui.voltage_lineedit.get_v_value()
            I_max = self.ui.max_current_lineedit.get_a_value()

            if self.calculate_motor_constants(T, omega, eta, V, I_max):
                I = self.ui.current_lineedit.get_a_value()
                if self.calculate_phase_resistance(V, eta, I):
                    self.update_stator_dimensions()
        finally:
            self.computing = False

    def update_stator_dimensions(self):
        """Update stator dimensions and dependent parameters."""
        if self.computing:
            return
        self.computing = True
        try:
            T = self.ui.torque_lineedit.get_nm_value()
            p = self.ui.num_poles_spinbox.value() // 2
            N = self.ui.turns_per_phase_lineedit.get_value()
            B = self.ui.magnet_strength_lineedit.get_t_value()

            if self.calculate_stator_dimensions(T, p, N, B):
                self.update_rotor_constraints()
        finally:
            self.computing = False

    def update_rotor_constraints(self):
        """Validate and update rotor diameter, length, and dependent parameters."""
        if self.computing:
            return
        self.computing = True
        try:
            stator_diameter = self.ui.stator_diameter_lineedit.get_mm_value()
            stator_length = self.ui.stator_length_lineedit.get_mm_value()
            air_gap = self.ui.air_gap_lineedit.get_mm_value()
            #axle_support_length = self.ui.axle_support_length_lineedit.get_mm_value()
            rotor_diameter = self.ui.rotor_diameter_lineedit.get_mm_value()
            rotor_length = self.ui.rotor_length_lineedit.get_mm_value()
            num_poles = self.ui.num_poles_spinbox.value()
            B = self.ui.magnet_strength_lineedit.get_t_value()

            # Rotor diameter must be >= stator diameter + 2 * air gap + 2 * magnet_thickness + 2 * rotor_thickness
            min_rotor_diameter = stator_diameter + 2 * air_gap  # Will be adjusted in magnet calc
            if rotor_diameter < min_rotor_diameter:
                self.set_error_state(self.ui.rotor_diameter_lineedit, f"Rotor diameter must be >= {min_rotor_diameter:.2f} mm")
                self.ui.magnet_count_lineedit.setText("")
                self.ui.magnet_width_lineedit.setText("")
                self.ui.magnet_length_lineedit.setText("")
                return

            # Rotor length must be >= stator length + axle support length
            min_rotor_length = stator_length
            if rotor_length < min_rotor_length:
                self.set_error_state(self.ui.rotor_length_lineedit, f"Rotor length must be >= {min_rotor_length:.2f} mm")
                self.ui.magnet_count_lineedit.setText("")
                self.ui.magnet_width_lineedit.setText("")
                self.ui.magnet_length_lineedit.setText("")
                return

            self.clear_error_state(self.ui.rotor_diameter_lineedit)
            self.clear_error_state(self.ui.rotor_length_lineedit)

            # Update magnet parameters
            if self.calculate_magnet_parameters(rotor_diameter, stator_diameter, stator_length, num_poles, B):
                # Update wire AWG
                current = self.ui.current_lineedit.get_a_value()
                self.calculate_wire_awg(current)
        except ValueError:
            self.set_error_state(self.ui.rotor_diameter_lineedit, "Invalid input values")
            self.set_error_state(self.ui.rotor_length_lineedit, "Invalid input values")
            self.ui.magnet_count_lineedit.setText("")
            self.ui.magnet_width_lineedit.setText("")
            self.ui.magnet_length_lineedit.setText("")
        finally:
            self.computing = False

    def on_torque_changed(self):
        self.update_power_speed_torque()

    def on_torque_lock_changed(self, locked):
        self.update_power_speed_torque()

    def on_speed_changed(self):
        self.update_power_speed_torque()

    def on_speed_lock_changed(self, locked):
        self.update_power_speed_torque()

    def on_power_changed(self):
        self.update_power_speed_torque()

    def on_power_lock_changed(self, locked):
        self.update_power_speed_torque()

    def on_efficiency_changed(self):
        self.update_motor_constants()

    def on_voltage_changed(self):
        self.update_motor_constants()

    def on_max_current_changed(self):
        self.update_motor_constants()

    def on_stator_diameter_changed(self):
        if not self.computing and self.ui.stator_diameter_lineedit_lock.is_locked():
            self.update_stator_dimensions()

    def on_stator_diameter_lock_changed(self, locked):
        self.update_stator_dimensions()

    def on_stator_length_changed(self):
        if not self.computing and self.ui.stator_length_lineedit_lock.is_locked():
            self.update_stator_dimensions()

    def on_stator_length_lock_changed(self, locked):
        self.update_stator_dimensions()

    def on_turns_changed(self):
        if not self.computing and self.ui.turns_per_phase_lineedit_lock.is_locked():
            self.update_stator_dimensions()

    def on_turns_lock_changed(self, locked):
        self.update_stator_dimensions()

    def on_num_poles_changed(self):
        self.update_stator_dimensions()

    def on_rotor_diameter_changed(self):
        self.update_rotor_constraints()

    def on_rotor_length_changed(self):
        self.update_rotor_constraints()

    def on_magnet_strength_changed(self):
        self.update_stator_dimensions()

    def on_air_gap_changed(self):
        self.update_rotor_constraints()

    def on_axle_support_length_changed(self):
        self.update_rotor_constraints()

    def on_stator_diameter_min_changed(self):
        self.update_stator_dimensions()

    def on_stator_diameter_max_changed(self):
        self.update_stator_dimensions()

    def on_stator_length_min_changed(self):
        self.update_stator_dimensions()

    def on_stator_length_max_changed(self):
        self.update_stator_dimensions()

    def on_wire_material_changed(self):
        self.update_rotor_constraints()

    def on_magnet_coverage_changed(self):
        self.update_rotor_constraints()

    def on_magnet_thickness_changed(self):
        if not self.computing and self.ui.magnet_thickness_lineedit_lock.is_locked():
            self.update_rotor_constraints()

    def on_magnet_thickness_lock_changed(self, locked):
        self.update_rotor_constraints()

    def on_rotor_thickness_changed(self):
        if not self.computing and self.ui.rotor_thickness_lineedit_lock.is_locked():
            self.update_rotor_constraints()

    def on_rotor_thickness_lock_changed(self, locked):
        self.update_rotor_constraints()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    dialog = BLDCDialog()
    dialog.show()
    sys.exit(app.exec_())

# Assumptions:
# - Ui_BLDCDialog exists and defines all UI elements (line edits, spinbox, lock buttons, wire_material_combobox).
# - Custom lock button widget has is_locked() method and lock_state_changed signal.
# - Line edits have get_<measurement>_value methods (e.g., get_nm_value, get_mm_value, get_v_per_rad_s_value, get_a_value, get_ohm_value, get_rad_per_s_value, get_w_value, get_fraction_value, get_t_value, get_value for turns and counts) returning Fraction or appropriate type.
# - Line edits have set_<measurement>_value methods (e.g., set_mm_value, set_ohm_value, set_value for integers).
# - FreeCAD-compatible units (mm for dimensions, Nm for torque, rad/s for speed, W for power, V for voltage, A for current, ohms for resistance, T for magnet strength).
# - wire_material_combobox is a QComboBox with 'Copper' and 'Copper-Clad Aluminum' options.
# - magnet_coverage_lineedit uses get_fraction_value for 0 to 1 range.
# - magnet_thickness_lineedit and rotor_thickness_lineedit have lock buttons.