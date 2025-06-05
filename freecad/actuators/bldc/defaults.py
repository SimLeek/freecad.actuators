
# stop potential import loops
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_window import BLDCWindow
else:
    from typing import Any
    BLDCWindow = Any
from fractions import Fraction


defaults = {
        "Quadcopter Motor": {
            "output_rpm": 26400,
            "output_torque": 0.5,
            "gearbox_ratio": 1,
            "motor_rpm": 26400,
            "motor_torque": 0.5,
            "max_volts": 12,
            "max_temp": 80+273.15,
            "motor_radius": 28,
            "num_slots": 12,
            "num_magnets": 10,
            "air_gap": .5,
            "axle_radius": 9,
            "slot_width": 1.5,
            "hammerhead_width": 4,
            "hammerhead_length": 1,
            "stator_inner_radius": 11,
            "magnet_thickness": 2,
            "outrunner_thickness": 1,
            "wire_diameter": 0.5,
            "turns_per_slot": 176,
            "needle_diameter": 1,
            "drill_bit_diameter": 1,
            "tight_pack": True,
            "needle_winding": True,
            "cnc_milling": True
        },
        "Micro Motor": {
            "output_rpm": 10000, "output_torque": 0.01, "gearbox_ratio": 5, "motor_rpm": 50000, "motor_torque": 0.002,
            "max_volts": 12, "max_temp": 60+273.15,
            "motor_radius": 10, "num_slots": 6, "num_magnets": 4, "air_gap": 0.2, "axle_radius": 1,
            "slot_width": 1, "hammerhead_width": 0.2, "hammerhead_length": 0.2, "stator_inner_radius": 2,
            "magnet_thickness": 0.5, "outrunner_thickness": 0.5,
            "wire_diameter": 0.1, "turns_per_slot": 20, "needle_diameter": 0.2, "drill_bit_diameter": 0.2
        },
        "MEMS Motor": {
            "output_rpm": 50000, "output_torque": 0.0001, "gearbox_ratio": 10, "motor_rpm": 500000, "motor_torque": 0.00001,
            "max_volts": 5, "max_temp": 50+273.15,
            "motor_radius": 2, "num_slots": 3, "num_magnets": 2, "air_gap": 0.05, "axle_radius": 0.2,
            "slot_width": 0.2, "hammerhead_width": 0.05, "hammerhead_length": 0.05, "stator_inner_radius": 0.5,
            "magnet_thickness": 0.1, "outrunner_thickness": 0.1,
            "wire_diameter": 0.02, "turns_per_slot": 5, "needle_diameter": 0.05, "drill_bit_diameter": 0.05
        },
        "Car Motor": {
            "output_rpm": 3000, "output_torque": 100, "gearbox_ratio": 4, "motor_rpm": 12000, "motor_torque": 25,
            "max_volts": 400, "max_temp": 120+273.15,
            "motor_radius": 150, "num_slots": 36, "num_magnets": 32, "air_gap": 2, "axle_radius": 20,
            "slot_width": 10, "hammerhead_width": 2, "hammerhead_length": 2, "stator_inner_radius": 50,
            "magnet_thickness": 5, "outrunner_thickness": 10,
            "wire_diameter": 2, "turns_per_slot": 100, "needle_diameter": 3, "drill_bit_diameter": 3
        },
        "Airplane Motor": {
            "output_rpm": 8000, "output_torque": 10, "gearbox_ratio": 2, "motor_rpm": 16000, "motor_torque": 5,
            "max_volts": 48, "max_temp": 100+273.15,
            "motor_radius": 100, "num_slots": 24, "num_magnets": 20, "air_gap": 1.5, "axle_radius": 10,
            "slot_width": 8, "hammerhead_width": 1.5, "hammerhead_length": 1.5, "stator_inner_radius": 30,
            "magnet_thickness": 3, "outrunner_thickness": 5,
            "wire_diameter": 1, "turns_per_slot": 80, "needle_diameter": 2, "drill_bit_diameter": 2
        }
    }

def connect_defaults(bldc_window: BLDCWindow):
    bldc_window.ui.default_settings_apply_button.clicked.connect(lambda: apply_default_settings(bldc_window))

def apply_default_settings(bldc_window: BLDCWindow):
    """Populate UI fields with default values based on selected motor type."""
    motor_type = bldc_window.ui.default_settings_combobox.currentText()

    if motor_type not in defaults:
        raise NotImplementedError("Unknown Motor Default Type")

    params = defaults[motor_type]
    # Input/Output Properties
    bldc_window.ui.output_rpm_lineedit.set_rpm_value(params["output_rpm"])
    bldc_window.ui.output_torque_lineedit.set_nm_value(params["output_torque"])  # output_torque
    bldc_window.ui.gearbox_ratio_lineedit.set_value(Fraction(params["gearbox_ratio"]))  # gearbox_ratio
    bldc_window.ui.motor_rpm_lineedit.set_rpm_value(params["motor_rpm"])  # motor_rpm
    bldc_window.ui.motor_torque_lineedit.set_nm_value(params["motor_torque"])  # motor_torque
    bldc_window.ui.max_volts_lineedit.set_v_value(params["max_volts"])  # max_volts
    bldc_window.ui.max_temp_lineedit.set_k_value(params["max_temp"])  # max_temp

    # Physical Properties
    bldc_window.ui.radius_lineedit.set_mm_value(params["motor_radius"])
    bldc_window.ui.num_slots_lineedit.set_value(params["num_slots"])
    bldc_window.ui.num_magnets_lineedit.set_value(params["num_magnets"])
    bldc_window.ui.air_gap_lineedit.set_mm_value(params["air_gap"])
    bldc_window.ui.axle_radius_lineedit.set_mm_value(params["axle_radius"])

    # Stator
    bldc_window.ui.slot_width_lineedit.set_mm_value(params["slot_width"])
    bldc_window.ui.hammerhead_width_lineedit.set_mm_value(params["hammerhead_width"])
    bldc_window.ui.hammerhead_length_lineedit.set_mm_value(params["hammerhead_length"])
    bldc_window.ui.stator_inner_radius_lineedit.set_mm_value(params["stator_inner_radius"])

    # Magnet and Outrunner
    bldc_window.ui.magnet_thickness_lineedit.set_mm_value(params["magnet_thickness"])
    bldc_window.ui.outrunner_thickness_lineedit.set_mm_value(params["outrunner_thickness"])

    # Wire
    bldc_window.ui.wire_diameter_lineedit.set_mm_value(params["wire_diameter"])
    bldc_window.ui.turns_per_slot_lineedit.set_value(params["turns_per_slot"])
    bldc_window.ui.needle_diameter_lineedit.set_mm_value(params["needle_diameter"])

    # CNC
    bldc_window.ui.drill_bit_diameter_lineedit.set_mm_value(params["drill_bit_diameter"])

    bldc_window.ui.tight_pack_checkbox.setChecked(params["tight_pack"])
    bldc_window.ui.needle_winding_checkbox.setChecked(params["needle_winding"])
    bldc_window.ui.cnc_milling_checkbox.setChecked(params["cnc_milling"])

    bldc_window.update_visualization(bldc_window)