import sys
import numpy as np
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QDoubleSpinBox, QLabel, \
    QLineEdit, QCheckBox
from PySide2.QtCore import Qt
import pyqtgraph as pg


class BLDCWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BLDC Motor Stator Visualization")
        self.setGeometry(100, 100, 1000, 800)

        # Main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        main_layout = QHBoxLayout(self.main_widget)

        # Plot widget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setAspectLocked(True)
        self.plot_widget.setRange(xRange=[-150, 150], yRange=[-150, 150])
        self.plot_widget.setBackground('w')
        main_layout.addWidget(self.plot_widget, 3)

        # Control panel for parameters
        control_widget = QWidget()
        control_layout = QVBoxLayout(control_widget)
        main_layout.addWidget(control_widget, 3)

        # BLDC parameters with spinboxes
        self.params = {
            "radius": 100.0,
            "num_slots": 12.0,
            "num_magnets": 10.0,
            "slot_arc_length": 15.0,
            "slot_width": 10.0,
            "hammerhead_width": 2.0,
            "hammerhead_length": 2.0,
            "air_gap": 5.0,
            "axle_radius": 15.0,
            "stator_inner_radius": 20.0,
            "magnet_thickness": 3.0,
            "wire_awg": 1.0,
            "num_turns_per_slot": 4.0,
            "outrunner_thickness": 5.0,
            "tight_pack": False,  # Default: tight packing off
            "fast_display": False,  # Default: fast display off
            "cnc_milling": False,  # Default: CNC milling off
            "drill_bit_diameter": 2.0  # Default drill bit diameter
        }

        # Create spinboxes for each parameter
        self.spinboxes = {}
        for param, value in self.params.items():
            if param in ["tight_pack", "fast_display", "cnc_milling"]:
                continue  # These will be checkboxes
            label = QLabel(param.replace("_", " ").title())
            control_layout.addWidget(label)
            spinbox = QDoubleSpinBox()
            spinbox.setDecimals(2)
            spinbox.setSingleStep(1.0)
            if param in ["num_slots", "num_magnets", "num_turns_per_slot"]:
                spinbox.setDecimals(0)
                spinbox.setRange(4, 1000000)  # Allow high turn counts
            elif param == "slot_arc_length":
                spinbox.setRange(5, 30)
            elif param == "air_gap":
                spinbox.setRange(1, 20)
            elif param in ["axle_radius", "stator_inner_radius"]:
                spinbox.setRange(5, 50)
            elif param == "magnet_thickness":
                spinbox.setRange(1, 10)
            elif param == "wire_awg":
                spinbox.setDecimals(2)
                spinbox.setRange(0.5, 5.0)
                spinbox.setSingleStep(0.1)
            elif param == "outrunner_thickness":
                spinbox.setRange(2, 15)
            elif param == "slot_width":
                spinbox.setRange(1, 30)
            elif param == "hammerhead_length":
                spinbox.setRange(0.5, 20.0)
            elif param == "hammerhead_width":
                spinbox.setRange(0.5, 20.0)
            elif param == "drill_bit_diameter":
                spinbox.setRange(0.5, 10.0)  # Reasonable range for drill bit diameter
            else:  # radius
                spinbox.setRange(50, 200)
            spinbox.setValue(value)
            spinbox.valueChanged.connect(self.update_visualization)
            control_layout.addWidget(spinbox)
            self.spinboxes[param] = spinbox

        # Add QLineEdit for max turns per layer
        self.max_turns_input = QLineEdit()
        self.max_turns_input.setPlaceholderText("Max turns per layer (e.g., 5,4,3)")
        control_layout.addWidget(QLabel("Max Turns per Layer"))
        control_layout.addWidget(self.max_turns_input)
        self.max_turns_input.editingFinished.connect(self.update_visualization)

        # Add Tight Pack checkbox
        self.tight_pack_checkbox = QCheckBox("Tight Pack (Hexagonal)")
        self.tight_pack_checkbox.setChecked(False)
        self.tight_pack_checkbox.stateChanged.connect(self.update_visualization)
        control_layout.addWidget(self.tight_pack_checkbox)

        # Add Fast Display checkbox
        self.fast_display_checkbox = QCheckBox("Fast Display")
        self.fast_display_checkbox.setChecked(False)
        self.fast_display_checkbox.stateChanged.connect(self.update_visualization)
        control_layout.addWidget(self.fast_display_checkbox)

        # Add CNC Milling checkbox
        self.cnc_milling_checkbox = QCheckBox("CNC Milling")
        self.cnc_milling_checkbox.setChecked(False)
        self.cnc_milling_checkbox.stateChanged.connect(self.update_visualization)
        control_layout.addWidget(self.cnc_milling_checkbox)

        # Connect range changed signal to update visualization
        self.plot_widget.sigRangeChanged.connect(self.update_visualization_with_cache)
        self.use_cache = False

        # Initial draw
        self.update_visualization()

    def update_visualization_with_cache(self):
        self.use_cache = True
        self.update_visualization()
        self.use_cache = False

    def update_visualization(self):
        """Update the visualization based on current parameter values."""
        # Update parameters from spinboxes
        for param, spinbox in self.spinboxes.items():
            self.params[param] = spinbox.value()

        # Update tight pack, fast display, and CNC milling settings
        self.params["tight_pack"] = self.tight_pack_checkbox.isChecked()
        self.params["fast_display"] = self.fast_display_checkbox.isChecked()
        self.params["cnc_milling"] = self.cnc_milling_checkbox.isChecked()

        # Parse max_turns_per_layer_list from QLineEdit
        max_turns_text = self.max_turns_input.text()
        if max_turns_text:
            try:
                self.params["max_turns_per_layer_list"] = [int(x) for x in max_turns_text.split(',')]
            except ValueError:
                self.params["max_turns_per_layer_list"] = None
        else:
            self.params["max_turns_per_layer_list"] = None

        # Clear the plot widget
        self.plot_widget.clear()

        # Calculate pixel scale (pixels per data unit)
        view_range = self.plot_widget.getViewBox().viewRange()
        plot_size = self.plot_widget.size()
        x_scale = (view_range[0][1] - view_range[0][0]) / plot_size.width()
        y_scale = (view_range[1][1] - view_range[1][0]) / plot_size.height()
        pixel_per_unit = min(x_scale, y_scale)

        # Draw components with scaled pen widths
        #self.draw_axle(pixel_per_unit)
        self.draw_stator_core(pixel_per_unit)
        #self.draw_wires(pixel_per_unit)
        #self.draw_magnets(pixel_per_unit)
        #self.draw_outrunner(pixel_per_unit)

    def draw_axle(self, pixel_per_unit):
        """Draw the central axle circle."""
        theta = np.linspace(0, 2 * np.pi, 60)
        x = self.params["axle_radius"] * np.cos(theta)
        y = self.params["axle_radius"] * np.sin(theta)
        x = np.append(x, x[0])
        y = np.append(y, y[0])
        pen_width = 2 / pixel_per_unit
        self.plot_widget.plot(x, y, pen=pg.mkPen('#000000', width=pen_width))

    def draw_stator_core(self, pixel_per_unit):
        """Draw the stator core using parametric equations for each slot with CNC milling support."""
        import numpy as np
        import pyqtgraph as pg

        # Parameters
        N = int(self.params["num_slots"])
        G = self.params["slot_width"] / 2  # half thickness
        W = self.params["hammerhead_width"]
        L = self.params["hammerhead_length"]
        r_inner = self.params["stator_inner_radius"]
        r_outer = self.params["radius"] - self.params["air_gap"] - self.params["magnet_thickness"] - L
        cnc_milling = self.params["cnc_milling"]
        drill_bit_radius = self.params["drill_bit_diameter"] / 2 if cnc_milling else 0
        adjusted_r_inner = r_inner - drill_bit_radius if cnc_milling else r_inner

        #pen_width = 1 / pixel_per_unit
        pen_width = 1
        pen = pg.mkPen('#000000', width=pen_width)

        all_x, all_y = [], []

        for i in range(N):
            q = (i * (360 / N)) / 180 * np.pi  # centerline angle of this slot

            # Quarter-circles at slot ends (before slot geometry) if CNC milling
            if cnc_milling:
                quarter_center_x = r_inner * np.cos(q) + drill_bit_radius * np.sin(q)+ G * np.sin(q)
                quarter_center_y = r_inner * np.sin(q) - drill_bit_radius * np.cos(q)- G * np.cos(q)
                theta_quarter_start = np.linspace(q+np.pi / 2, q, 10)
                x_quarter_start = quarter_center_x - (drill_bit_radius * np.sin(theta_quarter_start))
                y_quarter_start = quarter_center_y + (drill_bit_radius * np.cos(theta_quarter_start))

            # Radial vectors
            t_vals = np.linspace(r_inner, r_outer, 2)
            x_left = t_vals * np.cos(q) - G * np.sin(q)
            y_left = t_vals * np.sin(q) + G * np.cos(q)
            x_right = t_vals * np.cos(q) + G * np.sin(q)
            y_right = t_vals * np.sin(q) - G * np.cos(q)

            # Hammerhead ends with half-circles if CNC milling
            hammer_theta = np.arctan2(W + G, r_outer + L)
            sub_l = (W + G) * np.tan(hammer_theta)
            true_L = L - sub_l
            tip_x_left = r_outer * np.cos(q) - (W + G) * np.sin(q)
            tip_y_left = r_outer * np.sin(q) + (W + G) * np.cos(q)
            end_x_left = tip_x_left + true_L * np.cos(q)
            end_y_left = tip_y_left + true_L * np.sin(q)
            tip_x_right = r_outer * np.cos(q) + (W + G) * np.sin(q)
            tip_y_right = r_outer * np.sin(q) - (W + G) * np.cos(q)
            end_x_right = tip_x_right + true_L * np.cos(q)
            end_y_right = tip_y_right + true_L * np.sin(q)

            if cnc_milling:
                # Half-circle at left hammerhead transition
                half_center_x_left = x_left[-1] + drill_bit_radius * np.cos(q + np.pi / 2)
                half_center_y_left = y_left[-1] + drill_bit_radius * np.sin(q + np.pi / 2)
                theta_half_left = np.linspace(q+2*np.pi, q+np.pi,  15)
                x_half_left = half_center_x_left - (drill_bit_radius * np.sin(theta_half_left))
                y_half_left = half_center_y_left + (drill_bit_radius * np.cos(theta_half_left))

                # Half-circle at right hammerhead transition
                half_center_x_right = x_right[-1] - drill_bit_radius * np.cos(q + np.pi / 2)
                half_center_y_right = y_right[-1] - drill_bit_radius * np.sin(q + np.pi / 2)
                theta_half_right = np.linspace( q+2*np.pi, q+np.pi, 15)
                x_half_right = half_center_x_right - (drill_bit_radius * np.sin(theta_half_right))
                y_half_right = half_center_y_right + (drill_bit_radius * np.cos(theta_half_right))
            x_hammer_left = np.linspace(tip_x_left, end_x_left, 2)
            y_hammer_left = np.linspace(tip_y_left, end_y_left, 2)
            x_hammer_right = np.linspace(tip_x_right, end_x_right, 2)
            y_hammer_right = np.linspace(tip_y_right, end_y_right, 2)

            # Arc between hammerheads
            arc_end = np.arctan2(end_y_left, end_x_left)
            arc_start = np.arctan2(end_y_right, end_x_right)
            if arc_end < arc_start:
                arc_end += 2 * np.pi
            arc_theta = np.linspace(arc_end, arc_start, 20)
            arc_radius = r_outer + L
            x_arc = arc_radius * np.cos(arc_theta)
            y_arc = arc_radius * np.sin(arc_theta)

            # Quarter-circle at slot end (after inner arc) if CNC milling
            if cnc_milling:
                quarter_center_x = r_inner * np.cos(q) - drill_bit_radius * np.sin(q) - G * np.sin(q)
                quarter_center_y = r_inner * np.sin(q) + drill_bit_radius * np.cos(q) + G * np.cos(q)
                theta_quarter_end = np.linspace( q+np.pi, q+np.pi/2, 10)
                x_quarter_end = quarter_center_x - (drill_bit_radius * np.sin(theta_quarter_end))
                y_quarter_end = quarter_center_y + (drill_bit_radius * np.cos(theta_quarter_end))

            # Inner arc between slots
            if cnc_milling:
                arc_start = np.arctan2(y_quarter_end[-1], x_quarter_end[-1])
                q_next = np.deg2rad((i + 1) * (360 / N))  # centerline angle of next slot
#
                quarter_center_x = r_inner * np.cos(q_next) + drill_bit_radius * np.sin(q_next)+ G * np.sin(q_next)
                quarter_center_y = r_inner * np.sin(q_next) - drill_bit_radius * np.cos(q_next)- G * np.cos(q_next)
                next_x = quarter_center_x - (drill_bit_radius * np.sin(q_next)) # +np.pi/2))
                next_y = quarter_center_y + (drill_bit_radius * np.cos(q_next))
#
                arc_end = np.arctan2(next_y, next_x)
            else:
                arc_start = np.arctan2(y_left[0], x_left[0])
                q_next = np.deg2rad((i + 1) * (360 / N))  # centerline angle of next slot
                x_next = r_inner * np.cos(q_next) + G * np.sin(q_next)
                y_next = r_inner * np.sin(q_next) - G * np.cos(q_next)
                arc_end = np.arctan2(y_next, x_next)
#
            if arc_end < arc_start:
                arc_end += 2 * np.pi
            theta_inner = np.linspace(arc_start+(arc_end-arc_start)/5, arc_end, 5, endpoint=False)

            if cnc_milling:
                x_inner = (r_inner - drill_bit_radius / 2) * np.cos(theta_inner)
                y_inner = (r_inner - drill_bit_radius / 2) * np.sin(theta_inner)
            else:
                x_inner = r_inner * np.cos(theta_inner)
                y_inner = r_inner * np.sin(theta_inner)

            # Combine all points into a single counterclockwise polygon
            if cnc_milling:
                all_x.extend(x_quarter_start)
                all_x.extend(x_right)
                all_x.extend(x_half_right)
                all_x.extend(x_hammer_right)
                all_x.extend(x_arc[::-1])
                all_x.extend(x_hammer_left[::-1])
                all_x.extend(x_half_left)
                all_x.extend(x_left[::-1])
                all_y.extend(y_quarter_start)
                all_y.extend(y_right)
                all_y.extend(y_half_right)
                all_y.extend(y_hammer_right)
                all_y.extend(y_arc[::-1])
                all_y.extend(y_hammer_left[::-1])
                all_y.extend(y_half_left)
                all_y.extend(y_left[::-1])

                all_x.extend(x_quarter_end)
                all_y.extend(y_quarter_end)
                # currently not working with inner circles, and also not that important
                #all_x.extend(x_inner)
                #all_y.extend(y_inner)
            else:
                all_x.extend(x_right)
                all_x.extend(x_hammer_right)
                all_x.extend(x_arc[::-1])
                all_x.extend(x_hammer_left[::-1])
                all_x.extend(x_left[::-1])
                all_y.extend(y_right)
                all_y.extend(y_hammer_right)
                all_y.extend(y_arc[::-1])
                all_y.extend(y_hammer_left[::-1])
                all_y.extend(y_left[::-1])

                all_x.extend(x_inner)
                all_y.extend(y_inner)

        # Close polygon loop
        all_x.append(all_x[0])
        all_y.append(all_y[0])

        self.plot_widget.plot(np.array(all_x), np.array(all_y), pen=pen)

    def draw_wires(self, pixel_per_unit):
        """Draw the wires in the stator slots as arc segments."""
        stator_radius = self.params["radius"] - self.params["air_gap"] - self.params["magnet_thickness"]
        wire_diameter = self.params["wire_awg"]  # In mm
        slot_length = stator_radius - self.params["stator_inner_radius"]  # Radial length in mm
        max_turns_in_slot = int(slot_length / wire_diameter)  # Max turns that fit in one layer
        num_turns = int(self.params["num_turns_per_slot"])
        slot_arc_length_rad = np.deg2rad(self.params["slot_arc_length"])  # Convert degrees to radians
        tight_pack = self.params["tight_pack"]
        fast_display = self.params["fast_display"]

        max_turns_per_layer_list = self.params.get("max_turns_per_layer_list", None)

        pen_width = wire_diameter / pixel_per_unit  # Scale wire_awg to pixels
        non_colliding_pen = pg.mkPen('#B87333', width=pen_width)
        colliding_pen = pg.mkPen('#FF0000', width=pen_width)
        non_colliding_pen.setCapStyle(pg.QtCore.Qt.PenCapStyle.RoundCap)
        colliding_pen.setCapStyle(pg.QtCore.Qt.PenCapStyle.RoundCap)

        # Initialize arrays to store all x and y coordinates

        if not self.use_cache:
            self.all_x_non_colliding = []
            self.all_y_non_colliding = []
            self.all_x_colliding = []
            self.all_y_colliding = []
            # For hexagonal packing: theta shift = wire_diameter / 2 at reference radius
            theta_shift_factor = (np.sqrt(3) * wire_diameter) / 2 if tight_pack else wire_diameter
            for i in range(int(self.params["num_slots"])):
                slot_angle = i * (360.0 / self.params["num_slots"])
                slot_start_angle_rad = np.deg2rad(slot_angle)
                for j in range(int(min(num_turns, max_turns_in_slot))):
                    if max_turns_in_slot == 0:
                        max_turns_in_slot = 1
                    # num_layers here is the number of layers of wire
                    if j < num_turns % max_turns_in_slot:
                        num_layers = int(np.ceil(num_turns / max_turns_in_slot))
                    else:
                        num_layers = int(np.floor(num_turns / max_turns_in_slot))

                    # Adjust radial position for this layer
                    wire_arc_radius = stator_radius - j * wire_diameter - wire_diameter / 2.0
                    our_side_thickness = num_layers * wire_diameter
                    # Arc length in radians at this radius
                    start_angle = slot_start_angle_rad - our_side_thickness / wire_arc_radius
                    end_angle = slot_start_angle_rad + slot_arc_length_rad + our_side_thickness / wire_arc_radius
                    theta_wire = np.linspace(start_angle, end_angle, 20)
                    x_wire = wire_arc_radius * np.cos(theta_wire)
                    y_wire = wire_arc_radius * np.sin(theta_wire)
                    #all_x.extend(x_wire)
                    #all_y.extend(y_wire)
                    #all_x.append(float('inf'))
                    #all_y.append(float('inf'))

        # Plot all wire segments in one call
        #self.plot_widget.plot(np.array(all_x), np.array(all_y), pen=pen)

    def draw_magnets(self, pixel_per_unit):
        """Draw the magnets on the outrunner with thickness toward the stator."""
        magnet_outer_radius = self.params["radius"]
        magnet_inner_radius = magnet_outer_radius - self.params["magnet_thickness"]
        magnet_arc = 2 * np.pi / self.params["num_magnets"]
        for i in range(int(self.params["num_magnets"])):
            magnet_angle = i * (2 * np.pi / self.params["num_magnets"])
            start_angle = magnet_angle - magnet_arc / 3
            end_angle = magnet_angle + magnet_arc / 3
            theta_magnet = np.linspace(start_angle, end_angle, 20)
            x_inner = magnet_inner_radius * np.cos(theta_magnet)
            y_inner = magnet_inner_radius * np.sin(theta_magnet)
            x_outer = magnet_outer_radius * np.cos(theta_magnet[::-1])
            y_outer = magnet_outer_radius * np.sin(theta_magnet[::-1])
            x_magnet = np.concatenate([x_inner, x_outer])
            y_magnet = np.concatenate([y_inner, y_outer])
            x_magnet = np.append(x_magnet, x_magnet[0])
            y_magnet = np.append(y_magnet, y_magnet[0])
            pen_width = 1 / pixel_per_unit
            self.plot_widget.plot(x_magnet, y_magnet, pen=pg.mkPen('#C0C0C0', width=pen_width))

    def draw_outrunner(self, pixel_per_unit):
        """Draw the outrunner circles with editable thickness."""
        theta = np.linspace(0, 2 * np.pi, 200)
        inner_radius = self.params["radius"]
        x_inner = inner_radius * np.cos(theta)
        y_inner = inner_radius * np.sin(theta)
        x_inner = np.append(x_inner, x_inner[0])
        y_inner = np.append(y_inner, y_inner[0])
        pen_width = 2 / pixel_per_unit
        self.plot_widget.plot(x_inner, y_inner, pen=pg.mkPen('#808080', width=pen_width))

        outer_radius = inner_radius + self.params["outrunner_thickness"]
        x_outer = outer_radius * np.cos(theta)
        y_outer = outer_radius * np.sin(theta)
        x_outer = np.append(x_outer, x_outer[0])
        y_outer = np.append(y_outer, y_outer[0])
        self.plot_widget.plot(x_outer, y_outer, pen=pg.mkPen('#808080', width=pen_width))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BLDCWindow()
    window.show()
    sys.exit(app.exec_())