
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_window import BLDCWindow
else:
    from typing import Any
    BLDCWindow = Any

def connect_side_display_checkboxes(bldc_window: BLDCWindow):
    """Create horizontal Display Options group at the top."""
    bldc_window.ui.side_view_plot_widget.sigRangeChanged.connect(lambda: draw_side_view(bldc_window))

    bldc_window.ui.display_base_checkbox.setChecked(True)
    bldc_window.ui.display_base_checkbox.stateChanged.connect(lambda: draw_side_view(bldc_window))

    bldc_window.ui.display_axle_checkbox.setChecked(True)
    bldc_window.ui.display_axle_checkbox.stateChanged.connect(lambda: draw_side_view(bldc_window))

    bldc_window.ui.display_stator_core_checkbox.setChecked(True)
    bldc_window.ui.display_stator_core_checkbox.stateChanged.connect(lambda: draw_side_view(bldc_window))

    bldc_window.ui.display_magnets_checkbox.setChecked(True)
    bldc_window.ui.display_magnets_checkbox.stateChanged.connect(lambda: draw_side_view(bldc_window))

    bldc_window.ui.display_outrunner_checkbox.setChecked(True)
    bldc_window.ui.display_outrunner_checkbox.stateChanged.connect(lambda: draw_side_view(bldc_window))

    bldc_window.ui.display_wires_checkbox.setChecked(True)
    bldc_window.ui.display_wires_checkbox.stateChanged.connect(lambda: draw_side_view(bldc_window))


def connect_side_display_and_parameters(bldc_window: BLDCWindow):
    """Create grouped UI elements for motor parameters."""
    # Plot widget
    #bldc_window.ui.stator_plot_widget = pg.PlotWidget()
    bldc_window.ui.side_view_plot_widget.setAspectLocked(True)
    bldc_window.ui.side_view_plot_widget.setRange(xRange=[-150, 150], yRange=[-150, 150])
    bldc_window.ui.side_view_plot_widget.setBackground("w")
    #bldc_window.ui.stator_display_tab.addWidget(bldc_window.ui.stator_plot_widget, 3)

    # General Parameters Group
    bldc_window.ui.radius_lineedit.textChanged.connect(lambda: draw_side_view(bldc_window))
    bldc_window.ui.air_gap_lineedit.textChanged.connect(lambda: draw_side_view(bldc_window))
    bldc_window.ui.base_height_lineedit.textChanged.connect(lambda: draw_side_view(bldc_window))

    # Axle Group
    bldc_window.ui.axle_radius_lineedit.textChanged.connect(lambda: draw_side_view(bldc_window))
    bldc_window.ui.axle_below_base_height_lineedit.textChanged.connect(lambda: draw_side_view(bldc_window))
    bldc_window.ui.axle_above_outrunner_height_lineedit.textChanged.connect(lambda: draw_side_view(bldc_window))

    # Stator Group
    bldc_window.ui.hammerhead_length_lineedit.textChanged.connect(lambda: draw_side_view(bldc_window))
    bldc_window.ui.stator_inner_radius_lineedit.textChanged.connect(lambda: draw_side_view(bldc_window))
    bldc_window.ui.stator_height_lineedit.textChanged.connect(lambda: draw_side_view(bldc_window))
    bldc_window.ui.stator_dist_from_base_lineedit.textChanged.connect(lambda: draw_side_view(bldc_window))

    # Outrunner Group
    bldc_window.ui.outrunner_thickness_lineedit.textChanged.connect(lambda: draw_side_view(bldc_window))
    bldc_window.ui.outrunner_height_lineedit.textChanged.connect(lambda: draw_side_view(bldc_window))
    bldc_window.ui.outrunner_height_gap_lineedit.textChanged.connect(lambda: draw_side_view(bldc_window))

    # Magnet Group
    bldc_window.ui.magnet_tab_widget.currentChanged.connect(lambda: draw_side_view(bldc_window))
    bldc_window.ui.square_magnet_width_lineedit.textChanged.connect(lambda: draw_side_view(bldc_window))
    bldc_window.ui.square_magnet_rounded_corners.stateChanged.connect(lambda: draw_side_view(bldc_window))
    bldc_window.ui.square_magnet_rounding_radius_lineedit.textChanged.connect(lambda: draw_side_view(bldc_window))
    bldc_window.ui.arc_magnet_thickness_lineedit.textChanged.connect(lambda: draw_side_view(bldc_window))
    bldc_window.ui.square_magnet_height_lineedit.textChanged.connect(lambda: draw_side_view(bldc_window))
    bldc_window.ui.arc_magnet_height_lineedit.textChanged.connect(lambda: draw_side_view(bldc_window))

    # wire
    bldc_window.ui.turns_per_layer_lineedit.textChanged.connect(lambda: draw_side_view(bldc_window))
    bldc_window.ui.wire_diameter_lineedit.textChanged.connect(lambda: draw_side_view(bldc_window))
    bldc_window.ui.tight_pack_checkbox.stateChanged.connect(lambda: draw_side_view(bldc_window))

    print("connected side view")

def draw_side_view(bldc_window: BLDCWindow):
    """Draw the complete side view of the BLDC motor based on checkbox states."""
    bldc_window.ui.side_view_plot_widget.clear()

    # Calculate pixel scale
    view_range = bldc_window.ui.side_view_plot_widget.getViewBox().viewRange()
    plot_size = bldc_window.ui.side_view_plot_widget.size()
    x_scale = (view_range[0][1] - view_range[0][0]) / plot_size.width()
    y_scale = (view_range[1][1] - view_range[1][0]) / plot_size.height()
    pixel_per_unit = min(x_scale, y_scale)

    if bldc_window.ui.display_base_checkbox.isChecked():
        bldc_window.draw_side_base_callback(bldc_window, pixel_per_unit)
    if bldc_window.ui.display_axle_checkbox.isChecked():
        bldc_window.draw_side_axle_callback(bldc_window, pixel_per_unit)
    if bldc_window.ui.display_stator_core_checkbox.isChecked():
        bldc_window.draw_side_stator_callback(bldc_window, pixel_per_unit)
    if bldc_window.ui.display_magnets_checkbox.isChecked():
        bldc_window.draw_side_magnets_callback(bldc_window, pixel_per_unit)
    if bldc_window.ui.display_outrunner_checkbox.isChecked():
        bldc_window.draw_side_outrunner_callback(bldc_window, pixel_per_unit)
    if bldc_window.ui.display_wires_checkbox.isChecked():
        bldc_window.draw_side_wires_callback(bldc_window, pixel_per_unit)