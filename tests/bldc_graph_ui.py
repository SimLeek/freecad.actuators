import sys
import numpy as np
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QDoubleSpinBox, QLabel
from PySide2.QtCore import Qt, Signal
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
        main_layout.addWidget(control_widget, 1)

        # BLDC parameters with spinboxes (slot_arc_length in degrees now)
        self.params = {
            "radius": 100.0,  # Outer radius of stator
            "num_slots": 12.0,  # Number of stator slots
            "num_magnets": 10.0,  # Number of magnets
            "slot_arc_length": 15.0,  # Arc length of each slot in degrees
            "air_gap": 5.0,  # Distance between stator and magnets
            "axle_radius": 15.0,  # Radius of the axle circle
            "stator_inner_radius": 20.0,  # Radius of the axle circle
            "magnet_thickness": 3.0,  # Thickness of magnets
            "wire_awg": 1.0,  # Wire diameter in mm
            "num_turns_per_slot": 4.0,  # Number of wire turns per slot
            "outrunner_thickness": 5.0  # Thickness of the outrunner
        }

        # Create spinboxes for each parameter
        self.spinboxes = {}
        for param, value in self.params.items():
            label = QLabel(param.replace("_", " ").title())
            control_layout.addWidget(label)
            spinbox = QDoubleSpinBox()
            spinbox.setDecimals(2)
            spinbox.setSingleStep(1.0)
            if param in ["num_slots", "num_magnets", "num_turns_per_slot"]:
                spinbox.setDecimals(0)
                spinbox.setRange(4, 50)
            elif param == "slot_arc_length":
                spinbox.setDecimals(2)
                spinbox.setRange(5, 30)  # Reasonable range for degrees
                spinbox.setSingleStep(1.0)
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
            else:  # radius
                spinbox.setRange(50, 200)
            spinbox.setValue(value)
            spinbox.valueChanged.connect(self.update_visualization)
            control_layout.addWidget(spinbox)
            self.spinboxes[param] = spinbox

        # Connect range changed signal to update visualization
        self.plot_widget.sigRangeChanged.connect(self.update_visualization)

        # Initial draw
        self.update_visualization()

    def update_visualization(self):
        """Update the visualization based on current parameter values."""
        # Update parameters from spinboxes
        for param, spinbox in self.spinboxes.items():
            self.params[param] = spinbox.value()

        # Clear the plot widget
        self.plot_widget.clear()

        # Calculate pixel scale (pixels per data unit)
        view_range = self.plot_widget.getViewBox().viewRange()
        plot_size = self.plot_widget.size()
        x_scale = (view_range[0][1] - view_range[0][0]) / plot_size.width()  # Data units per pixel in x
        y_scale = (view_range[1][1] - view_range[1][0]) / plot_size.height()  # Data units per pixel in y
        pixel_per_unit = min(x_scale, y_scale)  # Use the smaller scale for consistency

        # Draw components with scaled pen widths
        self.draw_axle(pixel_per_unit)
        self.draw_stator_core(pixel_per_unit)
        self.draw_wires(pixel_per_unit)
        self.draw_magnets(pixel_per_unit)
        self.draw_outrunner(pixel_per_unit)

    def draw_axle(self, pixel_per_unit):
        """Draw the central axle circle."""
        theta = np.linspace(0, 2 * np.pi, 60)
        x = self.params["axle_radius"] * np.cos(theta)
        y = self.params["axle_radius"] * np.sin(theta)
        x = np.append(x, x[0])
        y = np.append(y, y[0])
        pen_width = 2 / pixel_per_unit  # Convert desired width (2 units) to pixels
        self.plot_widget.plot(x, y, pen=pg.mkPen('#000000', width=pen_width))

    def draw_stator_core(self, pixel_per_unit):
        """Draw the stator core with slots as square-wave-like shapes."""
        stator_radius = self.params["radius"] - self.params["air_gap"] - self.params["magnet_thickness"]
        inner_radius = self.params["stator_inner_radius"]
        slot_angle_step = 360.0 / self.params["num_slots"]  # In degrees
        slot_arc_length_rad = np.deg2rad(self.params["slot_arc_length"])  # Convert degrees to radians

        # Initialize arrays to store all x and y coordinates
        all_x = []
        all_y = []
        pen_width = 1 / pixel_per_unit  # Convert desired width (1 unit) to pixels
        pen = pg.mkPen('#000000', width=pen_width)

        for i in range(int(self.params["num_slots"])):
            slot_angle = i * slot_angle_step  # In degrees
            slot_start_angle_rad = np.deg2rad(slot_angle)
            slot_end_angle_rad = np.deg2rad(slot_angle + self.params["slot_arc_length"])
            slot_next_angle_rad = np.deg2rad((i + 1) * slot_angle_step)

            # Rising edge (left side)
            theta_rise = np.array([slot_start_angle_rad, slot_start_angle_rad])
            x_rise = np.array([inner_radius, stator_radius]) * np.cos(theta_rise)
            y_rise = np.array([inner_radius, stator_radius]) * np.sin(theta_rise)
            all_x.extend(x_rise)
            all_y.extend(y_rise)

            # Top part (outermost diameter arc)
            theta_top = np.linspace(slot_start_angle_rad, slot_end_angle_rad, 20)
            x_top = stator_radius * np.cos(theta_top)
            y_top = stator_radius * np.sin(theta_top)
            all_x.extend(x_top)
            all_y.extend(y_top)
            #all_x.append(x_top[0])  # Close the arc
            #all_y.append(y_top[0])

            # Falling edge (right side)
            theta_fall = np.array([slot_end_angle_rad, slot_end_angle_rad])
            x_fall = np.array([stator_radius, inner_radius]) * np.cos(theta_fall)
            y_fall = np.array([stator_radius, inner_radius]) * np.sin(theta_fall)
            all_x.extend(x_fall)
            all_y.extend(y_fall)

            # Low part (innermost diameter arc)
            theta_low = np.linspace(slot_end_angle_rad, slot_next_angle_rad, 20, endpoint=False)
            x_low = inner_radius * np.cos(theta_low)
            y_low = inner_radius * np.sin(theta_low)
            all_x.extend(x_low)
            all_y.extend(y_low)
            #all_x.append(x_low[0])  # Close the arc
            #all_y.append(y_low[0])

        # Plot all segments in one call
        self.plot_widget.plot(np.array(all_x), np.array(all_y), pen=pen)

    def draw_wires(self, pixel_per_unit):
        """Draw the wires in the stator slots as arc segments."""
        stator_radius = self.params["radius"] - self.params["air_gap"] - self.params["magnet_thickness"]
        wire_diameter = self.params["wire_awg"]  # In mm
        slot_length = stator_radius - self.params["stator_inner_radius"]  # Radial length in mm
        max_turns_in_slot = int(slot_length / wire_diameter)  # Max turns that fit in one layer
        num_turns = int(self.params["num_turns_per_slot"])
        slot_arc_length_rad = np.deg2rad(self.params["slot_arc_length"])  # Convert degrees to radians

        # Initialize arrays to store all x and y coordinates
        all_x = []
        all_y = []
        pen_width = wire_diameter / pixel_per_unit  # Scale wire_awg to pixels
        pen = pg.mkPen('#B87333', width=pen_width)
        pen.setCapStyle(pg.QtCore.Qt.PenCapStyle.RoundCap)

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
                all_x.extend(x_wire)
                all_y.extend(y_wire)
                all_x.append(float('inf'))
                all_y.append(float('inf'))

        # Plot all wire segments in one call
        self.plot_widget.plot(np.array(all_x), np.array(all_y), pen=pen)

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
            # Inner arc (toward stator)
            x_inner = magnet_inner_radius * np.cos(theta_magnet)
            y_inner = magnet_inner_radius * np.sin(theta_magnet)
            # Outer arc (at rotor radius)
            x_outer = magnet_outer_radius * np.cos(theta_magnet[::-1])
            y_outer = magnet_outer_radius * np.sin(theta_magnet[::-1])
            # Combine to form a closed shape
            x_magnet = np.concatenate([x_inner, x_outer])
            y_magnet = np.concatenate([y_inner, y_outer])
            x_magnet = np.append(x_magnet, x_magnet[0])
            y_magnet = np.append(y_magnet, y_magnet[0])
            pen_width = 1 / pixel_per_unit  # Convert desired width (1 unit) to pixels
            self.plot_widget.plot(x_magnet, y_magnet, pen=pg.mkPen('#C0C0C0', width=pen_width))  # Silver

    def draw_outrunner(self, pixel_per_unit):
        """Draw the outrunner circles with editable thickness."""
        theta = np.linspace(0, 2 * np.pi, 200)
        inner_radius = self.params["radius"]
        x_inner = inner_radius * np.cos(theta)
        y_inner = inner_radius * np.sin(theta)
        x_inner = np.append(x_inner, x_inner[0])
        y_inner = np.append(y_inner, y_inner[0])
        pen_width = 2 / pixel_per_unit  # Convert desired width (2 units) to pixels
        self.plot_widget.plot(x_inner, y_inner, pen=pg.mkPen('#808080', width=pen_width))  # Gray

        outer_radius = inner_radius + self.params["outrunner_thickness"]
        x_outer = outer_radius * np.cos(theta)
        y_outer = outer_radius * np.sin(theta)
        x_outer = np.append(x_outer, x_outer[0])
        y_outer = np.append(y_outer, y_outer[0])
        self.plot_widget.plot(x_outer, y_outer, pen=pg.mkPen('#808080', width=pen_width))  # Gray

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BLDCWindow()
    window.show()
    sys.exit(app.exec_())