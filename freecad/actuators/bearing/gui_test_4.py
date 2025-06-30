import math
from math import sin, cos, pi, sqrt, atan2
import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QRadioButton, QButtonGroup, QPushButton, QCheckBox
from PySide2.QtCore import Qt
import pyqtgraph as pg
import numpy as np
from freecad.actuators.compiled_ui.length_ui import QLengthEdit
from freecad.actuators.compiled_ui.angle_ui import QAngleEdit

from typing import Callable, List, Optional
from scipy.optimize import brentq
from dataclasses import dataclass

@dataclass
class ParametricDrawFunction(object):
    func: Callable[[float], float]  # callback function
    func_range: List[float]  # [start, end] range, inclusive
    num: int  # number of elements

def adj_range_for_height(func, height, func_range, num=50):
    def g(x): return func(x) - height

    min_range, max_range = func_range

    r = np.linspace(min_range, max_range, num)
    min_x = float('inf')
    max_x = -float('inf')
    for a, b in zip(r, r[1:]):
        if g(a) * g(b) < 0:
            x = brentq(g, a, b)
            if x<min_x:
                min_x = x
            if x>max_x:
                max_x = x
    if min_x ==float('inf') and max_x == -float('inf'):
        return None
    return [min_x, max_x]

def circle_groove(radius, num, height):
    def callback(x):
        return sqrt(radius**2 - x**2)
    func_range = adj_range_for_height(callback, height,[-radius, radius], 3)
    return ParametricDrawFunction( callback, func_range, num )

def circle_bearing(radius, num):
    def callback(x):
        return sqrt(radius**2 - x**2)
    func_range = [-radius, radius]
    return ParametricDrawFunction( callback, func_range, num )

def crowned_tapered_radius(x, l, delta, zeta, r_left, r_right, r_fillet):
    """
    Compute the crowned and tapered roller radius at a given x position,
    with fillets applied at both ends to smooth the transition.

    Parameters:
    - x (float): Position along the roller, where 0 is the center (range: [-l/2, l/2])
    - l (float): Total roller length (mm)
    - delta (float): Total crown drop at both ends (mm)
    - zeta (float): Crowning shape parameter (affects curvature shape)
    - r_left (float): Radius at the left end (x = -l/2)
    - r_right (float): Radius at the right end (x = +l/2)
    - r_fillet (float): Fillet radius (mm), controls how much rounding occurs at both ends

    Returns:
    - float: Final crowned and filleted radius at position x
    """
    alpha_rad = math.atan2((r_left - r_right),l)
    r_mid = (r_left + r_right)/2
    h = (delta / 2.0) * np.log(1 + zeta * (2 * x / l) ** 2)
    r_base = r_mid + x * math.tan(alpha_rad)  # Base radius at x
    r_crowned = r_base - h  # Adjusted radius
    fillet_dist = math.tan(alpha_rad)*r_fillet
    if r_left>r_right:
        fillet_left = r_fillet-fillet_dist
        fillet_right = r_fillet+fillet_dist
    else:
        fillet_left = r_fillet + fillet_dist
        fillet_right = r_fillet - fillet_dist
    if x+l/2 < fillet_left:
        fillet_x = x+l/2-r_fillet
        r_out = r_crowned - (-np.sqrt(r_fillet ** 2 - fillet_x ** 2)+r_fillet)
    elif -fillet_right < x-l/2 <= 0:
        fillet_x = x-l/2+r_fillet
        r_out = r_crowned - (-np.sqrt(r_fillet ** 2 - fillet_x ** 2)+r_fillet)
    else:
        r_out = r_crowned

    return r_out

def simple_tapered_radius(x, l, r_left, r_right):
    """
    Compute crowned tapered roller radius values at given x positions.

    Parameters:
    - x_values (array-like): x positions along the roller length (0 to L)
    - L (float): Roller length (mm)
    - delta (float): Crown drop at ends (mm)
    - zeta (float): Shape parameter for crowning
    - R_small (float): Radius at small end (mm)
    - alpha_deg (float): Taper angle (degrees)

    Returns:
    - numpy.ndarray: Crowned radius values at each x
    """
    alpha_rad = math.atan2((r_left - r_right),l)
    r_mid = (r_left + r_right)/2
    #h = (delta / 2.0) * np.log(1 + zeta * (2 * x / l) ** 2)
    r_base = r_mid + x * math.tan(alpha_rad)  # Base radius at x
    #r_crowned = r_base - h  # Adjusted radius
    return r_base

def roller_groove(l, r_left, r_right, num, height):
    callback = lambda x: simple_tapered_radius(x, l, r_left, r_right)
    func_range = adj_range_for_height(callback, height,[-l/2, l/2], 3)
    if func_range is None:
        func_range = [-l/2, l/2]
    return ParametricDrawFunction( callback, func_range, num )

def roller_bearing(l, delta, zeta, r_left, r_right, r_fillet, num):
    callback = lambda x: crowned_tapered_radius(x, l, delta, zeta, r_left, r_right, r_fillet)
    func_range = [-l/2, l/2]
    return ParametricDrawFunction( callback, func_range, num )


class PlotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interactive Bearing Plot")
        self.setGeometry(100, 100, 800, 600)

        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # PyQtGraph plot widget
        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)
        self.plot_widget.setAspectLocked(True)
        self.plot_widget.setXRange(-17, 12)  # Adjusted for inner_diameter=5 default
        self.plot_widget.setYRange(-2, 12)
        self.plot_widget.setBackground("w")

        # Validity indicator
        self.validity_label = QLabel("Inscribed Shape: Valid")
        self.validity_label.setStyleSheet("background-color: green; color: white; padding: 5px;")
        layout.addWidget(self.validity_label)

        # ef slice indicator
        self.ef_label = QLabel("Inscribed slice: valid")
        self.ef_label.setStyleSheet("background-color: green; color: white; padding: 5px;")
        layout.addWidget(self.ef_label)

        # slice indicator
        self.slice_label = QLabel("bbox slice: use kl")
        self.slice_label.setStyleSheet("background-color: green; color: white; padding: 5px;")
        layout.addWidget(self.slice_label)

        # Radio buttons for split selection
        self.split_group = QButtonGroup()
        self.bbox_radio = QRadioButton("Split Bounding Box")
        self.inscribed_radio = QRadioButton("Split Inscribed Rectangle")
        self.split_group.addButton(self.bbox_radio, 1)
        self.split_group.addButton(self.inscribed_radio, 2)
        self.bbox_radio.setChecked(True)
        layout.addWidget(self.bbox_radio)
        layout.addWidget(self.inscribed_radio)

        # Checkbox for locking bearing heights
        self.lock_heights_checkbox = QCheckBox("Lock Bearing Heights")
        self.lock_heights_checkbox.toggled.connect(self.toggle_bearing_heights)
        layout.addWidget(self.lock_heights_checkbox)

        # Gap input
        self.gap_edit = QLengthEdit()
        self.gap_edit.set_display_unit("mm")
        self.gap_edit.set_mm_value(1.0)  # 100/100 from slider
        layout.addWidget(QLabel("Gap Distance (mm)"))
        layout.addWidget(self.gap_edit)

        # Bearing width input
        self.bearing_width_edit = QLengthEdit()
        self.bearing_width_edit.set_display_unit("mm")
        self.bearing_width_edit.set_mm_value(2.0)  # 200/100 from slider
        layout.addWidget(QLabel("Bearing Width (mm)"))
        layout.addWidget(self.bearing_width_edit)

        # Groove extra input
        self.groove_extra_edit = QLengthEdit()
        self.groove_extra_edit.set_display_unit("mm")
        self.groove_extra_edit.set_mm_value(0.5)  # 50/100 from slider
        layout.addWidget(QLabel("Groove Extra (mm)"))
        layout.addWidget(self.groove_extra_edit)

        # Bearing height 1 input
        self.groove_depth_1_edit = QLengthEdit()
        self.groove_depth_1_edit.set_display_unit("mm")
        self.groove_depth_1_edit.set_mm_value(0.5)  # 50/100 from slider
        layout.addWidget(QLabel("Bearing Height 1 (mm)"))
        layout.addWidget(self.groove_depth_1_edit)

        # Bearing height 2 input
        self.groove_depth_2_edit = QLengthEdit()
        self.groove_depth_2_edit.set_display_unit("mm")
        self.groove_depth_2_edit.set_mm_value(0.5)  # 50/100 from slider
        layout.addWidget(QLabel("Bearing Height 2 (mm)"))
        layout.addWidget(self.groove_depth_2_edit)

        # Inner diameter input
        self.inner_diameter_edit = QLengthEdit()
        self.inner_diameter_edit.set_display_unit("mm")
        self.inner_diameter_edit.set_mm_value(5.0)  # 500/100 from slider
        layout.addWidget(QLabel("Inner Diameter (mm)"))
        layout.addWidget(self.inner_diameter_edit)

        # Theta input
        self.theta_edit = QAngleEdit()
        self.theta_edit.set_display_unit("deg")
        self.theta_edit.set_degrees_value(0.7854 * 180 / pi)  # pi/4 radians from slider (78/100)
        layout.addWidget(QLabel("Theta (radians)"))
        layout.addWidget(self.theta_edit)

        # w2 input
        self.w2_edit = QLengthEdit()
        self.w2_edit.set_display_unit("mm")
        self.w2_edit.set_mm_value(10.0)  # 10 from slider
        layout.addWidget(QLabel("w2 (mm)"))
        layout.addWidget(self.w2_edit)

        # h2 input
        self.h2_edit = QLengthEdit()
        self.h2_edit.set_display_unit("mm")
        self.h2_edit.set_mm_value(5.0)  # 5 from slider
        layout.addWidget(QLabel("h2 (mm)"))
        layout.addWidget(self.h2_edit)

        # AutoRange button
        self.auto_range_button = QPushButton("Zoom to Fit")
        self.auto_range_button.clicked.connect(self.auto_range)
        layout.addWidget(self.auto_range_button)

        # Connect inputs to update function
        self.theta_edit.textChanged.connect(self.update_plot)
        self.w2_edit.textChanged.connect(self.update_plot)
        self.h2_edit.textChanged.connect(self.update_plot)
        self.gap_edit.textChanged.connect(self.update_plot)
        self.bearing_width_edit.textChanged.connect(self.update_plot)
        self.groove_extra_edit.textChanged.connect(self.update_plot)
        self.groove_depth_1_edit.textChanged.connect(self.update_plot)
        self.groove_depth_2_edit.textChanged.connect(self.update_plot)
        self.inner_diameter_edit.textChanged.connect(self.update_plot)
        self.split_group.buttonClicked.connect(self.update_plot)

        # Initial plot items
        self.bounding_plot = self.plot_widget.plot(pen='#005')
        self.inscribed_plot = self.plot_widget.plot(pen='#500')
        self.points_plot = self.plot_widget.plot(symbol='o', symbolPen=None, symbolBrush='#a22', symbolSize=10)
        self.slice2_plot = self.plot_widget.plot(pen=pg.mkPen('#550', style=Qt.DashLine))
        self.slice1_plot = self.plot_widget.plot(pen=pg.mkPen('#050', style=Qt.SolidLine))

        # Initial plot
        self.update_plot()

    def auto_range(self):
        self.plot_widget.autoRange()

    def toggle_bearing_heights(self, checked):
        if checked:
            self.groove_depth_2_edit.set_mm_value(self.groove_depth_1_edit.get_mm_value())
            self.groove_depth_2_edit.setEnabled(False)
        else:
            self.groove_depth_2_edit.setEnabled(True)
        self.update_plot()

    def _calc_bbox_and_inscribed(self, theta, w2, h2):
        t = theta
        flip_x = False
        if pi > t > pi / 2:
            t = theta = pi - t
            flip_x = True
        sin_t, cos_t = sin(t), cos(t)
        if abs(theta - pi / 4) < 0.0001:
            if w2 == h2:
                w1 = h2 / sqrt(2)
                h1 = w2 / sqrt(2)
            else:
                w1 = w2 * 2
                h1 = h2 * 2
        else:
            sec_2t = 1 / cos(2 * t)
            h1 = sec_2t * (h2 * cos_t - w2 * sin_t)
            w1 = sec_2t * (w2 * cos_t - h2 * sin_t)

        i = (0, 0)
        g = (0, h2)
        h = (w2, h2)
        j = (w2, 0)

        c = (sin_t * h1, 0)
        a = (0, cos_t * h1)
        b = (cos_t * w1, h2)
        d = (w2, sin_t * w1)

        inscribed = [c, d, b, a]
        bbox = [i, j, h, g]

        return inscribed, bbox, h1, w1, flip_x, theta

    def bbox_line_intersection(self, p1, p2, x_min, x_max, y_min, y_max, t_min=0, t_max=1):
        x1, y1 = p1
        x2, y2 = p2
        intersections = []
        if abs(x2 - x1) > 1e-10:
            t = (x_min - x1) / (x2 - x1)
            if t_min <= t <= t_max:
                y = y1 + t * (y2 - y1)
                if y_min <= y <= y_max:
                    intersections.append((x_min, y))
        if abs(x2 - x1) > 1e-10:
            t = (x_max - x1) / (x2 - x1)
            if t_min <= t <= t_max:
                y = y1 + t * (y2 - y1)
                if y_min <= y <= y_max:
                    intersections.append((x_max, y))
        if abs(y2 - y1) > 1e-10:
            t = (y_min - y1) / (y2 - y1)
            if t_min <= t <= t_max:
                x = x1 + t * (x2 - x1)
                if x_min <= x <= x_max:
                    intersections.append((x, y_min))
        if abs(y2 - y1) > 1e-10:
            t = (y_max - y1) / (y2 - y1)
            if t_min <= t <= t_max:
                x = x1 + t * (x2 - x1)
                if x_min <= x <= x_max:
                    intersections.append((x, y_max))
        return intersections

    def line_line_intersection(self, a, b, c, d, t_min=None, t_max=None):
        ax, ay = a
        bx, by = b
        cx, cy = c
        dx, dy = d
        r = (bx - ax, by - ay)
        s = (dx - cx, dy - cy)
        cross_r_s = r[0] * s[1] - r[1] * s[0]
        if cross_r_s == 0:
            return None
        c_minus_a = (cx - ax, cy - ay)
        t = (c_minus_a[0] * s[1] - c_minus_a[1] * s[0]) / cross_r_s
        if t_min is not None and t_max is not None and (t > t_max or t < t_min):
            return None
        intersection = (ax + t * r[0], ay + t * r[1])
        return intersection

    def ensure_inscribed(self, inscribed, w2, h2):
        c, d, b, a = inscribed
        new_points = [c, d, b, a]
        sides = [(c, d), (d, b), (b, a), (a, c)]
        for p1, p2 in sides:
            intersects = self.bbox_line_intersection(p1, p2, 0, w2, 0, h2)
            for point in intersects:
                if point not in new_points:
                    new_points.append(point)
        new_points = new_points[4:]

        re_inscribed = False
        if len(new_points) >= 4:
            re_inscribed = True
            new_points.sort(key=lambda p: (p[1], p[0]))
            c, d = new_points[:2]
            new_points.sort(key=lambda p: (-p[1], p[0]))
            b, a = new_points[:2]

        inscribed = [c, d, b, a]
        return inscribed, re_inscribed

    def get_ef_kl_mn_lines(self, h1, w1, h2, w2, theta, inscribed_is_invalid):
        sin_t = sin(theta)
        cos_t = cos(theta)
        e = (h1 * sin_t / 2, h1 * cos_t / 2)
        f = ((w1 * cos_t + w2) / 2, (w1 * sin_t + h2) / 2)

        if inscribed_is_invalid:
            center_x = w2 / 2
            center_y = h2 / 2
            e = (center_x - h1 * cos_t / 2, center_y - h1 * sin_t / 2)
            f = (center_x + h1 * cos_t / 2, center_y + h1 * sin_t / 2)

        ex, ey = e
        fx, fy = f
        k_y = ey + (0 - ex) * (fy - ey) / (fx - ex) if abs(fx - ex) > 1e-10 else -1
        l_y = ey + (w2 - ex) * (fy - ey) / (fx - ex) if abs(fx - ex) > 1e-10 else h2 + 1
        k = (0, k_y)
        l = (w2, l_y)

        m_x = ex + (0 - ey) * (fx - ex) / (fy - ey) if abs(fy - ey) > 1e-10 else -1
        n_x = ex + (h2 - ey) * (fx - ex) / (fy - ey) if abs(fy - ey) > 1e-10 else w2 + 1
        m = (m_x, 0)
        n = (n_x, h2)

        return e, f, k, l, m, n

    def get_split_and_gap_lines(self, e, f, k, l, m, n, theta, kl_valid, gap):
        if self.inscribed_radio.isChecked():
            sel1_x, sel1_y = e
            sel2_x, sel2_y = f
        elif kl_valid:
            sel1_x, sel1_y = k
            sel2_x, sel2_y = l
        else:
            sel1_x, sel1_y = m
            sel2_x, sel2_y = n

        # Parallel lines at gap distance
        gap_cos = gap * cos(theta)
        gap_sin = gap * sin(theta)
        line1_a = [sel1_x - gap_sin, sel1_y + gap_cos]
        line1_b = [sel2_x - gap_sin, sel2_y + gap_cos]
        line2_a = [sel1_x + gap_sin, sel1_y - gap_cos]
        line2_b = [sel2_x + gap_sin, sel2_y - gap_cos]

        return line1_a, line1_b, line2_a, line2_b, sel1_x, sel1_y, sel2_x, sel2_y

    def get_split_shapes(self, line1_a, line1_b, line2_a, line2_b, w2, h2, inscribed, bbox, inscribed_is_invalid):
        c, d, b, a = inscribed
        i, j, h, g = bbox
        split_shapes = []
        line1_inters = []
        line2_inters = []
        if self.bbox_radio.isChecked():
            line1_inters = self.bbox_line_intersection(line1_a, line1_b, 0, w2, 0, h2, -100, 100)
            line2_inters = self.bbox_line_intersection(line2_a, line2_b, 0, w2, 0, h2, -100, 100)

            if len(line1_inters) == 2 and len(line2_inters) == 2:
                line1_inters = sorted(line1_inters, key=lambda x: x[0])
                line2_inters = sorted(line2_inters, key=lambda x: x[0])

                if h[1] > line1_inters[1][1]:
                    t1_split = [line1_inters[0], line1_inters[1], h, g]
                elif i[0] < line1_inters[0][0]:
                    t1_split = [line1_inters[0], line1_inters[1], g, i]
                else:
                    t1_split = [line1_inters[0], line1_inters[1], g]

                if line2_inters[1][0] < h[0]:
                    br_split = [line2_inters[1], line2_inters[0], j, h]
                elif i[1] < line2_inters[0][1]:
                    br_split = [line2_inters[1], line2_inters[0], i, j]
                else:
                    br_split = [line2_inters[1], line2_inters[0], j]

                split_shapes = [t1_split, br_split]
        elif not self.bbox_radio.isChecked() and not inscribed_is_invalid:
            line1_inters.append(self.line_line_intersection(line1_a, line1_b, a, c))
            line1_inters.append(self.line_line_intersection(line1_a, line1_b, b, d))
            line2_inters.append(self.line_line_intersection(line2_a, line2_b, a, c))
            line2_inters.append(self.line_line_intersection(line2_a, line2_b, b, d))

            if (None not in line1_inters) and (None not in line2_inters):
                line1_inters = sorted(line1_inters, key=lambda x: x[0])
                line2_inters = sorted(line2_inters, key=lambda x: x[0])

                top_split = [line1_inters[0], line1_inters[1], b, a]
                bottom_split = [line2_inters[1], line2_inters[0], c, d]

                split_shapes = [top_split, bottom_split]
        return split_shapes

    def calc_split_points(self, theta, w2, h2, gap, outer_para: ParametricDrawFunction, bearing_para: ParametricDrawFunction, inner_diameter, para_inner:Optional[ParametricDrawFunction]=None):
        inscribed, bbox, h1, w1, flip_x, theta = self._calc_bbox_and_inscribed(theta, w2, h2)
        c,d,b,a = inscribed
        i, j, h, g = bbox

        points_outside = any(p[0] < 0 or p[0] > w2 or p[1] > h2 for p in [c, d, b, a])

        if points_outside:
            inscribed, re_inscribed = self.ensure_inscribed(inscribed, w2, h2)
        else:
            re_inscribed = False
        c,d,b,a = inscribed

        inscribed_is_invalid = points_outside and not re_inscribed

        e, f, k, l, m, n = self.get_ef_kl_mn_lines(h1, w1, h2, w2, theta, inscribed_is_invalid)

        # Validity checks
        ef_valid = not any(p[0] < 0 or p[0] > w2 or p[1]<0 or p[1] > h2 for p in [e, f])
        kl_valid = not any(p[0] < 0 or p[0] > w2 or p[1]<0 or p[1] > h2 for p in [k, l])
        mn_valid = not any(p[0] < 0 or p[0] > w2 or p[1]<0 or p[1] > h2 for p in [m, n])

        line1_a, line1_b, line2_a, line2_b, sel1_x, sel1_y, sel2_x, sel2_y = self.get_split_and_gap_lines(e, f, k, l, m, n, theta, kl_valid, gap)

        # Determine split shapes
        split_shapes = self.get_split_shapes(line1_a, line1_b, line2_a, line2_b, w2, h2, inscribed, bbox, inscribed_is_invalid)


        # Add groove to split shapes
        split_mid = ((sel1_x + sel2_x) / 2, (sel1_y + sel2_y) / 2)

        # Compute direction vector of the splitting line (sel1 to sel2)
        split_dx = sel2_x - sel1_x
        split_dy = sel2_y - sel1_y
        split_length = sqrt(split_dx ** 2 + split_dy ** 2)
        # Compute perpendicular vector (counterclockwise 90-degree rotation)
        split_unit_x = split_dx / split_length
        split_unit_y = split_dy / split_length
        perp_unit_x = -split_dy / split_length
        perp_unit_y = split_dx / split_length

        # Define perpendicular line through split_mid (extend infinitely)
        perp_a = (split_mid[0] - perp_unit_x, split_mid[1] - perp_unit_y)
        perp_b = (split_mid[0] + perp_unit_x, split_mid[1] + perp_unit_y)



        para_pts = []
        shape_01s = []
        for i_s, shape in enumerate(split_shapes):
            if len(shape) < 3:
                continue

            shape_01s.append(shape[0:2])  # copy here since we're modifying the list
            # First line points
            p1, p2 = shape_01s[i_s][0], shape_01s[i_s][1]

            # Find intersection of perpendicular line with the shape's first line
            intersection = self.line_line_intersection(perp_a, perp_b, p1, p2, t_min=-float('inf'), t_max=float('inf'))
            if intersection is None:
                # Fallback to geometric midpoint if no intersection
                mid_x = (p1[0] + p2[0]) / 2
                mid_y = (p1[1] + p2[1]) / 2
            else:
                mid_x, mid_y = intersection

            # Compute unit vector along the shape's first line
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            length = sqrt(dx ** 2 + dy ** 2)
            if length == 0:
                continue
            unit_x = dx / length
            unit_y = dy / length

            if outer_para.func_range[0] <-length/2 or outer_para.func_range[0] > length/2:
                outer_para.func_range = [-length / 2, length / 2]

            # Compute groove start and end points
            groove_start = (mid_x + unit_x * outer_para.func_range[0], mid_y + unit_y * outer_para.func_range[0])
            groove_end = (mid_x + unit_x * outer_para.func_range[1], mid_y + unit_y * outer_para.func_range[1])

            # Compute perpendicular vector (counterclockwise 90-degree rotation)
            if i_s % 2 == 0:
                perp_x = -unit_y
                perp_y = unit_x
                f_lin = np.linspace(outer_para.func_range[0], outer_para.func_range[1], outer_para.num)
            else:
                unit_x = -unit_x
                unit_y = -unit_y
                perp_x = unit_y
                perp_y = -unit_x
                f_lin = np.linspace(outer_para.func_range[1], outer_para.func_range[0], outer_para.num)

            pts = []
            for x in f_lin:
                y = outer_para.func(x)
                #if x==para.func_range[0] or x==para.func_range[1] and y==gap:
                #    continue

                pt = [
                    mid_x + unit_x * x + perp_x * (y-gap),
                    mid_y + unit_y * x + perp_y * (y-gap)
                ]

                pts.append(pt)

            # Adjust for bottom shape direction (reverse groove points)
            if np.allclose(outer_para.func_range, [-length / 2, length / 2]): #and np.allclose([pts[0], pts[-1]], [p1, shape[1]]):
                new_points = [*pts] + shape[2:]
            else:
                if not np.allclose(pts[0], groove_start):
                    pts = [groove_start] + pts
                if not np.allclose(pts[-1], groove_end):
                    pts = pts + [groove_end]
                new_points = [p1, *pts] + shape[1:]
            para_pts.append(pts)

            split_shapes[i_s] = new_points

        inset_shapes = []
        if para_inner is not None:
            for i_s, shape in enumerate(split_shapes):
                if len(shape) < 3:
                    continue

                # First line points
                p1, p2 = shape_01s[i_s][0], shape_01s[i_s][1]

                # Find intersection of perpendicular line with the shape's first line
                intersection = self.line_line_intersection(perp_a, perp_b, p1, p2, t_min=-float('inf'),
                                                           t_max=float('inf'))
                if intersection is None:
                    # Fallback to geometric midpoint if no intersection
                    mid_x = (p1[0] + p2[0]) / 2
                    mid_y = (p1[1] + p2[1]) / 2
                else:
                    mid_x, mid_y = intersection

                # Compute unit vector along the shape's first line
                dx = p2[0] - p1[0]
                dy = p2[1] - p1[1]
                length = sqrt(dx ** 2 + dy ** 2)
                if length == 0:
                    continue
                unit_x = dx / length
                unit_y = dy / length

                if para_inner.func_range[0] < -length / 2 or para_inner.func_range[0] > length / 2:
                    para_inner.func_range = [-length / 2, length / 2]

                # Compute groove start and end points

                # Compute perpendicular vector (counterclockwise 90-degree rotation)
                if i_s%2==0:
                    perp_x = -unit_y
                    perp_y = unit_x
                    f_lin = np.linspace(outer_para.func_range[1], outer_para.func_range[0], outer_para.num)
                else:
                    unit_x=-unit_x
                    unit_y=-unit_y
                    perp_x = unit_y
                    perp_y = -unit_x
                    f_lin = np.linspace(outer_para.func_range[0], outer_para.func_range[1], outer_para.num)

                pts = []
                for x in f_lin:
                    y = para_inner.func(x)
                    pt = [
                        mid_x + unit_x * x + perp_x * (y - gap),
                        mid_y + unit_y * x + perp_y * (y - gap)
                    ]

                    pts.append(pt)

                inset_shapes.append(para_pts[i_s] + pts + para_pts[i_s][0:1])

        if kl_valid:
            p1, p2 = k, l
        elif mn_valid:
            p1, p2 = m, n
        else:
            raise RuntimeError("Neither kl nor mn valid. Shouldn't be mathematically possible.")

        # Find intersection of perpendicular line with the shape's first line
        intersection = self.line_line_intersection(perp_a, perp_b, p1, p2, t_min=-float('inf'), t_max=float('inf'))
        if intersection is None:
            # Fallback to geometric midpoint if no intersection
            mid_x = (p1[0] + p2[0]) / 2
            mid_y = (p1[1] + p2[1]) / 2
        else:
            mid_x, mid_y = intersection
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        length = sqrt(dx ** 2 + dy ** 2)
        # if length == 0:  # idk, you deserve your div 0 here
        unit_x = dx / length
        unit_y = dy / length

        if bearing_para.func_range[0] < -length / 2 or bearing_para.func_range[0] > length / 2:
            bearing_para.func_range = [-length / 2, length / 2]

        # Compute perpendicular vector (counterclockwise 90-degree rotation)
        perp_x = unit_y
        perp_y = -unit_x

        bearing = []
        for x in np.linspace(bearing_para.func_range[1], bearing_para.func_range[0], bearing_para.num):
            y = bearing_para.func(x)
            pt = [
                mid_x + unit_x * x + perp_x * y,
                mid_y + unit_y * x + perp_y * y
            ]

            bearing.append(pt)

        # flip base
        #unit_y=-unit_y
        #unit_x=-unit_x
        perp_x = -unit_y
        perp_y = unit_x

        for x in np.linspace(bearing_para.func_range[0], bearing_para.func_range[1], bearing_para.num):
            y = bearing_para.func(x)
            pt = [
                mid_x + unit_x * x + perp_x * y,
                mid_y + unit_y * x + perp_y * y
            ]

            bearing.append(pt)


        if flip_x:
            inscribed = [[-x[0]+w2, x[1]] for x in inscribed]
            bbox = [[-x[0]+w2, x[1]] for x in bbox]
            e = [-e[0]+w2, e[1]]
            f = [-f[0]+w2, f[1]]
            k = [-k[0] + w2, k[1]]
            l = [-l[0] + w2, l[1]]
            m = [-m[0] + w2, m[1]]
            n = [-n[0] + w2, n[1]]
            split_shapes = [[[-x[0] + w2, x[1]] for x in s] for s in split_shapes]
            inset_shapes = [[[-x[0] + w2, x[1]] for x in s] for s in inset_shapes]
            bearing = [(-x[0]+w2, x[1]) for x in bearing]

        # Mirror shapes and points
        mirror_inscribed = [(-xy[0] - inner_diameter, xy[1]) for xy in inscribed]
        mirror_bbox = [(-xy[0] - inner_diameter, xy[1]) for xy in bbox]
        mirror_ef = [(-xy[0] - inner_diameter, xy[1]) for xy in [e, f]]
        mirror_kl = [(-xy[0] - inner_diameter, xy[1]) for xy in [k, l]]
        mirror_mn = [(-xy[0] - inner_diameter, xy[1]) for xy in [m, n]]
        mirror_split_shapes = []
        for shape in split_shapes:
            mirror_shape = [(-xy[0] - inner_diameter, xy[1]) for xy in shape]
            mirror_split_shapes.append(mirror_shape)

        mirror_insets = []
        for shape in inset_shapes:
            mirror_shape = [(-xy[0] - inner_diameter, xy[1]) for xy in shape]
            mirror_insets.append(mirror_shape)

        mirror_bearing = [(-xy[0] - inner_diameter, xy[1]) for xy in bearing]


        return inscribed, bbox, [e,f], [k,l], [m,n], split_shapes, inset_shapes, bearing, inscribed_is_invalid, ef_valid, kl_valid, mn_valid, mirror_inscribed, mirror_bbox, mirror_ef, mirror_kl, mirror_mn, mirror_split_shapes, mirror_insets, mirror_bearing

    def update_plot(self):
        self.plot_widget.clear()
        deg = self.theta_edit.get_degrees_value()
        if deg<0:
            deg +=180
        elif deg>=180:
            deg -=180
        self.theta_edit.set_degrees_value(deg)

        theta = self.theta_edit.get_degrees_value() * pi / 180  # Convert degrees to radians


        w2 = self.w2_edit.get_mm_value()
        h2 = self.h2_edit.get_mm_value()
        gap = self.gap_edit.get_mm_value()
        bearing_width = self.bearing_width_edit.get_mm_value()
        groove_extra = self.groove_extra_edit.get_mm_value()
        groove_depth_1 = self.groove_depth_1_edit.get_mm_value()
        groove_depth_2 = self.groove_depth_1_edit.get_mm_value() if self.lock_heights_checkbox.isChecked() else self.groove_depth_2_edit.get_mm_value()
        inner_diameter = self.inner_diameter_edit.get_mm_value()
        inset_thickness = .25

        #para = circle_groove(bearing_width+groove_extra+inset_thickness, 50, gap)
        #para_inner = circle_groove(bearing_width+groove_extra, 50, gap)
        #para_bearing = circle_bearing(bearing_width, 50)

        bearing_angle = math.atan2((groove_depth_1-groove_depth_2), bearing_width)
        bearing_avg = (groove_depth_1+groove_depth_2)/2
        extra_d1 = bearing_avg+math.tan(bearing_angle)*(bearing_width+groove_extra)/2
        extra_d2 = bearing_avg-math.tan(bearing_angle)*(bearing_width+groove_extra)/2

        para = roller_groove(bearing_width+groove_extra, extra_d1+inset_thickness, extra_d2+inset_thickness, 250, gap)
        para_inner = roller_groove(bearing_width+groove_extra,  extra_d1, extra_d2, 50, gap)
        para_bearing = roller_bearing(bearing_width, .1, .1, groove_depth_1, groove_depth_2, .2, 250)

        inscribed, bbox, ef, kl, mn, split_shapes, inset_shapes, bearing, is_invalid, ef_valid, kl_valid, mn_valid, mirror_inscribed, mirror_bbox, mirror_ef, mirror_kl, mirror_mn, mirror_split_shapes, mirror_inset_shapes, mirror_bearing = self.calc_split_points(
            theta, w2, h2, gap, para, para_bearing, inner_diameter, para_inner
        )

        if kl_valid:
            self.slice_label.setText("slice: use kl")
            self.slice_label.setStyleSheet("background-color: green; color: white; padding: 5px;")
        elif mn_valid:
            self.slice_label.setText("slice: use mn")
            self.slice_label.setStyleSheet("background-color: green; color: white; padding: 5px;")
        else:
            self.slice_label.setText("slice: NO VALID SLICE")
            self.slice_label.setStyleSheet("background-color: red; color: white; padding: 5px;")

        if ef_valid:
            self.ef_label.setText("inscribed slice: valid")
            self.ef_label.setStyleSheet("background-color: green; color: white; padding: 5px;")
        else:
            self.ef_label.setText("Inscribed slice: Invalid (use bbox)")
            self.ef_label.setStyleSheet("background-color: red; color: white; padding: 5px;")

        # Update validity indicator
        if is_invalid:
            self.validity_label.setText("Inscribed Shape: Invalid (Using Fallback)")
            self.validity_label.setStyleSheet("background-color: red; color: white; padding: 5px;")
        else:
            self.validity_label.setText("Inscribed Shape: Valid")
            self.validity_label.setStyleSheet("background-color: green; color: white; padding: 5px;")

        self.plot_widget.clear()

        # Update bounding rectangle
        bounding_x = [0, w2, w2, 0, 0]
        bounding_y = [0, 0, h2, h2, 0]
        self.plot_widget.plot(bounding_x, bounding_y, pen='#0000FF')

        # Update mirrored bounding rectangle
        mirror_bounding_x = [-x - inner_diameter for x in [0, w2, w2, 0, 0]]
        mirror_bounding_y = [0, 0, h2, h2, 0]
        self.plot_widget.plot(mirror_bounding_x, mirror_bounding_y, pen='#0000FF')

        '''if not is_invalid:
            # Update inscribed rectangle (original points for visualization)
            c, d, b, a = inscribed
            inscribed_x = [c[0], d[0], b[0], a[0], c[0]]
            inscribed_y = [c[1], d[1], b[1], a[1], c[1]]
            self.plot_widget.plot(inscribed_x, inscribed_y, pen='#800080')

            # Update mirrored inscribed rectangle
            c, d, b, a = mirror_inscribed
            mirror_inscribed_x = [c[0], d[0], b[0], a[0], c[0]]
            mirror_inscribed_y = [c[1], d[1], b[1], a[1], c[1]]
            self.plot_widget.plot(mirror_inscribed_x, mirror_inscribed_y, pen='#800080')'''

        # Update split shapes
        if split_shapes:
            for e, shape in enumerate(split_shapes):
                if len(shape) >= 3:
                    x_coords = [p[0] for p in shape] + [shape[0][0]]
                    y_coords = [p[1] for p in shape] + [shape[0][1]]
                    pen_color = '#aa0000' if e == 0 else '#00aa00'
                    self.plot_widget.plot(x_coords, y_coords, pen=pen_color)

        # Update mirrored split shapes
        if mirror_split_shapes:
            for e, shape in enumerate(mirror_split_shapes):
                if len(shape) >= 3:
                    x_coords = [p[0] for p in shape] + [shape[0][0]]
                    y_coords = [p[1] for p in shape] + [shape[0][1]]
                    pen_color = '#aa0000' if e == 0 else '#00aa00'
                    self.plot_widget.plot(x_coords, y_coords, pen=pen_color)

        # Update split shapes
        if inset_shapes:
            for e, shape in enumerate(inset_shapes):
                if len(shape) >= 3:
                    x_coords = [p[0] for p in shape] + [shape[0][0]]
                    y_coords = [p[1] for p in shape] + [shape[0][1]]
                    pen_color = '#003300' if e == 0 else '#0000aa'
                    self.plot_widget.plot(x_coords, y_coords, pen=pen_color)

        # Update mirrored split shapes
        if mirror_inset_shapes:
            for e, shape in enumerate(mirror_inset_shapes):
                if len(shape) >= 3:
                    x_coords = [p[0] for p in shape] + [shape[0][0]]
                    y_coords = [p[1] for p in shape] + [shape[0][1]]
                    pen_color = '#003300' if e == 0 else '#0000aa'
                    self.plot_widget.plot(x_coords, y_coords, pen=pen_color)

        if bearing:
            if len(bearing) >= 3:
                x_coords = [p[0] for p in bearing] + [bearing[0][0]]
                y_coords = [p[1] for p in bearing] + [bearing[0][1]]
                pen_color = '#222222'
                self.plot_widget.plot(x_coords, y_coords, pen=pen_color)

        if mirror_bearing:
            if len(mirror_bearing) >= 3:
                x_coords = [p[0] for p in mirror_bearing] + [mirror_bearing[0][0]]
                y_coords = [p[1] for p in mirror_bearing] + [mirror_bearing[0][1]]
                pen_color = '#222222'
                self.plot_widget.plot(x_coords, y_coords, pen=pen_color)

        if not is_invalid:
            # Update points
            e, f = ef
            points_x = [e[0], f[0]]
            points_y = [e[1], f[1]]
            self.plot_widget.plot(points_x, points_y, symbol='o', symbolPen=None, symbolBrush='#FF69B4', symbolSize=10)

            # Update mirrored ef points
            e, f = mirror_ef
            points_x = [e[0], f[0]]
            points_y = [e[1], f[1]]
            self.plot_widget.plot(points_x, points_y, symbol='o', symbolPen=None, symbolBrush='#FF69B4', symbolSize=10)

        if kl_valid:
            k, l = kl
            points_x = [k[0], l[0]]
            points_y = [k[1], l[1]]
            self.plot_widget.plot(points_x, points_y, symbol='o', symbolPen=None, symbolBrush='#8B0000', symbolSize=10)

            # Update mirrored kl points
            k, l = mirror_kl
            points_x = [k[0], l[0]]
            points_y = [k[1], l[1]]
            self.plot_widget.plot(points_x, points_y, symbol='o', symbolPen=None, symbolBrush='#8B0000', symbolSize=10)

        if mn_valid:
            m, n = mn
            points_x = [m[0], n[0]]
            points_y = [m[1], n[1]]
            self.plot_widget.plot(points_x, points_y, symbol='o', symbolPen=None, symbolBrush='#5C4033', symbolSize=10)

            # Update mirrored mn points
            m, n = mirror_mn
            points_x = [m[0], n[0]]
            points_y = [m[1], n[1]]
            self.plot_widget.plot(points_x, points_y, symbol='o', symbolPen=None, symbolBrush='#5C4033', symbolSize=10)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PlotWindow()
    window.show()
    sys.exit(app.exec_())