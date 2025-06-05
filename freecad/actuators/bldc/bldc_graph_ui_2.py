"""
BLDC Motor Stator Visualization module.

This module provides a graphical interface to visualize a BLDC motor stator
using PySide2 and pyqtgraph, allowing users to adjust parameters and display
various components of the motor.
"""
import sys
import numpy as np
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QDoubleSpinBox,
    QLabel,
    QLineEdit,
    QCheckBox,
    QGroupBox,
    QScrollArea,
)
import pyqtgraph as pg


def traverse_tuple(nums):
    """Automatically handles backwards iteration for range."""
    start, end = nums
    if start <= end:
        for i in range(start, end):
            yield i
    else:
        for i in range(start, end, -1):
            yield i


class BLDCWindow(QMainWindow):
    """A window for visualizing BLDC motor stator with interactive controls."""

    def __init__(self):
        """Initialize the BLDC motor visualization window."""
        super().__init__()
        self.setWindowTitle("BLDC Motor Stator Visualization")
        self.setGeometry(100, 100, 1000, 800)

        # Parameters
        self.radius = 100.0
        self.num_slots = 12.0
        self.num_magnets = 10.0
        self.slot_width = 10.0
        self.hammerhead_width = 2.0
        self.hammerhead_length = 2.0
        self.air_gap = 5.0
        self.axle_radius = 15.0
        self.stator_inner_radius = 20.0
        self.magnet_thickness = 3.0
        self.wire_awg = 1.0
        self.num_turns_per_slot = 70
        self.outrunner_thickness = 5.0
        self.tight_pack = False
        self.fast_display = False
        self.cnc_milling = False
        self.drill_bit_diameter = 2.0
        self.needle_winding = False
        self.needle_winder_diameter = 2.0
        self.display_axle = True
        self.display_stator_core = True
        self.display_wires = True
        self.display_magnets = True
        self.display_outrunner = True
        self.turns_per_layer_list = None
        self.spinboxes = {}
        self.cached_turns_per_layer = None

        # Main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        main_layout = QVBoxLayout(self.main_widget)

        # Display Options (Horizontal at top)
        self.create_display_group(main_layout)

        # Content layout (Graph + Scrollable Controls)
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        # Plot widget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setAspectLocked(True)
        self.plot_widget.setRange(xRange=[-150, 150], yRange=[-150, 150])
        self.plot_widget.setBackground("w")
        content_layout.addWidget(self.plot_widget, 3)

        # Scrollable control panel
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        scroll_area.setWidget(control_widget)
        content_layout.addWidget(scroll_area, 3)

        # Create grouped UI elements
        self.create_ui_groups(control_layout)

        # Connect range changed signal
        self.plot_widget.sigRangeChanged.connect(self.update_visualization_with_cache)
        self.use_cache = False

        # Initial draw
        self.update_visualization()

    def create_display_group(self, main_layout):
        """Create horizontal Display Options group at the top."""
        display_group = QGroupBox("Display Options")
        display_layout = QHBoxLayout()
        for param in [
            "display_axle",
            "display_stator_core",
            "display_wires",
            "display_magnets",
            "display_outrunner",
        ]:
            checkbox = QCheckBox(param.replace("_", " ").title())
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(self.update_visualization)
            setattr(self, f"{param}_checkbox", checkbox)
            display_layout.addWidget(checkbox)
        display_group.setLayout(display_layout)
        main_layout.addWidget(display_group)

    def create_ui_groups(self, control_layout):
        """Create grouped UI elements for motor parameters."""
        # General Parameters Group
        general_group = QGroupBox("General Parameters")
        general_layout = QVBoxLayout()
        for param in ["radius", "num_slots", "num_magnets", "air_gap", "axle_radius"]:
            self.add_spinbox(general_layout, param)
        general_group.setLayout(general_layout)
        control_layout.addWidget(general_group)

        # Stator Group
        stator_group = QGroupBox("Stator Parameters")
        stator_layout = QVBoxLayout()
        for param in [
            "slot_width",
            "hammerhead_width",
            "hammerhead_length",
            "stator_inner_radius",
        ]:
            self.add_spinbox(stator_layout, param)
        stator_group.setLayout(stator_layout)
        control_layout.addWidget(stator_group)

        # Magnet and Outrunner Group
        magnet_group = QGroupBox("Magnet and Outrunner Parameters")
        magnet_layout = QVBoxLayout()
        for param in ["magnet_thickness", "outrunner_thickness"]:
            self.add_spinbox(magnet_layout, param)
        magnet_group.setLayout(magnet_layout)
        control_layout.addWidget(magnet_group)

        # Wire Group
        wire_group = QGroupBox("Wire Parameters")
        wire_layout = QVBoxLayout()
        for param in ["wire_awg", "num_turns_per_slot", "needle_winder_diameter"]:
            self.add_spinbox(wire_layout, param)
        self.turns_per_layer_input = QLineEdit()
        self.turns_per_layer_input.setPlaceholderText("Turns per layer (e.g., [5,4,3])")
        wire_layout.addWidget(QLabel("Turns per Layer"))
        wire_layout.addWidget(self.turns_per_layer_input)
        self.turns_per_layer_input.editingFinished.connect(self.update_visualization)
        self.tight_pack_checkbox = QCheckBox("Tight Pack (Hexagonal)")
        self.tight_pack_checkbox.stateChanged.connect(self.update_visualization)
        wire_layout.addWidget(self.tight_pack_checkbox)
        self.needle_winding_checkbox = QCheckBox("Needle Winding")
        self.needle_winding_checkbox.stateChanged.connect(self.update_visualization)
        wire_layout.addWidget(self.needle_winding_checkbox)
        wire_group.setLayout(wire_layout)
        control_layout.addWidget(wire_group)

        # CNC Group
        cnc_group = QGroupBox("CNC Parameters")
        cnc_layout = QVBoxLayout()
        self.cnc_milling_checkbox = QCheckBox("CNC Milling")
        self.cnc_milling_checkbox.stateChanged.connect(self.update_visualization)
        cnc_layout.addWidget(self.cnc_milling_checkbox)
        self.add_spinbox(cnc_layout, "drill_bit_diameter")
        cnc_group.setLayout(cnc_layout)
        control_layout.addWidget(cnc_group)

        # Add stretch to push content up
        control_layout.addStretch()

    def add_spinbox(self, layout, param):
        """Add a spinbox for a parameter to the layout."""
        label = QLabel(param.replace("_", " ").title())
        layout.addWidget(label)
        spinbox = QDoubleSpinBox()
        decimals = 2
        if param in ["num_slots", "num_magnets", "num_turns_per_slot"]:
            decimals = 0
        elif param in ["wire_awg", "needle_winder_diameter", "drill_bit_diameter"]:
            decimals = 2
        spinbox.setDecimals(decimals)
        spinbox.setSingleStep(0.1 if param in ["wire_awg", "needle_winder_diameter"] else 1.0)
        if param in ["num_slots", "num_magnets", "num_turns_per_slot"]:
            spinbox.setMinimum(1)  # Ensure positive integers
        spinbox.setValue(getattr(self, param))
        spinbox.valueChanged.connect(self.update_visualization)
        spinbox.setRange(0, 100000)
        layout.addWidget(spinbox)
        self.spinboxes[param] = spinbox

    def update_visualization_with_cache(self):
        """Update visualization using cached turns per layer."""
        self.use_cache = True
        self.update_visualization()
        self.use_cache = False

    def update_visualization(self):
        """Update the visualization based on current parameter values."""
        # Update parameters from spinboxes
        for param, spinbox in self.spinboxes.items():
            setattr(self, param, spinbox.value())

        # Update checkboxes
        self.tight_pack = self.tight_pack_checkbox.isChecked()
        self.cnc_milling = self.cnc_milling_checkbox.isChecked()
        self.needle_winding = self.needle_winding_checkbox.isChecked()
        self.display_axle = self.display_axle_checkbox.isChecked()
        self.display_stator_core = self.display_stator_core_checkbox.isChecked()
        self.display_wires = self.display_wires_checkbox.isChecked()
        self.display_magnets = self.display_magnets_checkbox.isChecked()
        self.display_outrunner = self.display_outrunner_checkbox.isChecked()

        # Parse turns per layer
        if not self.use_cache:
            max_turns_text = self.turns_per_layer_input.text()
            if max_turns_text:
                try:
                    self.turns_per_layer_list = eval(max_turns_text)
                    self.cached_turns_per_layer = self.turns_per_layer_list
                except Exception:
                    self.turns_per_layer_list = None
            else:
                self.turns_per_layer_list = None
        else:
            self.turns_per_layer_list = self.cached_turns_per_layer

        # Clear plot
        self.plot_widget.clear()

        # Calculate pixel scale
        view_range = self.plot_widget.getViewBox().viewRange()
        plot_size = self.plot_widget.size()
        x_scale = (view_range[0][1] - view_range[0][0]) / plot_size.width()
        y_scale = (view_range[1][1] - view_range[1][0]) / plot_size.height()
        pixel_per_unit = min(x_scale, y_scale)

        # Draw components
        if self.display_axle:
            self.draw_axle(pixel_per_unit)
        if self.display_stator_core:
            self.draw_stator_core(pixel_per_unit)
        if self.display_wires:
            self.draw_wires(pixel_per_unit)
        if self.display_magnets:
            self.draw_magnets(pixel_per_unit)
        if self.display_outrunner:
            self.draw_outrunner(pixel_per_unit)

    def draw_axle(self, _):
        """Draw the central axle circle."""
        theta = np.linspace(0, 2 * np.pi, 60, endpoint=False)
        x = self.axle_radius * np.cos(theta)
        y = self.axle_radius * np.sin(theta)
        x = np.append(x, x[0])
        y = np.append(y, y[0])
        pen_width = 2
        self.plot_widget.plot(x, y, pen=pg.mkPen("#000000", width=pen_width))

    def draw_magnets(self, _):
        """Draw magnets on the outrunner with thickness toward the stator."""
        magnet_outer_radius = self.radius
        magnet_inner_radius = magnet_outer_radius - self.magnet_thickness
        magnet_arc = 2 * np.pi / self.num_magnets
        for i in range(int(self.num_magnets)):
            magnet_angle = i * (2 * np.pi / self.num_magnets)
            start_angle = magnet_angle - magnet_arc / 3
            end_angle = magnet_angle + magnet_arc / 3
            theta_magnet = np.linspace(start_angle, end_angle, 20, endpoint=False)
            x_inner = magnet_inner_radius * np.cos(theta_magnet)
            y_inner = magnet_inner_radius * np.sin(theta_magnet)
            x_outer = magnet_outer_radius * np.cos(theta_magnet[::-1])
            y_outer = magnet_outer_radius * np.sin(theta_magnet[::-1])
            x_magnet = np.concatenate([x_inner, x_outer])
            y_magnet = np.concatenate([y_inner, y_outer])
            x_magnet = np.append(x_magnet, x_magnet[0])
            y_magnet = np.append(y_magnet, y_magnet[0])
            pen_width = 2
            # todo: move this plot outside the for loop and add nans to x and y to keep plots separate
            self.plot_widget.plot(x_magnet, y_magnet, pen=pg.mkPen("#C0C0C0", width=pen_width))

    def draw_outrunner(self, _):
        """Draw outrunner circles with editable thickness."""
        theta = np.linspace(0, 2 * np.pi, 200, endpoint=False)
        inner_radius = self.radius
        x_inner = inner_radius * np.cos(theta)
        y_inner = inner_radius * np.sin(theta)
        x_inner = np.append(x_inner, x_inner[0])
        y_inner = np.append(y_inner, y_inner[0])
        pen_width = 2
        self.plot_widget.plot(x_inner, y_inner, pen=pg.mkPen("#808080", width=pen_width))
        outer_radius = inner_radius + self.outrunner_thickness
        x_outer = outer_radius * np.cos(theta)
        y_outer = outer_radius * np.sin(theta)
        x_outer = np.append(x_outer, x_outer[0])
        y_outer = np.append(y_outer, y_outer[0])
        self.plot_widget.plot(x_outer, y_outer, pen=pg.mkPen("#808080", width=pen_width))

    # region Stator

    def _calculate_slot_points(
        self,
        slot_idx,
        num_slots,
        slot_width_half,
        hammerhead_width,
        hammerhead_length,
        r_inner,
        r_outer,
        cnc_milling,
        drill_bit_radius,
    ):
        """Calculate points for a single stator slot."""
        q = (slot_idx * (360 / num_slots)) / 180 * np.pi
        x_slot, y_slot = [], []

        if cnc_milling:
            quarter_center_x = (
                r_inner * np.cos(q)
                + drill_bit_radius * np.sin(q)
                + slot_width_half * np.sin(q)
            )
            quarter_center_y = (
                r_inner * np.sin(q)
                - drill_bit_radius * np.cos(q)
                - slot_width_half * np.cos(q)
            )
            theta_quarter_start = np.linspace(q + np.pi / 2-np.pi/(2*20), q, 10, endpoint=False)
            x_quarter_start = quarter_center_x - (drill_bit_radius * np.sin(theta_quarter_start))
            y_quarter_start = quarter_center_y + (drill_bit_radius * np.cos(theta_quarter_start))
            x_slot.extend(x_quarter_start)
            y_slot.extend(y_quarter_start)

        t_vals = np.linspace(r_inner, r_outer, 2)
        x_left = t_vals * np.cos(q) - slot_width_half * np.sin(q)
        y_left = t_vals * np.sin(q) + slot_width_half * np.cos(q)
        x_right = t_vals * np.cos(q) + slot_width_half * np.sin(q)
        y_right = t_vals * np.sin(q) - slot_width_half * np.cos(q)

        hammer_theta = np.arctan2(hammerhead_width + slot_width_half, r_outer + hammerhead_length)
        hammer_length_adjusted = hammerhead_length - (hammerhead_width + slot_width_half) * np.tan(
            hammer_theta
        )
        tip_x_left = r_outer * np.cos(q) - (hammerhead_width + slot_width_half) * np.sin(q)
        tip_y_left = r_outer * np.sin(q) + (hammerhead_width + slot_width_half) * np.cos(q)
        end_x_left = tip_x_left + hammer_length_adjusted * np.cos(q)
        end_y_left = tip_y_left + hammer_length_adjusted * np.sin(q)
        tip_x_right = r_outer * np.cos(q) + (hammerhead_width + slot_width_half) * np.sin(q)
        tip_y_right = r_outer * np.sin(q) - (hammerhead_width + slot_width_half) * np.cos(q)
        end_x_right = tip_x_right + hammer_length_adjusted * np.cos(q)
        end_y_right = tip_y_right + hammer_length_adjusted * np.sin(q)

        if cnc_milling:
            half_center_x_left = x_left[-1] + drill_bit_radius * np.cos(q + np.pi / 2)
            half_center_y_left = y_left[-1] + drill_bit_radius * np.sin(q + np.pi / 2)
            theta_half_left = np.linspace(q + 2 * np.pi-np.pi/(2*30), q + np.pi, 15, endpoint=False)
            x_half_left = half_center_x_left - (drill_bit_radius * np.sin(theta_half_left))
            y_half_left = half_center_y_left + (drill_bit_radius * np.cos(theta_half_left))
            half_center_x_right = x_right[-1] - drill_bit_radius * np.cos(q + np.pi / 2)
            half_center_y_right = y_right[-1] - drill_bit_radius * np.sin(q + np.pi / 2)
            theta_half_right = np.linspace(q + 2 * np.pi-np.pi/(2*30), q + np.pi, 15, endpoint=False)
            x_half_right = half_center_x_right - (drill_bit_radius * np.sin(theta_half_right))
            y_half_right = half_center_y_right + (drill_bit_radius * np.cos(theta_half_right))

        x_hammer_left = np.linspace(tip_x_left, end_x_left, 2)
        y_hammer_left = np.linspace(tip_y_left, end_y_left, 2)
        x_hammer_right = np.linspace(tip_x_right, end_x_right, 2)
        y_hammer_right = np.linspace(tip_y_right, end_y_right, 2)

        arc_end = np.arctan2(end_y_left, end_x_left)
        arc_start = np.arctan2(end_y_right, end_x_right)
        if arc_end < arc_start:
            arc_end += 2 * np.pi
        arc_theta = np.linspace(arc_end, arc_start, 20, endpoint=False)
        arc_radius = r_outer + hammerhead_length
        x_arc = arc_radius * np.cos(arc_theta)
        y_arc = arc_radius * np.sin(arc_theta)

        if cnc_milling:
            quarter_center_x = (
                r_inner * np.cos(q)
                - drill_bit_radius * np.sin(q)
                - slot_width_half * np.sin(q)
            )
            quarter_center_y = (
                r_inner * np.sin(q)
                + drill_bit_radius * np.cos(q)
                + slot_width_half * np.cos(q)
            )
            theta_quarter_end = np.linspace(q + np.pi+np.pi/(2*20), q + np.pi / 2, 10, endpoint=False)
            x_quarter_end = quarter_center_x - (drill_bit_radius * np.sin(theta_quarter_end))
            y_quarter_end = quarter_center_y + (drill_bit_radius * np.cos(theta_quarter_end))

        if cnc_milling:
            arc_start = np.arctan2(y_quarter_end[-1], x_quarter_end[-1])
            q_next = np.deg2rad((slot_idx + 1) * (360 / num_slots))
            quarter_center_x = (
                r_inner * np.cos(q_next)
                + drill_bit_radius * np.sin(q_next)
                + slot_width_half * np.sin(q_next)
            )
            quarter_center_y = (
                r_inner * np.sin(q_next)
                - drill_bit_radius * np.cos(q_next)
                - slot_width_half * np.cos(q_next)
            )
            next_x = quarter_center_x - (drill_bit_radius * np.sin(q_next))
            next_y = quarter_center_y + (drill_bit_radius * np.cos(q_next))
            arc_end = np.arctan2(next_y, next_x)
        else:
            arc_start = np.arctan2(y_left[0], x_left[0])
            q_next = np.deg2rad((slot_idx + 1) * (360 / num_slots))
            x_next = r_inner * np.cos(q_next) + slot_width_half * np.sin(q_next)
            y_next = r_inner * np.sin(q_next) - slot_width_half * np.cos(q_next)
            arc_end = np.arctan2(y_next, x_next)
        if arc_end < arc_start:
            arc_end += 2 * np.pi
        theta_inner = np.linspace(arc_start + (arc_end - arc_start) / 5, arc_end, 5, endpoint=False)
        inner_radius = (r_inner - drill_bit_radius / 2) if cnc_milling else r_inner
        x_inner = inner_radius * np.cos(theta_inner)
        y_inner = inner_radius * np.sin(theta_inner)

        if cnc_milling:
            x_slot.extend(x_right)
            x_slot.extend(x_half_right)
            x_slot.extend(x_hammer_right)
            x_slot.extend(x_arc[::-1])
            x_slot.extend(x_hammer_left[::-1])
            x_slot.extend(x_half_left)
            x_slot.extend(x_left[::-1])
            x_slot.extend(x_quarter_end)
            y_slot.extend(y_right)
            y_slot.extend(y_half_right)
            y_slot.extend(y_hammer_right)
            y_slot.extend(y_arc[::-1])
            y_slot.extend(y_hammer_left[::-1])
            y_slot.extend(y_half_left)
            y_slot.extend(y_left[::-1])
            y_slot.extend(y_quarter_end)
        else:
            x_slot.extend(x_right)
            x_slot.extend(x_hammer_right)
            x_slot.extend(x_arc[::-1])
            x_slot.extend(x_hammer_left[::-1])
            x_slot.extend(x_left[::-1])
            x_slot.extend(x_inner)
            y_slot.extend(y_right)
            y_slot.extend(y_hammer_right)
            y_slot.extend(y_arc[::-1])
            y_slot.extend(y_hammer_left[::-1])
            y_slot.extend(y_left[::-1])
            y_slot.extend(y_inner)

        return x_slot, y_slot

    def draw_stator_core(self, pixel_per_unit):
        """Draw the stator core with slots, supporting CNC milling."""
        num_slots = int(self.num_slots)
        slot_width_half = self.slot_width / 2
        hammerhead_width = self.hammerhead_width
        hammerhead_length = self.hammerhead_length
        r_inner = self.stator_inner_radius
        r_outer = (
            self.radius
            - self.air_gap
            - self.magnet_thickness
            - hammerhead_length
        )
        cnc_milling = self.cnc_milling
        drill_bit_radius = self.drill_bit_diameter / 2 if cnc_milling else 0
        pen_width = 2
        pen = pg.mkPen("#000000", width=pen_width)
        all_x, all_y = [], []

        for slot_idx in range(num_slots):
            x_slot, y_slot = self._calculate_slot_points(
                slot_idx,
                num_slots,
                slot_width_half,
                hammerhead_width,
                hammerhead_length,
                r_inner,
                r_outer,
                cnc_milling,
                drill_bit_radius,
            )
            all_x.extend(x_slot)
            all_y.extend(y_slot)

        all_x.append(all_x[0])
        all_y.append(all_y[0])
        self.plot_widget.plot(np.array(all_x), np.array(all_y), pen=pen)

    # endregion Stator

    # region Wires
    def draw_wires(self, pixel_per_unit):
        """Draw the wires in the stator slots as lines between left and right vectors."""
        wire_awg = self.wire_awg
        L = self.hammerhead_length
        r_inner = self.stator_inner_radius
        r_outer = self.radius - self.air_gap - self.magnet_thickness - L
        num_turns = int(self.num_turns_per_slot)
        #turns_list = self.params["turns_per_layer_list"]
        turns_list=None
        N = int(self.num_slots)
        tight_pack = self.tight_pack
        G = self.slot_width / 2
        collision_check_diameter = wire_awg
        if self.needle_winding:
            collision_check_diameter += self.needle_winder_diameter/2

        # Pens for drawing
        pen_width = wire_awg / pixel_per_unit
        non_colliding_pen = pg.mkPen('#B87333', width=pen_width, cap=pg.QtCore.Qt.RoundCap)
        colliding_pen = pg.mkPen('#FF0000', width=pen_width, cap=pg.QtCore.Qt.RoundCap)
        needle_pen = pg.mkPen('#ca5cdd', width=self.needle_winder_diameter/pixel_per_unit, cap=pg.QtCore.Qt.RoundCap)
        min_needle_rad = None
        max_needle_rad = self.radius - self.magnet_thickness

        good_x, good_y = [], []
        bad_x, bad_y = [], []
        needle_x, needle_y = [], []

        for i in range(N):
            q = i * (360.0 / N) / 180.0 * np.pi

            # Define bin positions for loose and tight packing
            # len(bin_counts) also determines turns per layer
            if tight_pack:
                # Two sets of bins for hexagonal packing
                bin_radii_even = np.arange(r_inner, r_outer, wire_awg)
                bin_radii_odd = np.arange( r_inner + (wire_awg / 2), r_outer, wire_awg)
                bin_counts_even = [0]*len(bin_radii_even)
                bin_counts_odd = [0]*len(bin_radii_odd)
                current_bin = len(bin_counts_even) - 1
            else:
                bin_radii = np.arange(r_inner, r_outer, wire_awg)
                #print(bin_radii)
                bin_counts = [0]*len(bin_radii)
                current_bin = len(bin_counts) - 1

            current_layer = 0
            if turns_list is None:
                turns_list = [[current_bin]]
                turn = 0
                while turn<num_turns:
                    #print(turn)
                    #print(current_bin)
                    #todo: add the wire winding tool end diameter to this to ensure it can fit and winding is possible
                    #  add it as another parameter that can be edited in the ui
                    if tight_pack:
                        if current_layer%2==0:
                            total_height = wire_awg*int((current_layer+1)/2) * np.sqrt(3) + collision_check_diameter
                        else:
                            total_height = wire_awg*(int((current_layer+1)/2)-1) * np.sqrt(3) + wire_awg*(np.sqrt(3) / 2) + collision_check_diameter
                    else:
                        total_height = (current_layer) * wire_awg + collision_check_diameter
                    G_adjusted = G + total_height

                    r=0
                    if tight_pack:
                        if current_layer%2==0:
                            r = bin_radii_even[current_bin]
                        else:
                            r = bin_radii_odd[current_bin]
                    else:
                        r = bin_radii[current_bin]

                    # Wire end positions
                    x_left = r * np.cos(0) - G_adjusted * np.sin(0)
                    y_left = r * np.sin(0) + G_adjusted * np.cos(0)
                    x_right = r * np.cos(0) + G_adjusted * np.sin(0)
                    y_right = r * np.sin(0) - G_adjusted * np.cos(0)

                    # Collision detection with slot boundaries
                    theta_left = (-0.5) * (360 / N) / 180 * np.pi
                    theta_right = (0.5) * (360 / N) / 180 * np.pi

                    # Calculate angles of wire ends
                    angle_left = np.arctan2(y_left, x_left)
                    angle_right = np.arctan2(y_right, x_right)

                    # Check if wire (with thickness) crosses boundaries
                    min_angle = min(angle_left, angle_right)
                    max_angle = max(angle_left, angle_right)
                    is_colliding = (min_angle < theta_left < max_angle) or (min_angle < theta_right < max_angle)

                    if is_colliding:
                        #print('is_colliding')
                        #print(min_angle / np.pi * 180, max_angle / np.pi * 180, theta_left / np.pi * 180,
                        #      theta_right / np.pi * 180)
                        if current_layer%2!=0:
                            turns_list[-1][0] = current_bin+1  # postpone start for odd going back
                        turn-=1

                    if current_layer%2==0:
                        current_bin-=1
                        if current_bin<0 or is_colliding:
                            current_layer+=1
                            # corresponding next position in both packing methods should be equal to our prev position:
                            current_bin+=1
                            if is_colliding:
                                turns_list[-1].append(current_bin)
                                turns_list.append([current_bin + 1])
                            else:
                                turns_list[-1].append(current_bin-1)
                                turns_list.append([current_bin])
                    else:
                        # don't check is_colliding here. We want to keep going out until there's room
                        current_bin+=1
                        if tight_pack:
                            if current_bin>=len(bin_counts_odd):
                                # corresponding next position in odd layer should be one behind our prev position:
                                current_bin -= 1
                                current_layer += 1
                                if current_bin >= len(bin_counts_odd) or is_colliding:
                                    break  # Todo: add warning here: not possible to wind anymore
                                turns_list[-1].append(current_bin+1)
                                turns_list.append([len(bin_counts_even)-1])  # even has different start
                        else:
                            if current_bin >= len(bin_counts):
                                current_bin -= 1
                                #if is_colliding:
                                #    current_bin -= 1
                                current_layer += 1
                                if current_bin >= len(bin_counts) or is_colliding:
                                    break  # Todo: add warning here: not possible to wind anymore
                                turns_list[-1].append(current_bin+1)
                                turns_list.append([current_bin])
                    turn+=1
                if current_layer%2==0:
                    turns_list[-1].append(current_bin)  # set at end of loop, iterated at start, so no plus/minus
                else:
                    turns_list[-1].append(current_bin)
                self.turns_per_layer_input.setText(str(turns_list))
            #print(turns_list)
            current_layer = 0
            for turn_tuple in turns_list:
                for turn in traverse_tuple(turn_tuple):
                    if tight_pack:
                        if current_layer % 2 == 0:
                            bin_counts_even[turn] += 1
                        else:
                            bin_counts_odd[turn] += 1
                    else:
                        bin_counts[turn] += 1
                current_layer +=1
            #print(bin_counts)
            if tight_pack:
                for r, bc in zip(bin_radii_even, bin_counts_even):
                    if bc==0:
                        continue
                    total_height = wire_awg*(bc-1)*np.sqrt(3)+collision_check_diameter

                    G_adjusted = G + total_height
                    # Wire end positions
                    x_left = r * np.cos(0) - G_adjusted * np.sin(0)
                    y_left = r * np.sin(0) + G_adjusted * np.cos(0)
                    x_right = r * np.cos(0) + G_adjusted * np.sin(0)
                    y_right = r * np.sin(0) - G_adjusted * np.cos(0)

                    if min_needle_rad is None or r<min_needle_rad:
                        # needle radius matches where needle has to be to pull wire around stator
                        # it is not the actual radius along the stator, or where the wire is
                        # it is specifically this collision radius
                        min_needle_rad = np.sqrt(x_left**2+y_left**2)

                    # Collision detection with slot boundaries
                    theta_left = (-0.5) * (360 / N) / 180 * np.pi
                    theta_right = (0.5) * (360 / N) / 180 * np.pi

                    # Calculate angles of wire ends
                    angle_left = np.arctan2(y_left, x_left)
                    angle_right = np.arctan2(y_right, x_right)

                    # Check if wire (with thickness) crosses boundaries
                    min_angle = min(angle_left, angle_right)
                    max_angle = max(angle_left, angle_right)
                    is_colliding = (min_angle < theta_left < max_angle) or (min_angle < theta_right < max_angle)

                    # reset to actual positions
                    middle_height = wire_awg*(bc-1)*np.sqrt(3)+wire_awg*.5
                    G_adjusted = G + middle_height
                    x_left = r * np.cos(q) - G_adjusted * np.sin(q)
                    y_left = r * np.sin(q) + G_adjusted * np.cos(q)
                    x_right = r * np.cos(q) + G_adjusted * np.sin(q)
                    y_right = r * np.sin(q) - G_adjusted * np.cos(q)

                    if not is_colliding:
                        good_x.extend([x_left, x_right, np.nan])
                        good_y.extend([y_left, y_right, np.nan])
                    else:
                        #print('is_colliding1')
                        bad_x.extend([x_left, x_right, np.nan])
                        bad_y.extend([y_left, y_right, np.nan])
                for r, bc in zip(bin_radii_odd, bin_counts_odd):
                    if bc==0:
                        continue

                    total_height = wire_awg*(bc - 1) * np.sqrt(3) + wire_awg*(np.sqrt(3)/2) + collision_check_diameter

                    G_adjusted = G + total_height
                    # Wire end positions
                    x_left = r * np.cos(0) - G_adjusted * np.sin(0)
                    y_left = r * np.sin(0) + G_adjusted * np.cos(0)
                    x_right = r * np.cos(0) + G_adjusted * np.sin(0)
                    y_right = r * np.sin(0) - G_adjusted * np.cos(0)

                    if min_needle_rad is None or r<min_needle_rad:
                        # needle radius matches where needle has to be to pull wire around stator
                        # it is not the actual radius along the stator, or where the wire is
                        # it is specifically this collision radius
                        min_needle_rad = np.sqrt(x_left**2+y_left**2)

                    # Collision detection with slot boundaries
                    theta_left = (-0.5) * (360 / N) / 180 * np.pi
                    theta_right = (0.5) * (360 / N) / 180 * np.pi

                    # Calculate angles of wire ends
                    angle_left = np.arctan2(y_left, x_left)
                    angle_right = np.arctan2(y_right, x_right)

                    # Check if wire (with thickness) crosses boundaries
                    min_angle = min(angle_left, angle_right)
                    max_angle = max(angle_left, angle_right)
                    is_colliding = (min_angle < theta_left < max_angle) or (min_angle < theta_right < max_angle)

                    # reset to actual positions
                    middle_height = wire_awg*(bc - 1) * np.sqrt(3) + wire_awg * (0.5 + np.sqrt(3) / 2)
                    G_adjusted = G + middle_height
                    x_left = r * np.cos(q) - G_adjusted * np.sin(q)
                    y_left = r * np.sin(q) + G_adjusted * np.cos(q)
                    x_right = r * np.cos(q) + G_adjusted * np.sin(q)
                    y_right = r * np.sin(q) - G_adjusted * np.cos(q)

                    if not is_colliding:
                        good_x.extend([x_left, x_right, np.nan])
                        good_y.extend([y_left, y_right, np.nan])
                    else:
                        #print('is_colliding2')
                        bad_x.extend([x_left, x_right, np.nan])
                        bad_y.extend([y_left, y_right, np.nan])
            else:
                for r, bc in zip(bin_radii, bin_counts):
                    if bc==0:
                        continue
                    total_height = (bc-1)*wire_awg + collision_check_diameter
                    G_adjusted = G + total_height
                    # Wire end positions
                    x_left = r * np.cos(0) - G_adjusted * np.sin(0)
                    y_left = r * np.sin(0) + G_adjusted * np.cos(0)
                    x_right = r * np.cos(0) + G_adjusted * np.sin(0)
                    y_right = r * np.sin(0) - G_adjusted * np.cos(0)

                    if min_needle_rad is None or r<min_needle_rad:
                        # needle radius matches where needle has to be to pull wire around stator
                        # it is not the actual radius along the stator, or where the wire is
                        # it is specifically this collision radius
                        min_needle_rad = np.sqrt(x_left**2+y_left**2)

                    # Collision detection with slot boundaries
                    theta_left = (-0.5) * (360 / N) / 180 * np.pi
                    theta_right = (0.5) * (360 / N) / 180 * np.pi

                    # Calculate angles of wire ends
                    angle_left = np.arctan2(y_left, x_left)
                    angle_right = np.arctan2(y_right, x_right)

                    # Check if wire (with thickness) crosses boundaries
                    min_angle = min(angle_left, angle_right)
                    max_angle = max(angle_left, angle_right)
                    is_colliding = (min_angle < theta_left < max_angle) or (min_angle < theta_right < max_angle)

                    # reset to actual positions
                    middle_height = (bc - 1) * wire_awg + wire_awg / 2
                    G_adjusted = G + middle_height
                    x_left = r * np.cos(q) - G_adjusted * np.sin(q)
                    y_left = r * np.sin(q) + G_adjusted * np.cos(q)
                    x_right = r * np.cos(q) + G_adjusted * np.sin(q)
                    y_right = r * np.sin(q) - G_adjusted * np.cos(q)

                    if not is_colliding:
                        good_x.extend([x_left, x_right, np.nan])
                        good_y.extend([y_left, y_right, np.nan])
                    else:
                        #print('is_colliding2')
                        #print(min_angle / np.pi * 180, max_angle / np.pi * 180, theta_left / np.pi * 180,
                        #      theta_right / np.pi * 180)
                        bad_x.extend([x_left, x_right, np.nan])
                        bad_y.extend([y_left, y_right, np.nan])
            q_half = (i+.5) * (360.0 / N) / 180.0 * np.pi
            needle_x.extend([max_needle_rad*np.cos(q_half), min_needle_rad*np.cos(q_half), np.nan])
            needle_y.extend([max_needle_rad*np.sin(q_half), min_needle_rad*np.sin(q_half), np.nan])

        self.plot_widget.plot(good_x, good_y, pen=non_colliding_pen)
        self.plot_widget.plot(bad_x, bad_y, pen=colliding_pen)
        if self.needle_winding:
            self.plot_widget.plot(needle_x, needle_y, pen=needle_pen)


    # endregion Wires


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BLDCWindow()
    window.show()
    sys.exit(app.exec_())