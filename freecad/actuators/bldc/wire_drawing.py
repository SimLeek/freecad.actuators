"""
Wire placement and collision detection functions for BLDC motor visualization.
"""
import numpy as np
import pyqtgraph as pg
from freecad.actuators.util import traverse_tuple

# stop potential import loops
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main_window import BLDCWindow
else:
    from typing import Any
    BLDCWindow = Any

def draw_wires(bldc_window: BLDCWindow, pixel_per_unit):
    """Draw the wires in the stator slots as lines between left and right vectors."""
    wire_diam = bldc_window.ui.wire_diameter_lineedit.get_mm_value()
    L = bldc_window.ui.hammerhead_length_lineedit.get_mm_value()
    r_inner = bldc_window.ui.stator_inner_radius_lineedit.get_mm_value()
    r_outer = (
            bldc_window.ui.radius_lineedit.get_mm_value() -
            bldc_window.ui.outrunner_thickness_lineedit.get_mm_value() -
            bldc_window.ui.magnet_thickness_lineedit.get_mm_value() -
            bldc_window.ui.air_gap_lineedit.get_mm_value() -
            L
    )
    num_turns = int(bldc_window.ui.turns_per_slot_lineedit.get_value())
    if bldc_window.use_cache:
        try:
            turns_list = eval(bldc_window.ui.turns_per_layer_lineedit.text())
        except Exception:
            turns_list = None
    else:
        turns_list = None
    N = int(bldc_window.ui.num_slots_lineedit.get_value())
    tight_pack = bldc_window.ui.tight_pack_checkbox.isChecked()
    G = bldc_window.ui.slot_width_lineedit.get_mm_value() / 2
    collision_check_diameter = wire_diam
    if bldc_window.ui.needle_winding_checkbox.isChecked():
        collision_check_diameter += bldc_window.ui.needle_diameter_lineedit.get_mm_value()/2

    # Pens for drawing
    pen_width = wire_diam / pixel_per_unit
    needle_pen_width = bldc_window.ui.needle_diameter_lineedit.get_mm_value()/pixel_per_unit
    non_colliding_pen = pg.mkPen('#B87333', width=pen_width, cap=pg.QtCore.Qt.RoundCap)
    colliding_pen = pg.mkPen('#FF0000', width=pen_width, cap=pg.QtCore.Qt.RoundCap)
    needle_pen = pg.mkPen('#ca5cdd', width=needle_pen_width, cap=pg.QtCore.Qt.RoundCap)
    min_needle_rad = None
    max_needle_rad = r_outer + L + bldc_window.ui.air_gap_lineedit.get_mm_value()

    good_x, good_y = [], []
    bad_x, bad_y = [], []
    needle_x, needle_y = [], []

    for i in range(N):
        q = i * (360.0 / N) / 180.0 * np.pi

        # Define bin positions for loose and tight packing
        # len(bin_counts) also determines turns per layer
        if tight_pack:
            # Two sets of bins for hexagonal packing
            bin_radii_even = np.arange(r_inner, r_outer, wire_diam)
            bin_radii_odd = np.arange( r_inner + (wire_diam / 2), r_outer, wire_diam)
            bin_counts_even = [0]*len(bin_radii_even)
            bin_counts_odd = [0]*len(bin_radii_odd)
            current_bin = len(bin_counts_even) - 1
        else:
            bin_radii = np.arange(r_inner, r_outer, wire_diam)
            bin_counts = [0]*len(bin_radii)
            current_bin = len(bin_counts) - 1

        current_layer = 0
        if turns_list is None:
            turns_list = [[current_bin]]
            turn = 0
            while turn<num_turns:
                if tight_pack:
                    if current_layer > len(bin_counts_even) + len(bin_counts_odd):
                        break
                    if current_layer%2==0:
                        total_height = wire_diam*int((current_layer+1)/2) * np.sqrt(3) + collision_check_diameter
                    else:
                        total_height = wire_diam*(int((current_layer+1)/2)-1) * np.sqrt(3) + wire_diam*(np.sqrt(3) / 2) + collision_check_diameter
                else:
                    if current_layer > len(bin_counts):
                        break
                    total_height = (current_layer) * wire_diam + collision_check_diameter
                G_adjusted = G + total_height

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
                            current_layer += 1
                            if current_bin >= len(bin_counts) or is_colliding:
                                break  # Todo: add warning here: not possible to wind anymore
                            turns_list[-1].append(current_bin+1)
                            turns_list.append([current_bin])
                turn+=1
            if turn<bldc_window.ui.turns_per_slot_lineedit.get_value() and not bldc_window.ui.turns_per_slot_lock.is_locked:
                bldc_window.ui.turns_per_slot_lineedit.set_value(turn)
            if current_layer%2==0:
                turns_list[-1].append(current_bin)  # set at end of loop, iterated at start, so no plus/minus
            else:
                turns_list[-1].append(current_bin)
            bldc_window.ui.turns_per_layer_lineedit.setText(str(turns_list))
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
        if tight_pack:
            for r, bc in zip(bin_radii_even, bin_counts_even):
                if bc==0:
                    continue
                total_height = wire_diam*(bc-1)*np.sqrt(3)+collision_check_diameter

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
                middle_height = wire_diam*(bc-1)*np.sqrt(3)+wire_diam*.5
                G_adjusted = G + middle_height
                x_left = r * np.cos(q) - G_adjusted * np.sin(q)
                y_left = r * np.sin(q) + G_adjusted * np.cos(q)
                x_right = r * np.cos(q) + G_adjusted * np.sin(q)
                y_right = r * np.sin(q) - G_adjusted * np.cos(q)

                if not is_colliding:
                    good_x.extend([x_left, x_right, np.nan])
                    good_y.extend([y_left, y_right, np.nan])
                else:
                    bad_x.extend([x_left, x_right, np.nan])
                    bad_y.extend([y_left, y_right, np.nan])
            for r, bc in zip(bin_radii_odd, bin_counts_odd):
                if bc==0:
                    continue

                total_height = wire_diam*(bc - 1) * np.sqrt(3) + wire_diam*(np.sqrt(3)/2) + collision_check_diameter

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
                middle_height = wire_diam*(bc - 1) * np.sqrt(3) + wire_diam * (0.5 + np.sqrt(3) / 2)
                G_adjusted = G + middle_height
                x_left = r * np.cos(q) - G_adjusted * np.sin(q)
                y_left = r * np.sin(q) + G_adjusted * np.cos(q)
                x_right = r * np.cos(q) + G_adjusted * np.sin(q)
                y_right = r * np.sin(q) - G_adjusted * np.cos(q)

                if not is_colliding:
                    good_x.extend([x_left, x_right, np.nan])
                    good_y.extend([y_left, y_right, np.nan])
                else:
                    bad_x.extend([x_left, x_right, np.nan])
                    bad_y.extend([y_left, y_right, np.nan])
        else:
            for r, bc in zip(bin_radii, bin_counts):
                if bc==0:
                    continue
                total_height = (bc-1)*wire_diam + collision_check_diameter
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
                middle_height = (bc - 1) * wire_diam + wire_diam / 2
                G_adjusted = G + middle_height
                x_left = r * np.cos(q) - G_adjusted * np.sin(q)
                y_left = r * np.sin(q) + G_adjusted * np.cos(q)
                x_right = r * np.cos(q) + G_adjusted * np.sin(q)
                y_right = r * np.sin(q) - G_adjusted * np.cos(q)

                if not is_colliding:
                    good_x.extend([x_left, x_right, np.nan])
                    good_y.extend([y_left, y_right, np.nan])
                else:
                    bad_x.extend([x_left, x_right, np.nan])
                    bad_y.extend([y_left, y_right, np.nan])
        q_half = (i + 0.5) * (360.0 / N) / 180.0 * np.pi
        needle_x.extend([max_needle_rad*np.cos(q_half), min_needle_rad*np.cos(q_half), np.nan])
        needle_y.extend([max_needle_rad*np.sin(q_half), min_needle_rad*np.sin(q_half), np.nan])

    bldc_window.ui.stator_plot_widget.plot(good_x, good_y, pen=non_colliding_pen)
    bldc_window.ui.stator_plot_widget.plot(bad_x, bad_y, pen=colliding_pen)
    if bldc_window.ui.needle_winding_checkbox.isChecked():
        bldc_window.ui.stator_plot_widget.plot(needle_x, needle_y, pen=needle_pen)