"""
Visualization functions for drawing BLDC motor components.
"""
import numpy as np
import pyqtgraph as pg

# stop potential import loops
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_window import BLDCWindow
else:
    from typing import Any
    BLDCWindow = Any

from fractions import Fraction

def draw_axle(bldc_window: BLDCWindow, _):
    """Draw the central axle circle."""
    theta = np.linspace(0, 2 * np.pi, 60, endpoint=False)
    x = bldc_window.ui.axle_radius_lineedit.get_mm_value() * np.cos(theta)
    y = bldc_window.ui.axle_radius_lineedit.get_mm_value() * np.sin(theta)
    x = np.append(x, x[0])
    y = np.append(y, y[0])
    pen_width = 2
    bldc_window.ui.stator_plot_widget.plot(x, y, pen=pg.mkPen("#000000", width=pen_width))

def get_magnet_inner_radius(bldc_window: BLDCWindow):
    magnet_outer_radius = bldc_window.ui.radius_lineedit.get_mm_value() - bldc_window.ui.outrunner_thickness_lineedit.get_mm_value()
    if magnet_outer_radius==0:
        return 0,0
    if bldc_window.ui.magnet_tab_widget.currentIndex()==0: # square magnet
        magnet_thickness = bldc_window.ui.square_magnet_thickness_lineedit.get_mm_value()
        magnet_width = bldc_window.ui.square_magnet_width_lineedit.get_mm_value()

        if bldc_window.ui.square_magnet_rounded_corners.isChecked():
            rad = bldc_window.ui.square_magnet_rounding_radius_lineedit.get_mm_value()
            magnet_width -= 2*rad
        dist_from_wall = magnet_outer_radius - magnet_outer_radius*np.sin(np.arccos(magnet_width/2/magnet_outer_radius))
        magnet_inner_radius = magnet_outer_radius - magnet_thickness - dist_from_wall

        #print(f"magnet_thickness({magnet_thickness}), magnet_width({magnet_width}), rad({rad}), dist_from_wall({dist_from_wall}), magnet_inner_radius({magnet_inner_radius})")
    else:
        magnet_thickness = bldc_window.ui.arc_magnet_thickness_lineedit.get_mm_value()

        dist_from_wall = 0
        magnet_inner_radius = magnet_outer_radius - magnet_thickness
    return magnet_inner_radius, dist_from_wall

def xy_groups_to_nan_joined(all_xy):
    all_x = []
    all_y = []
    for xy in all_xy:
        x, y = xy
        all_x.append(np.nan)
        all_y.append(np.nan)
        all_x.extend(x)
        all_y.extend(y)
    return all_x, all_y

def draw_magnets(bldc_window: BLDCWindow, _):
    """Draw magnets on the outrunner with thickness toward the stator."""
    magnet_outer_radius = bldc_window.ui.radius_lineedit.get_mm_value() - bldc_window.ui.outrunner_thickness_lineedit.get_mm_value()


    if bldc_window.ui.magnet_tab_widget.currentIndex()==0: # square magnet
        # todo: break into own section dependent on num magnets and thickness
        num_magnets = bldc_window.ui.num_square_magnets_lineedit.get_value()
        magnet_thickness = bldc_window.ui.square_magnet_thickness_lineedit.get_mm_value()
        if magnet_thickness == 0 or num_magnets == 0:
            return

        if bldc_window.ui.square_magnet_rounded_corners.isChecked():
            rounding_radius = bldc_window.ui.square_magnet_rounding_radius_lineedit.get_mm_value()
        else:
            rounding_radius = 0

        magnet_inner_radius, dist_from_wall = get_magnet_inner_radius(bldc_window)
        bldc_window.ui.square_magnet_dist_from_circle_lineedit.set_mm_value(dist_from_wall)
        theta = (num_magnets - 2) * np.pi / (2 * num_magnets)
        no_thickness_width = 2 * magnet_outer_radius * np.cos(theta)
        h = magnet_outer_radius * np.sin(theta) - (magnet_thickness - rounding_radius)
        max_w = 2 * h * np.cos(theta)
        bldc_window.ui.square_magnet_width_slider.setFractionalSingleStep(max_w / 1000)
        bldc_window.ui.square_magnet_width_slider.setFractionalMinimum(0)
        bldc_window.ui.square_magnet_width_slider.setFractionalMaximum(max_w)
        bldc_window.ui.square_magnet_min_max_display.setText(f"[0mm, {max_w}mm]")

        magnet_width = bldc_window.ui.square_magnet_width_lineedit.get_mm_value()
        dist_from_each_other = max_w - magnet_width
        bldc_window.ui.square_magnet_dist_between_lineedit.set_mm_value(dist_from_each_other)

        if rounding_radius * 2 > magnet_width:
            bldc_window.ui.square_magnet_rounding_radius_lineedit.setStyleSheet("background-color: red;")
            bldc_window.ui.square_magnet_rounding_radius_lineedit.setToolTip("rounding radius cannot be greater than magnet width")
        elif rounding_radius * 2 > magnet_thickness:
            bldc_window.ui.square_magnet_rounding_radius_lineedit.setStyleSheet("background-color: red;")
            bldc_window.ui.square_magnet_rounding_radius_lineedit.setToolTip("rounding radius cannot be greater than magnet height")
        else:
            bldc_window.ui.square_magnet_rounding_radius_lineedit.setStyleSheet("")
            bldc_window.ui.square_magnet_rounding_radius_lineedit.setToolTip("")
        # todo end

        all_xy = get_square_magnet_points(num_magnets, magnet_outer_radius, dist_from_wall, rounding_radius, magnet_width, magnet_thickness)
        all_x, all_y = xy_groups_to_nan_joined(all_xy)

        pen_width = 2
        bldc_window.ui.stator_plot_widget.plot(all_x, all_y, pen=pg.mkPen("#C0C0C0", width=pen_width), fillLevel=0, fillBrush=pg.mkBrush("#E0E0E0"))

    else:
        # todo: break into own section dependent on num magnets
        num_magnets = bldc_window.ui.num_arc_magnets_lineedit.get_value()
        if num_magnets == 0:
            return
        #magnet_thickness = bldc_window.ui.arc_magnet_thickness_lineedit.get_mm_value()
        max_arc_width = 360/num_magnets
        magnet_inner_radius, _ = get_magnet_inner_radius(bldc_window)

        if magnet_outer_radius-magnet_inner_radius==0:
            return

        bldc_window.ui.arc_magnet_width_slider.setFractionalSingleStep(max_arc_width / 1000)
        bldc_window.ui.arc_magnet_width_slider.setFractionalMinimum(0)
        bldc_window.ui.arc_magnet_width_slider.setFractionalMaximum(max_arc_width)
        bldc_window.ui.arc_magnet_min_max_display.setText(f"[0°, {max_arc_width}°]")

        arc_width = bldc_window.ui.arc_magnet_width_lineedit.get_degrees_value()
        dist_from_each_other = 2 * magnet_inner_radius * np.sin(np.deg2rad(max_arc_width - arc_width) / 2)
        bldc_window.ui.arc_magnet_dist_between_lineedit.set_mm_value(dist_from_each_other)
        # todo end
        all_xy = get_arc_magnet_points(num_magnets, arc_width, magnet_inner_radius, magnet_outer_radius)
        all_x, all_y = xy_groups_to_nan_joined(all_xy)

        pen_width = 2
        bldc_window.ui.stator_plot_widget.plot(all_x, all_y, pen=pg.mkPen("#C0C0C0", width=pen_width), fillLevel=0, fillBrush=pg.mkBrush("#E0E0E0"))

def get_arc_magnet_points(num_magnets, arc_width, magnet_inner_radius, magnet_outer_radius):
    magnet_arc = 2 * np.pi / num_magnets
    all_x, all_y = [], []
    group_xy = []
    for i in range(int(num_magnets)):
        group_xy.append([[], []])
        magnet_angle = i * (2 * np.pi / num_magnets)
        start_angle = magnet_angle - np.deg2rad(arc_width) / 2
        end_angle = magnet_angle + np.deg2rad(arc_width) / 2
        theta_magnet = np.linspace(start_angle, end_angle, 20, endpoint=False)
        x_inner = magnet_inner_radius * np.cos(theta_magnet)
        y_inner = magnet_inner_radius * np.sin(theta_magnet)
        x_outer = magnet_outer_radius * np.cos(theta_magnet[::-1])
        y_outer = magnet_outer_radius * np.sin(theta_magnet[::-1])
        x_magnet = np.concatenate([x_inner, x_outer])
        y_magnet = np.concatenate([y_inner, y_outer])
        x_magnet = np.append(x_magnet, x_magnet[0])
        y_magnet = np.append(y_magnet, y_magnet[0])
        group_xy[-1][0].extend(x_magnet)
        group_xy[-1][1].extend(y_magnet)
        group_xy[-1][0].append(group_xy[-1][0][0])
        group_xy[-1][1].append(group_xy[-1][1][0])
        #all_x.append(np.nan)
        #all_y.append(np.nan)
    return group_xy


def get_square_magnet_points(num_magnets, magnet_outer_radius, dist_from_wall, rounding_radius, magnet_width, magnet_thickness):
    non_round_width = magnet_width - rounding_radius * 2
    non_round_height = magnet_thickness - rounding_radius * 2

    group_xy = []
    for i in range(int(num_magnets)):
        group_xy.append([[], []])
        q = i * (2 * np.pi / num_magnets)  # magnet_angle

        r = magnet_outer_radius - dist_from_wall

        if rounding_radius != 0:
            quarter_center_x = (r - rounding_radius) * np.cos(q) - (non_round_width / 2) * np.sin(q)
            quarter_center_y = (r - rounding_radius) * np.sin(q) + (non_round_width / 2) * np.cos(q)

            theta_quarter_start = np.linspace(q + 2 * np.pi, q + 3 * np.pi / 2, 10, endpoint=True)
            x_quarter = quarter_center_x - (rounding_radius * np.sin(theta_quarter_start))
            y_quarter = quarter_center_y + (rounding_radius * np.cos(theta_quarter_start))
            #raise(ValueError(f"{group_xy}"))
            group_xy[-1][0].extend(x_quarter)
            group_xy[-1][1].extend(y_quarter)

        x_left = r * np.cos(q) - non_round_width / 2 * np.sin(q)
        y_left = r * np.sin(q) + non_round_width / 2 * np.cos(q)
        x_right = r * np.cos(q) + non_round_width / 2 * np.sin(q)
        y_right = r * np.sin(q) - non_round_width / 2 * np.cos(q)

        if rounding_radius == 0:
            group_xy[-1][0].extend([x_left, x_right])
            group_xy[-1][1].extend([y_left, y_right])
            #group_xy[-1][0].extend([x_right])
            #group_xy[-1][1].extend([y_right])

        if rounding_radius != 0:
            quarter_center_x = (r - rounding_radius) * np.cos(q) + (non_round_width / 2) * np.sin(q)
            quarter_center_y = (r - rounding_radius) * np.sin(q) - (non_round_width / 2) * np.cos(q)

            theta_quarter_start = np.linspace(q - np.pi / 2, q - np.pi, 10, endpoint=True)
            x_quarter = quarter_center_x - (rounding_radius * np.sin(theta_quarter_start))
            y_quarter = quarter_center_y + (rounding_radius * np.cos(theta_quarter_start))
            group_xy[-1][0].extend(x_quarter)
            group_xy[-1][1].extend(y_quarter)

        x_left = (r - rounding_radius) * np.cos(q) + magnet_width / 2 * np.sin(q)
        y_left = (r - rounding_radius) * np.sin(q) - magnet_width / 2 * np.cos(q)
        x_right = (r - rounding_radius - non_round_height) * np.cos(q) + magnet_width / 2 * np.sin(q)
        y_right = (r - rounding_radius - non_round_height) * np.sin(q) - magnet_width / 2 * np.cos(q)

        if rounding_radius==0:
            group_xy[-1][0].extend([x_right])
            group_xy[-1][1].extend([y_right])

        if rounding_radius != 0:
            quarter_center_x = (r - rounding_radius - non_round_height) * np.cos(q) + (non_round_width / 2) * np.sin(q)
            quarter_center_y = (r - rounding_radius - non_round_height) * np.sin(q) - (non_round_width / 2) * np.cos(q)

            theta_quarter_start = np.linspace(q + np.pi, q + np.pi / 2, 10, endpoint=True)
            x_quarter = quarter_center_x - (rounding_radius * np.sin(theta_quarter_start))
            y_quarter = quarter_center_y + (rounding_radius * np.cos(theta_quarter_start))
            group_xy[-1][0].extend(x_quarter)
            group_xy[-1][1].extend(y_quarter)

        x_left = (r - magnet_thickness) * np.cos(q) + non_round_width / 2 * np.sin(q)
        y_left = (r - magnet_thickness) * np.sin(q) - non_round_width / 2 * np.cos(q)
        x_right = (r - magnet_thickness) * np.cos(q) - non_round_width / 2 * np.sin(q)
        y_right = (r - magnet_thickness) * np.sin(q) + non_round_width / 2 * np.cos(q)

        if rounding_radius == 0:
            group_xy[-1][0].extend([x_right])
            group_xy[-1][1].extend([y_right])

        if rounding_radius != 0:
            quarter_center_x = (r - rounding_radius - non_round_height) * np.cos(q) - (non_round_width / 2) * np.sin(q)
            quarter_center_y = (r - rounding_radius - non_round_height) * np.sin(q) + (non_round_width / 2) * np.cos(q)

            theta_quarter_start = np.linspace(q + np.pi / 2, q, 10, endpoint=True)
            x_quarter = quarter_center_x - (rounding_radius * np.sin(theta_quarter_start))
            y_quarter = quarter_center_y + (rounding_radius * np.cos(theta_quarter_start))
            group_xy[-1][0].extend(x_quarter)
            group_xy[-1][1].extend(y_quarter)

        x_left = (r - rounding_radius - non_round_height) * np.cos(q) - magnet_width / 2 * np.sin(q)
        y_left = (r - rounding_radius - non_round_height) * np.sin(q) + magnet_width / 2 * np.cos(q)
        x_right = (r - rounding_radius) * np.cos(q) - magnet_width / 2 * np.sin(q)
        y_right = (r - rounding_radius) * np.sin(q) + magnet_width / 2 * np.cos(q)

        #if rounding_radius == 0:
            #group_xy[-1][0].extend([x_right])
            #group_xy[-1][1].extend([y_right])

        group_xy[-1][0].append(group_xy[-1][0][0])
        group_xy[-1][1].append(group_xy[-1][1][0])

    return group_xy

def draw_outrunner(bldc_window: BLDCWindow, _):
    """Draw outrunner circles with editable thickness."""
    theta = np.linspace(0, 2 * np.pi, 200, endpoint=False)
    inner_radius = bldc_window.ui.radius_lineedit.get_mm_value() - bldc_window.ui.outrunner_thickness_lineedit.get_mm_value()
    x_inner = inner_radius * np.cos(theta)
    y_inner = inner_radius * np.sin(theta)
    x_inner = np.append(x_inner, x_inner[0])
    y_inner = np.append(y_inner, y_inner[0])
    pen_width = 2
    bldc_window.ui.stator_plot_widget.plot(x_inner, y_inner, pen=pg.mkPen("#808080", width=pen_width))
    outer_radius = bldc_window.ui.radius_lineedit.get_mm_value()
    x_outer = outer_radius * np.cos(theta)
    y_outer = outer_radius * np.sin(theta)
    x_outer = np.append(x_outer, x_outer[0])
    y_outer = np.append(y_outer, y_outer[0])
    bldc_window.ui.stator_plot_widget.plot(x_outer, y_outer, pen=pg.mkPen("#808080", width=pen_width))

def draw_stator_core(bldc_window: BLDCWindow, pixel_per_unit):
    """Draw the stator core with slots, supporting CNC milling."""
    num_slots = int(bldc_window.ui.num_slots_lineedit.get_value())
    slot_width_half = bldc_window.ui.slot_width_lineedit.get_mm_value() / 2
    hammerhead_width = bldc_window.ui.hammerhead_width_lineedit.get_mm_value()
    hammerhead_length = bldc_window.ui.hammerhead_length_lineedit.get_mm_value()
    r_inner = bldc_window.ui.stator_inner_radius_lineedit.get_mm_value()
    mag_inner, _ = get_magnet_inner_radius(bldc_window)

    r_outer = (
        mag_inner
        - bldc_window.ui.air_gap_lineedit.get_mm_value()
        - hammerhead_length
    )
    cnc_milling = bldc_window.ui.cnc_milling_checkbox.isChecked()
    drill_bit_radius = bldc_window.ui.drill_bit_diameter_lineedit.get_mm_value() / 2 if cnc_milling else 0
    pen_width = 2
    pen = pg.mkPen("#000000", width=pen_width)
    all_x, all_y = [], []

    for slot_idx in range(num_slots):
        x_slot, y_slot = _calculate_slot_points(
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

    if all_x:
        all_x.append(all_x[0])
        all_y.append(all_y[0])
        bldc_window.ui.stator_plot_widget.plot(np.array(all_x), np.array(all_y), pen=pen)

def _calculate_slot_points(
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
                               (r_inner+drill_bit_radius) * np.cos(q)
            + drill_bit_radius * np.sin(q)
            + slot_width_half * np.sin(q)
        )
        quarter_center_y = (
            (r_inner+drill_bit_radius) * np.sin(q)
            - drill_bit_radius * np.cos(q)
            - slot_width_half * np.cos(q)
        )
        theta_quarter_start = np.linspace(q + np.pi / 2 - np.pi / (2 * 20), q, 10, endpoint=False)
        x_quarter_start = quarter_center_x - (drill_bit_radius * np.sin(theta_quarter_start))
        y_quarter_start = quarter_center_y + (drill_bit_radius * np.cos(theta_quarter_start))
        x_slot.extend(x_quarter_start)
        y_slot.extend(y_quarter_start)

    if not cnc_milling:
        drill_bit_radius = 0

    t_vals = np.linspace(r_inner+drill_bit_radius, r_outer - drill_bit_radius, 2)
    x_left = t_vals * np.cos(q) - slot_width_half * np.sin(q)
    y_left = t_vals * np.sin(q) + slot_width_half * np.cos(q)
    x_right = t_vals * np.cos(q) + slot_width_half * np.sin(q)
    y_right = t_vals * np.sin(q) - slot_width_half * np.cos(q)

    hammer_theta = np.arctan2(hammerhead_width + slot_width_half, r_outer + hammerhead_length)
    # div 2 would make sense, but close enough
    sub_len = (hammerhead_width + slot_width_half)* np.tan( hammer_theta )/1.9
    hammer_length_adjusted = hammerhead_length - sub_len
    #if hammer_length_adjusted<0:
    #    print("f")
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
        theta_half_left = np.linspace(q + 3*np.pi/2 - np.pi / (2 * 30), q + np.pi, 15, endpoint=False)
        x_half_left = half_center_x_left - (drill_bit_radius * np.sin(theta_half_left))
        y_half_left = half_center_y_left + (drill_bit_radius * np.cos(theta_half_left))
        half_center_x_right = x_right[-1] - drill_bit_radius * np.cos(q + np.pi / 2)
        half_center_y_right = y_right[-1] - drill_bit_radius * np.sin(q + np.pi / 2)
        theta_half_right = np.linspace(q + 2 * np.pi - np.pi / (2 * 30), q + 3*np.pi/2, 15, endpoint=False)
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
    arc_theta = np.linspace(arc_end, arc_start, 20, endpoint=True)
    arc_radius = r_outer + hammerhead_length
    x_arc = arc_radius * np.cos(arc_theta)
    y_arc = arc_radius * np.sin(arc_theta)

    if cnc_milling:
        quarter_center_x = (
            (r_inner+drill_bit_radius) * np.cos(q)
            - drill_bit_radius * np.sin(q)
            - slot_width_half * np.sin(q)
        )
        quarter_center_y = (
            (r_inner+drill_bit_radius) * np.sin(q)
            + drill_bit_radius * np.cos(q)
            + slot_width_half * np.cos(q)
        )
        theta_quarter_end = np.linspace(q + np.pi + np.pi / (2 * 20), q + np.pi / 2, 10, endpoint=False)
        x_quarter_end = quarter_center_x - (drill_bit_radius * np.sin(theta_quarter_end))
        y_quarter_end = quarter_center_y + (drill_bit_radius * np.cos(theta_quarter_end))

    if cnc_milling:
        arc_start = np.arctan2(y_quarter_end[-1], x_quarter_end[-1])
        q_next = np.deg2rad((slot_idx + 1) * (360 / num_slots))
        quarter_center_x = (
            (r_inner+drill_bit_radius) * np.cos(q_next)
            + drill_bit_radius * np.sin(q_next)
            + slot_width_half * np.sin(q_next)
        )
        quarter_center_y = (
            (r_inner+drill_bit_radius) * np.sin(q_next)
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