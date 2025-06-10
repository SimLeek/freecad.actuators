"""
UI and visualization management functions for the BLDC Motor Stator Visualization.
"""
import math
# stop potential import loops
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window import BLDCWindow
else:
    from typing import Any
    BLDCWindow = Any
import colorsys

def connect_slot_pole(bldc_window: BLDCWindow):
    """Create horizontal Display Options group at the top."""
    bldc_window.slot_pole_validation = SlotPoleValidation(bldc_window)
    bldc_window.ui.slot_pole_grid_widget.set_callback(bldc_window.slot_pole_validation.slot_pole_cell_callback)
    bldc_window.ui.slot_pole_grid_widget.model.row_header_callback = bldc_window.slot_pole_validation.row_header_callback
    bldc_window.ui.slot_pole_grid_widget.model.col_header_callback = bldc_window.slot_pole_validation.col_header_callback
    bldc_window.ui.slot_pole_grid_widget.model.bounds = [3, 2, None, None]
    bldc_window.ui.slot_pole_grid_widget.model.rows = 36
    bldc_window.ui.slot_pole_grid_widget.model.cols = 42
    bldc_window.ui.slot_pole_grid_widget.set_selection(1, 1)  # set selection must be after to update grid

    bldc_window.ui.display_winding_factor_radio_button.toggled.connect(bldc_window.ui.slot_pole_grid_widget.update_cell_callback)
    bldc_window.ui.display_freq_at_rpm_radio_button.toggled.connect(bldc_window.ui.slot_pole_grid_widget.update_cell_callback)
    bldc_window.ui.display_cogging_freq_radio_button.toggled.connect(bldc_window.ui.slot_pole_grid_widget.update_cell_callback)
    bldc_window.ui.display_winding_balance_radio_button.toggled.connect(bldc_window.ui.slot_pole_grid_widget.update_cell_callback)

    bldc_window.ui.display_coil_span_radio_button.toggled.connect(bldc_window.ui.slot_pole_grid_widget.update_cell_callback)
    bldc_window.ui.display_chording_radio_button.toggled.connect(bldc_window.ui.slot_pole_grid_widget.update_cell_callback)
    bldc_window.ui.display_magnet_pitch_factor_radio_button.toggled.connect(bldc_window.ui.slot_pole_grid_widget.update_cell_callback)
    bldc_window.ui.display_winding_distribution_radio_button.toggled.connect(bldc_window.ui.slot_pole_grid_widget.update_cell_callback)
    bldc_window.ui.display_slot_pole_radio_button.toggled.connect(bldc_window.ui.slot_pole_grid_widget.update_cell_callback)

    bldc_window.ui.remove_no_symmetry_checkbox.toggled.connect(bldc_window.ui.slot_pole_grid_widget.update_cell_callback)
    bldc_window.ui.remove_unbalanced_checkbox.toggled.connect(bldc_window.ui.slot_pole_grid_widget.update_cell_callback)
    bldc_window.ui.remove_ns_is_nm_checkbox.toggled.connect(bldc_window.ui.slot_pole_grid_widget.update_cell_callback)
    bldc_window.ui.remove_q_less_0_25_checkbox.toggled.connect(bldc_window.ui.slot_pole_grid_widget.update_cell_callback)
    bldc_window.ui.remove_q_gt_0_5_checkbox.toggled.connect(bldc_window.ui.slot_pole_grid_widget.update_cell_callback)

    bldc_window.ui.motor_rpm_lineedit.textChanged.connect(bldc_window.ui.slot_pole_grid_widget.update_cell_callback)

    bldc_window.ui.slot_pole_grid_widget.selection_changed_callback = bldc_window.slot_pole_validation.update_lineedits
    bldc_window.ui.num_slots_lineedit.textChanged.connect(bldc_window.slot_pole_validation.update_grid)

    bldc_window.ui.num_arc_magnets_lineedit.textChanged.connect(bldc_window.slot_pole_validation.update_grid)
    bldc_window.ui.num_square_magnets_lineedit.textChanged.connect(bldc_window.slot_pole_validation.update_grid)
    bldc_window.ui.magnet_tab_widget.currentChanged.connect(bldc_window.slot_pole_validation.update_grid)

class SlotPoleValidation(object):
    def __init__(self, window :BLDCWindow):
        self.window = window

    @staticmethod
    def row_header_callback(x):
        num_phases = 3
        return int(x * num_phases)

    @staticmethod
    def col_header_callback(y):
        return int(y * 2)

    def update_lineedits(self, selected, deselected):
        indexes = selected.indexes()
        if indexes:
            index = indexes[0]
            num_poles = self.col_header_callback(index.column() + self.window.ui.slot_pole_grid_widget.model.x_offset)
            num_slots = self.row_header_callback(index.row() + self.window.ui.slot_pole_grid_widget.model.y_offset)

            # todo: Needs to override locks, so let's use a button for this later.
            #self.window.ui.num_slots_lineedit.set_value(int(num_slots))
            #if self.window.ui.magnet_tab_widget.currentIndex() == 0:
            #    self.window.ui.num_square_magnets_lineedit.set_value(int(num_poles))
            #else:
            #    self.window.ui.num_arc_magnets_lineedit.set_value(int(num_poles))

    def update_grid(self):
        num_slots = int(self.window.ui.num_slots_lineedit.get_value())

        if self.window.ui.magnet_tab_widget.currentIndex()==0:
            num_poles = int(self.window.ui.num_square_magnets_lineedit.get_value())
        else:
            num_poles = int(self.window.ui.num_arc_magnets_lineedit.get_value())

        x_pos = int(num_poles/2)
        y_pos = int(num_slots/3)

        self.window.ui.slot_pole_grid_widget.set_selection(x_pos, y_pos)

    def slot_pole_cell_callback(self, x, y):
        # thanks:
        #   https://docs.google.com/spreadsheets/d/1AZ2w6lbniuLydnSUgLaUv4zhjWA-wICHkOnHHVaU8Mg
        #   https://things-in-motion.blogspot.com/2019/01/selecting-best-pole-and-slot.html
        number_of_poles = x
        number_of_slots = y
        num_phases = 3
        winding_order=1
        if number_of_slots<2 or number_of_poles<2:
            return False, "f", (0,0,0)

        selectable=True
        color_hsv = [0, 0, 255]

        q = number_of_slots/(number_of_poles*num_phases)
        winding_distribution_z = number_of_slots/math.gcd(number_of_slots, number_of_poles*num_phases)
        #print(f"slots:{number_of_slots}")
        #print(f"poles:{number_of_poles}")
        #print(f"phases:{num_phases}")
        #print(f"z:{winding_distribution_z}")
        magnet_pitch_factor = math.sin(math.radians(0.5*winding_order*60))/(winding_distribution_z*math.sin(math.radians((winding_order*60)/(2*winding_distribution_z))))
        _gamma_s = math.pi*number_of_poles/number_of_slots
        chording = math.pi - _gamma_s
        coil_span_factor = math.cos(0.5*winding_order*chording)
        winding_factor = coil_span_factor*magnet_pitch_factor
        rpm = self.window.ui.motor_rpm_lineedit.get_rpm_value()
        freq = (rpm/60)*(number_of_poles/2)

        winding_balance = (number_of_slots/(3*math.gcd(int(number_of_slots), int(number_of_poles/2))))%1.0
        lcm = math.lcm(x, y)

        text="?"

        if self.window.ui.display_slot_pole_radio_button.isChecked():
            text = f"{q:.2f}"
            color_hsv = [max(0,120*(1.0-(.375-q))),255,255]
        elif self.window.ui.display_winding_distribution_radio_button.isChecked():
            text = f"{int(winding_distribution_z)}"
            color_hsv = [min(120, int(120 * abs(winding_distribution_z/35))), 255, 255]
        elif self.window.ui.display_magnet_pitch_factor_radio_button.isChecked():
            text = f"{magnet_pitch_factor:.3f}"
            color_hsv = [min(120, int(120 * (magnet_pitch_factor/.045 - 1.0))), 255, 255]
        elif self.window.ui.display_chording_radio_button.isChecked():
            text = f"{chording:.3f}"
            color_hsv = [max(0, int(120 * (1.0-chording/3.0))), 255, 255]
        elif self.window.ui.display_coil_span_radio_button.isChecked():
            text = f"{coil_span_factor:.3f}"
            color_hsv = [max(0, int(120 * ((coil_span_factor+1) / 2.0))), 255, 255]
        elif self.window.ui.display_winding_factor_radio_button.isChecked():
            text = f"{winding_factor:.3f}"
            color_hsv = [max(0, int(120 * ((winding_factor + 1) / 2.0))), 255, 255]
        elif self.window.ui.display_winding_balance_radio_button.isChecked():
            text = f"{winding_balance:.3f}"
            color_hsv = [max(0, int(120 * (1.0 - winding_balance))), 255, 255]
        elif self.window.ui.display_cogging_freq_radio_button.isChecked():
            text = f"{int(lcm)}"
            color_hsv = [min(120, int(120 * (lcm/8000))), 255, 255]
        elif self.window.ui.display_freq_at_rpm_radio_button.isChecked():
            text = f"{int(freq)}"
            color_hsv = [max(0, int(120 * (1-freq/2000))), 255, 255]

        if self.window.ui.remove_q_less_0_25_checkbox.isChecked() and q<.25:
            text="q<.25"
            selectable = False
            color_hsv[1]=127
            color_hsv[2] = 127
        if self.window.ui.remove_q_gt_0_5_checkbox.isChecked() and q>.5:
            text = "q>.5"
            selectable = False
            color_hsv[1] = 127
            color_hsv[2] = 127
        if self.window.ui.remove_ns_is_nm_checkbox.isChecked() and x==y:
            text = "Ns=Nm"
            selectable = False
            color_hsv[1] = 127
            color_hsv[2] = 127
        if self.window.ui.remove_unbalanced_checkbox.isChecked() and winding_balance!=0:
            text = "UnBal"
            selectable = False
            color_hsv[1] = 127
            color_hsv[2] = 127
        if self.window.ui.remove_no_symmetry_checkbox.isChecked() and math.gcd(x, y)==1:
            text = "NoSym"
            selectable = False
            color_hsv[1] = 127
            color_hsv[2] = 127

        bg_color = colorsys.hsv_to_rgb(color_hsv[0]/360, color_hsv[1]/255, color_hsv[2]/255)
        bg_color = [int(c*255) for c in bg_color]
        #print(color_hsv, bg_color)

        return True, text, bg_color
