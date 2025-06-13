"""
Visualization functions for drawing BLDC motor side view as overlapping rectangles and wire lines.
"""
import numpy as np
import pyqtgraph as pg
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_window import BLDCWindow
else:
    from typing import Any
    BLDCWindow = Any
from freecad.actuators.util import traverse_tuple

def get_magnet_inner_radius(bldc_window: BLDCWindow):
    magnet_outer_radius = bldc_window.ui.radius_lineedit.get_mm_value() - bldc_window.ui.outrunner_thickness_lineedit.get_mm_value()
    if magnet_outer_radius==0:
        return 0, 0
    if bldc_window.ui.magnet_tab_widget.currentIndex() == 0:  # square magnet
        magnet_thickness = bldc_window.ui.square_magnet_thickness_lineedit.get_mm_value()
        magnet_width = bldc_window.ui.square_magnet_width_lineedit.get_mm_value()
        if bldc_window.ui.square_magnet_rounded_corners.isChecked():
            rad = bldc_window.ui.square_magnet_rounding_radius_lineedit.get_mm_value()
            magnet_width -= 2 * rad
        dist_from_wall = magnet_outer_radius - magnet_outer_radius * np.sin(np.arccos(magnet_width / 2 / magnet_outer_radius))
        magnet_inner_radius = magnet_outer_radius - magnet_thickness - dist_from_wall
    else:  # arc magnet
        magnet_thickness = bldc_window.ui.arc_magnet_thickness_lineedit.get_mm_value()
        dist_from_wall = 0
        magnet_inner_radius = magnet_outer_radius - magnet_thickness
    return magnet_inner_radius, dist_from_wall

def draw_side_base(bldc_window: BLDCWindow, pixel_per_unit):
    """Draw the base rectangle in the side view."""
    outrunner_outer_radius = bldc_window.ui.radius_lineedit.get_mm_value()
    base_height = bldc_window.ui.base_height_lineedit.get_mm_value()
    pen_width = 2
    base_x = [-outrunner_outer_radius, outrunner_outer_radius, outrunner_outer_radius, -outrunner_outer_radius, -outrunner_outer_radius]
    base_y = [0, 0, base_height, base_height, 0]
    bldc_window.ui.side_view_plot_widget.plot(base_x, base_y, pen=pg.mkPen("#4B0082", width=pen_width), fillLevel=0, fillBrush=pg.mkBrush("#4B008280"))

def draw_side_axle(bldc_window: BLDCWindow, pixel_per_unit):
    """Draw the axle rectangle in the side view."""
    axle_radius = bldc_window.ui.axle_radius_lineedit.get_mm_value()
    base_height = bldc_window.ui.base_height_lineedit.get_mm_value()
    outrunner_height = bldc_window.ui.outrunner_height_lineedit.get_mm_value()
    base_extension = bldc_window.ui.axle_below_base_height_lineedit.get_mm_value()
    outrunner_extension = bldc_window.ui.axle_above_outrunner_height_lineedit.get_mm_value()
    axle_bottom = -base_extension
    axle_top = base_height + outrunner_height + outrunner_extension
    pen_width = 2
    axle_x = [-axle_radius, axle_radius, axle_radius, -axle_radius, -axle_radius]
    axle_y = [axle_bottom, axle_bottom, axle_top, axle_top, axle_bottom]
    bldc_window.ui.side_view_plot_widget.plot(axle_x, axle_y, pen=pg.mkPen("#000000", width=pen_width), fillLevel=0, fillBrush=pg.mkBrush("#00000080"))

def draw_side_stator(bldc_window: BLDCWindow, pixel_per_unit):
    """Draw the stator core rectangles in the side view."""
    stator_inner_radius = bldc_window.ui.axle_radius_lineedit.get_mm_value()
    magnet_inner_radius, _ = get_magnet_inner_radius(bldc_window)
    air_gap = bldc_window.ui.air_gap_lineedit.get_mm_value()
    hammerhead_length = bldc_window.ui.hammerhead_length_lineedit.get_mm_value()
    base_dist = bldc_window.ui.stator_dist_from_base_lineedit.get_mm_value()
    start_height = bldc_window.ui.base_height_lineedit.get_mm_value() + base_dist
    stator_height = bldc_window.ui.stator_height_lineedit.get_mm_value()
    stator_outer_radius = magnet_inner_radius - air_gap - hammerhead_length
    if start_height==0 or stator_outer_radius-stator_inner_radius==0:
        return
    pen_width = 2
    stator_x = [stator_inner_radius, stator_outer_radius, stator_outer_radius, stator_inner_radius, stator_inner_radius]
    stator_y = [start_height, start_height, start_height + stator_height, start_height + stator_height, start_height]
    bldc_window.ui.side_view_plot_widget.plot(stator_x, stator_y, pen=pg.mkPen("#000000", width=pen_width), fillLevel=0, fillBrush=pg.mkBrush("#00000040"))
    stator_x_neg = [-stator_outer_radius, -stator_inner_radius, -stator_inner_radius, -stator_outer_radius, -stator_outer_radius]
    bldc_window.ui.side_view_plot_widget.plot(stator_x_neg, stator_y, pen=pg.mkPen("#000000", width=pen_width), fillLevel=0, fillBrush=pg.mkBrush("#00000040"))

def draw_side_magnets(bldc_window: BLDCWindow, pixel_per_unit):
    """Draw the magnet rectangles in the side view."""
    magnet_outer_radius = bldc_window.ui.radius_lineedit.get_mm_value() - bldc_window.ui.outrunner_thickness_lineedit.get_mm_value()
    magnet_inner_radius, _ = get_magnet_inner_radius(bldc_window)

    base_dist = bldc_window.ui.stator_dist_from_base_lineedit.get_mm_value()
    start_height = bldc_window.ui.base_height_lineedit.get_mm_value() + base_dist
    stator_height = bldc_window.ui.stator_height_lineedit.get_mm_value()
    mid_stator_height = start_height + stator_height/2

    if bldc_window.ui.magnet_tab_widget.currentIndex()==0:
        magnet_height = bldc_window.ui.square_magnet_height_lineedit.get_mm_value()
    else:
        magnet_height = bldc_window.ui.arc_magnet_height_lineedit.get_mm_value()
    magnet_bottom = mid_stator_height - magnet_height / 2
    magnet_top = mid_stator_height + magnet_height / 2
    pen_width = 2
    magnet_x = [magnet_inner_radius, magnet_outer_radius, magnet_outer_radius, magnet_inner_radius, magnet_inner_radius]
    magnet_y = [magnet_bottom, magnet_bottom, magnet_top, magnet_top, magnet_bottom]
    bldc_window.ui.side_view_plot_widget.plot(magnet_x, magnet_y, pen=pg.mkPen("#C0C0C0", width=pen_width), fillLevel=0, fillBrush=pg.mkBrush("#C0C0C080"))
    magnet_x_neg = [-magnet_outer_radius, -magnet_inner_radius, -magnet_inner_radius, -magnet_outer_radius, -magnet_outer_radius]
    bldc_window.ui.side_view_plot_widget.plot(magnet_x_neg, magnet_y, pen=pg.mkPen("#C0C0C0", width=pen_width), fillLevel=0, fillBrush=pg.mkBrush("#C0C0C080"))

def draw_side_outrunner(bldc_window: BLDCWindow, pixel_per_unit):
    """Draw the outrunner rectangles in the side view."""
    outrunner_thickness = bldc_window.ui.outrunner_thickness_lineedit.get_mm_value()
    magnet_outer_radius = bldc_window.ui.radius_lineedit.get_mm_value() - outrunner_thickness
    outrunner_outer_radius = bldc_window.ui.radius_lineedit.get_mm_value()
    base_height = bldc_window.ui.base_height_lineedit.get_mm_value() + bldc_window.ui.outrunner_height_gap_lineedit.get_mm_value()
    outrunner_height = bldc_window.ui.outrunner_height_lineedit.get_mm_value()
    pen_width = 2
    # ccw
    outrunner_x = [ outrunner_outer_radius,  # start bottom right
                   outrunner_outer_radius,
                   -outrunner_outer_radius,
                   -outrunner_outer_radius,
                   -magnet_outer_radius,
                   -magnet_outer_radius,
                   magnet_outer_radius,
                   magnet_outer_radius,
                   outrunner_outer_radius]  # end bottom right
    outrunner_y = [ base_height,
                    base_height + outrunner_height,
                    base_height + outrunner_height,
                    base_height,
                    base_height,
                    base_height + outrunner_height - outrunner_thickness,
                    base_height + outrunner_height - outrunner_thickness,
                    base_height,
                    base_height]
    bldc_window.ui.side_view_plot_widget.plot(outrunner_x, outrunner_y, pen=pg.mkPen("#808080", width=pen_width), fillLevel=0, fillBrush=pg.mkBrush("#80808080"))

def draw_side_wires(bldc_window: BLDCWindow, pixel_per_unit):
    """Draw the wire lines above and below the stator in the side view."""
    stator_inner_radius = bldc_window.ui.stator_inner_radius_lineedit.get_mm_value()
    magnet_inner_radius, _ = get_magnet_inner_radius(bldc_window)
    air_gap = bldc_window.ui.air_gap_lineedit.get_mm_value()
    hammerhead_length = bldc_window.ui.hammerhead_length_lineedit.get_mm_value()
    stator_outer_radius = magnet_inner_radius - air_gap - hammerhead_length
    base_height = bldc_window.ui.base_height_lineedit.get_mm_value()
    stator_height = bldc_window.ui.stator_height_lineedit.get_mm_value()
    wire_diam = bldc_window.ui.wire_diameter_lineedit.get_mm_value()
    stator_base_dist = bldc_window.ui.stator_dist_from_base_lineedit.get_mm_value()
    if stator_height==0 or stator_outer_radius-stator_inner_radius==0 or wire_diam==0:
        return

    tight_pack = bldc_window.ui.tight_pack_checkbox.isChecked()
    bin_radii_even = np.arange(stator_inner_radius, stator_outer_radius, wire_diam)
    bin_radii_odd = np.arange(stator_inner_radius + (wire_diam / 2), stator_outer_radius+wire_diam, wire_diam)
    bin_radii = np.arange(stator_inner_radius, stator_outer_radius, wire_diam)
    bin_counts_even = [0] * len(bin_radii_even)
    bin_counts_odd = [0] * len(bin_radii_odd)
    bin_counts = [0] * len(bin_radii)
    try:
        turns_list = eval(bldc_window.ui.turns_per_layer_lineedit.text())
    except SyntaxError:
        return  # don't run this function without the turns list
    if not isinstance(turns_list, list):
        return  # don't run this function without the turns list
    current_layer = 0
    for turn_tuple in turns_list:
        for turn in traverse_tuple(turn_tuple):  # Simplified traversal
            #if tight_pack:
            #    if current_layer % 2 == 0:
            #        bin_counts_even[turn] = int((current_layer + 2) / 2)
            #    else:
            #        bin_counts_odd[turn] = int((current_layer + 1) / 2)
            #else:
            bin_counts[turn] = current_layer
        current_layer += 1
    #if tight_pack:
    #    max_bin_count = max(max(bin_counts_even), max(bin_counts_odd))
    #else:
    max_bin_count = max(bin_counts)
    all_x, all_y = [], []

    for bc in range(max_bin_count+1):
        if tight_pack:
            middle_height = wire_diam * (bc - 1) * np.sqrt(3)/2 + wire_diam * .5
        else:
            middle_height = (bc - 1) * wire_diam + wire_diam / 2
        wire_y_top = base_height + stator_base_dist + stator_height + middle_height
        wire_y_bottom = base_height + stator_base_dist - middle_height
        all_x.extend([-stator_outer_radius, stator_outer_radius, np.nan])
        all_y.extend([wire_y_top, wire_y_top, np.nan])
        all_x.extend([-stator_outer_radius, stator_outer_radius, np.nan])
        all_y.extend([wire_y_bottom, wire_y_bottom, np.nan])
    bldc_window.ui.side_view_plot_widget.plot(all_x, all_y, pen=pg.mkPen("#B87333", width=wire_diam / pixel_per_unit))