"""
UI and visualization management functions for the BLDC Motor Stator Visualization.
"""

# stop potential import loops
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_window import BLDCWindow
else:
    from typing import Any
    BLDCWindow = Any

def connect_display_checkboxes(bldc_window: BLDCWindow):
    """Create horizontal Display Options group at the top."""
    bldc_window.ui.display_stator_core_checkbox.setChecked(True)
    bldc_window.ui.display_stator_core_checkbox.stateChanged.connect(lambda: update_visualization(bldc_window))

    bldc_window.ui.display_wires_checkbox.setChecked(True)
    bldc_window.ui.display_wires_checkbox.stateChanged.connect(lambda: update_visualization(bldc_window))

    bldc_window.ui.display_magnets_checkbox.setChecked(True)
    bldc_window.ui.display_magnets_checkbox.stateChanged.connect(lambda: update_visualization(bldc_window))

    bldc_window.ui.display_outrunner_checkbox.setChecked(True)
    bldc_window.ui.display_outrunner_checkbox.stateChanged.connect(lambda: update_visualization(bldc_window))

    bldc_window.ui.display_bearing_checkbox.setChecked(True)
    bldc_window.ui.display_bearing_checkbox.stateChanged.connect(lambda: update_visualization(bldc_window))

    bldc_window.ui.display_height_checkbox.setChecked(True)
    bldc_window.ui.display_height_checkbox.stateChanged.connect(lambda: update_visualization(bldc_window))

def connect_display_and_parameters(bldc_window: BLDCWindow):
    """Create grouped UI elements for motor parameters."""
    # Plot widget
    #bldc_window.ui.stator_plot_widget = pg.PlotWidget()
    bldc_window.ui.stator_plot_widget.setAspectLocked(True)
    bldc_window.ui.stator_plot_widget.setRange(xRange=[-150, 150], yRange=[-150, 150])
    bldc_window.ui.stator_plot_widget.setBackground("w")
    #bldc_window.ui.stator_display_tab.addWidget(bldc_window.ui.stator_plot_widget, 3)

    # General Parameters Group
    bldc_window.ui.radius_lineedit.textChanged.connect(lambda: update_visualization(bldc_window))
    bldc_window.ui.num_slots_lineedit.textChanged.connect(lambda: update_visualization(bldc_window))
    bldc_window.ui.num_magnets_lineedit.textChanged.connect(lambda: update_visualization(bldc_window))
    bldc_window.ui.air_gap_lineedit.textChanged.connect(lambda: update_visualization(bldc_window))
    bldc_window.ui.axle_radius_lineedit.textChanged.connect(lambda: update_visualization(bldc_window))

    # Stator Group
    bldc_window.ui.slot_width_lineedit.textChanged.connect(lambda: update_visualization(bldc_window))
    bldc_window.ui.hammerhead_width_lineedit.textChanged.connect(lambda: update_visualization(bldc_window))
    bldc_window.ui.hammerhead_length_lineedit.textChanged.connect(lambda: update_visualization(bldc_window))
    bldc_window.ui.stator_inner_radius_lineedit.textChanged.connect(lambda: update_visualization(bldc_window))

    # Magnet and Outrunner Group
    bldc_window.ui.magnet_thickness_lineedit.textChanged.connect(lambda: update_visualization(bldc_window))
    bldc_window.ui.outrunner_thickness_lineedit.textChanged.connect(lambda: update_visualization(bldc_window))

    # Wire Group
    bldc_window.ui.wire_diameter_lineedit.textChanged.connect(lambda: update_visualization(bldc_window))
    bldc_window.ui.turns_per_slot_lineedit.textChanged.connect(lambda: update_visualization(bldc_window))
    bldc_window.ui.needle_diameter_lineedit.textChanged.connect(lambda: update_visualization(bldc_window))
    bldc_window.ui.turns_per_layer_lineedit.editingFinished.connect(lambda: update_visualization(bldc_window))
    bldc_window.ui.turns_per_layer_lineedit.setPlaceholderText("Turns per layer (e.g., [5,4,3])")
    bldc_window.ui.tight_pack_checkbox.stateChanged.connect(lambda: update_visualization(bldc_window))
    bldc_window.ui.needle_winding_checkbox.stateChanged.connect(lambda: update_visualization(bldc_window))

    # CNC Group
    bldc_window.ui.cnc_milling_checkbox.stateChanged.connect(lambda: update_visualization(bldc_window))
    bldc_window.ui.drill_bit_diameter_lineedit.textChanged.connect(lambda: update_visualization(bldc_window))

    print("connected")

def update_visualization(bldc_window: BLDCWindow):
    """Update the visualization based on current parameter values."""
    # Clear turns
    if not bldc_window.use_cache and not bldc_window.ui.turns_per_layer_lock.is_locked:
        bldc_window.ui.turns_per_layer_lineedit.setText("")

    # Clear plot
    bldc_window.ui.stator_plot_widget.clear()

    # Calculate pixel scale
    view_range = bldc_window.ui.stator_plot_widget.getViewBox().viewRange()
    plot_size = bldc_window.ui.stator_plot_widget.size()
    x_scale = (view_range[0][1] - view_range[0][0]) / plot_size.width()
    y_scale = (view_range[1][1] - view_range[1][0]) / plot_size.height()
    pixel_per_unit = min(x_scale, y_scale)

    # Draw components using callbacks
    if bldc_window.ui.display_axle_checkbox.isChecked():
        bldc_window.draw_axle_callback(bldc_window, pixel_per_unit)
    if bldc_window.ui.display_stator_core_checkbox.isChecked():
        bldc_window.draw_stator_core_callback(bldc_window, pixel_per_unit)
    if bldc_window.ui.display_wires_checkbox.isChecked():
        bldc_window.draw_wires_callback(bldc_window, pixel_per_unit)
    if bldc_window.ui.display_magnets_checkbox.isChecked():
        bldc_window.draw_magnets_callback(bldc_window, pixel_per_unit)
    if bldc_window.ui.display_outrunner_checkbox.isChecked():
        bldc_window.draw_outrunner_callback(bldc_window, pixel_per_unit)

def update_visualization_with_cache(bldc_window):
    """Update visualization using cached turns per layer."""
    bldc_window.use_cache = True
    update_visualization(bldc_window)
    bldc_window.use_cache = False