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

def draw_axle(bldc_window: BLDCWindow, _):
    """Draw the central axle circle."""
    theta = np.linspace(0, 2 * np.pi, 60, endpoint=False)
    x = bldc_window.ui.axle_radius_lineedit.get_mm_value() * np.cos(theta)
    y = bldc_window.ui.axle_radius_lineedit.get_mm_value() * np.sin(theta)
    x = np.append(x, x[0])
    y = np.append(y, y[0])
    pen_width = 2
    bldc_window.ui.stator_plot_widget.plot(x, y, pen=pg.mkPen("#000000", width=pen_width))

def draw_magnets(bldc_window: BLDCWindow, _):
    """Draw magnets on the outrunner with thickness toward the stator."""
    magnet_outer_radius = bldc_window.ui.radius_lineedit.get_mm_value() - bldc_window.ui.outrunner_thickness_lineedit.get_mm_value()
    magnet_inner_radius = magnet_outer_radius - bldc_window.ui.magnet_thickness_lineedit.get_mm_value()
    num_magnets = bldc_window.ui.num_magnets_lineedit.get_value()
    magnet_arc = 2 * np.pi / num_magnets
    all_x, all_y = [], []
    for i in range(int(num_magnets)):
        magnet_angle = i * (2 * np.pi / num_magnets)
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
        all_x.extend(x_magnet)
        all_y.extend(y_magnet)
        all_x.append(np.nan)
        all_y.append(np.nan)
    pen_width = 2
    bldc_window.ui.stator_plot_widget.plot(all_x, all_y, pen=pg.mkPen("#C0C0C0", width=pen_width))

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
    r_outer = (
        bldc_window.ui.radius_lineedit.get_mm_value()
        - bldc_window.ui.outrunner_thickness_lineedit.get_mm_value()
        - bldc_window.ui.air_gap_lineedit.get_mm_value()
        - bldc_window.ui.magnet_thickness_lineedit.get_mm_value()
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
            r_inner * np.cos(q)
            + drill_bit_radius * np.sin(q)
            + slot_width_half * np.sin(q)
        )
        quarter_center_y = (
            r_inner * np.sin(q)
            - drill_bit_radius * np.cos(q)
            - slot_width_half * np.cos(q)
        )
        theta_quarter_start = np.linspace(q + np.pi / 2 - np.pi / (2 * 20), q, 10, endpoint=False)
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
        theta_half_left = np.linspace(q + 2 * np.pi - np.pi / (2 * 30), q + np.pi, 15, endpoint=False)
        x_half_left = half_center_x_left - (drill_bit_radius * np.sin(theta_half_left))
        y_half_left = half_center_y_left + (drill_bit_radius * np.cos(theta_half_left))
        half_center_x_right = x_right[-1] - drill_bit_radius * np.cos(q + np.pi / 2)
        half_center_y_right = y_right[-1] - drill_bit_radius * np.sin(q + np.pi / 2)
        theta_half_right = np.linspace(q + 2 * np.pi - np.pi / (2 * 30), q + np.pi, 15, endpoint=False)
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
        theta_quarter_end = np.linspace(q + np.pi + np.pi / (2 * 20), q + np.pi / 2, 10, endpoint=False)
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