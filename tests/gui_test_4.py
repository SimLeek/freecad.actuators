from math import sin, cos, pi, sqrt, atan2
import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider, QLabel, QRadioButton, QButtonGroup
from PySide2.QtCore import Qt
import pyqtgraph as pg
import numpy as np

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
        self.plot_widget.setXRange(-2, 12)
        self.plot_widget.setYRange(-2, 12)

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

        # Gap slider
        self.gap_slider = QSlider(Qt.Horizontal)
        self.gap_slider.setMinimum(0)
        self.gap_slider.setMaximum(500)
        self.gap_slider.setValue(100)
        layout.addWidget(QLabel("Gap Distance"))
        layout.addWidget(self.gap_slider)

        # Bearing width slider
        self.bearing_width_slider = QSlider(Qt.Horizontal)
        self.bearing_width_slider.setMinimum(1)
        self.bearing_width_slider.setMaximum(1000)
        self.bearing_width_slider.setValue(200)
        layout.addWidget(QLabel("Bearing Width"))
        layout.addWidget(self.bearing_width_slider)

        # Groove extra slider
        self.groove_extra_slider = QSlider(Qt.Horizontal)
        self.groove_extra_slider.setMinimum(0)
        self.groove_extra_slider.setMaximum(200)
        self.groove_extra_slider.setValue(50)
        layout.addWidget(QLabel("Groove Extra"))
        layout.addWidget(self.groove_extra_slider)

        # Groove depth 1 slider
        self.groove_depth_1_slider = QSlider(Qt.Horizontal)
        self.groove_depth_1_slider.setMinimum(0)
        self.groove_depth_1_slider.setMaximum(500)
        self.groove_depth_1_slider.setValue(50)
        layout.addWidget(QLabel("Bearing Height 1"))
        layout.addWidget(self.groove_depth_1_slider)

        # Groove depth 2 slider
        self.groove_depth_2_slider = QSlider(Qt.Horizontal)
        self.groove_depth_2_slider.setMinimum(0)
        self.groove_depth_2_slider.setMaximum(500)
        self.groove_depth_2_slider.setValue(50)
        layout.addWidget(QLabel("Bearing Height 2"))
        layout.addWidget(self.groove_depth_2_slider)

        # Sliders for theta, w2, h2
        self.theta_slider = QSlider(Qt.Horizontal)
        self.theta_slider.setMinimum(0)
        self.theta_slider.setMaximum(157)  # 0 to pi/2
        self.theta_slider.setValue(78)  # Start at pi/4
        layout.addWidget(QLabel("Theta (radians)"))
        layout.addWidget(self.theta_slider)

        self.w2_slider = QSlider(Qt.Horizontal)
        self.w2_slider.setMinimum(1)
        self.w2_slider.setMaximum(20)
        self.w2_slider.setValue(10)
        layout.addWidget(QLabel("w2"))
        layout.addWidget(self.w2_slider)

        self.h2_slider = QSlider(Qt.Horizontal)
        self.h2_slider.setMinimum(1)
        self.h2_slider.setMaximum(20)
        self.h2_slider.setValue(5)
        layout.addWidget(QLabel("h2"))
        layout.addWidget(self.h2_slider)

        # Connect sliders and radio buttons to update function
        self.theta_slider.valueChanged.connect(self.update_plot)
        self.w2_slider.valueChanged.connect(self.update_plot)
        self.h2_slider.valueChanged.connect(self.update_plot)
        self.gap_slider.valueChanged.connect(self.update_plot)
        self.bearing_width_slider.valueChanged.connect(self.update_plot)
        self.groove_extra_slider.valueChanged.connect(self.update_plot)
        self.groove_depth_1_slider.valueChanged.connect(self.update_plot)
        self.groove_depth_2_slider.valueChanged.connect(self.update_plot)
        self.split_group.buttonClicked.connect(self.update_plot)

        # Initial plot items
        self.bounding_plot = self.plot_widget.plot(pen='b')
        self.inscribed_plot = self.plot_widget.plot(pen='r')
        self.points_plot = self.plot_widget.plot(symbol='o', symbolPen=None, symbolBrush='pink', symbolSize=10)
        self.slice2_plot = self.plot_widget.plot(pen=pg.mkPen('y', style=Qt.DashLine))
        self.slice1_plot = self.plot_widget.plot(pen=pg.mkPen('g', style=Qt.SolidLine))

        # Initial plot
        self.update_plot()

    def calc_points(self, theta, w2, h2, gap, bearing_width, groove_extra, groove_depth_1, groove_depth_2=None):
        # Handle 45-degree edge case
        t = theta
        sin_t, cos_t = sin(t), cos(t)
        if abs(theta - pi/4) < 0.0001:
            h1 = w1 = w2 / sqrt(2)
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

        points_outside = any(p[0] < 0 or p[0] > w2 or p[1] > h2 for p in [c, d, b, a])

        def bbox_line_intersection(p1, p2, x_min, x_max, y_min, y_max, t_min=0, t_max=1):
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

        def line_line_intersection(a, b, c, d, t_min=None, t_max=None):
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

        new_points = [c, d, b, a]
        sides = [(c, d), (d, b), (b, a), (a, c)]
        for p1, p2 in sides:
            intersects = bbox_line_intersection(p1, p2, 0, w2, 0, h2)
            for point in intersects:
                if point not in new_points:
                    new_points.append(point)
        new_points = new_points[4:]

        e = (h1 * sin_t / 2, h1 * cos_t / 2)
        f = ((w1 * cos_t + w2) / 2, (w1 * sin_t + h2) / 2)

        if len(new_points) >= 4:
            new_points.sort(key=lambda p: (p[1], p[0]))
            c, d = new_points[:2]
            new_points.sort(key=lambda p: (-p[1], p[0]))
            b, a = new_points[:2]
        elif points_outside:
            center_x = w2 / 2
            center_y = h2 / 2
            e = (center_x - h1 * cos_t / 2, center_y - h1 * sin_t / 2)
            f = (center_x + h1 * cos_t / 2, center_y + h1 * sin_t / 2)

        ex, ey = e
        fx, fy = f
        k_y = ey + (0 - ex) * (fy - ey) / (fx - ex) if abs(fx - ex) > 1e-10 else ey
        l_y = ey + (w2 - ex) * (fy - ey) / (fx - ex) if abs(fx - ex) > 1e-10 else ey
        k = (0, k_y)
        l = (w2, l_y)

        m_x = ex + (0 - ey) * (fx - ex) / (fy - ey) if abs(fy - ey) > 1e-10 else ex
        n_x = ex + (h2 - ey) * (fx - ex) / (fy - ey) if abs(fy - ey) > 1e-10 else ex
        m = (m_x, 0)
        n = (n_x, h2)

        # Validity checks
        is_invalid = points_outside and not len(new_points) >= 4
        ef_valid = not any(p[0] < 0 or p[0] > w2 or p[1] > h2 for p in [e, f])
        kl_valid = not any(p[0] < 0 or p[0] > w2 or p[1] > h2 for p in [k, l])
        mn_valid = not any(p[0] < 0 or p[0] > w2 or p[1] > h2 for p in [m, n])


        # Parallel lines at gap distance
        if self.inscribed_radio.isChecked():
            sel1 = sel1_x, sel1_y = e
            sel2 = sel2_x, sel2_y = f
        elif kl_valid:
            sel1 = sel1_x, sel1_y = k
            sel2 = sel2_x, sel2_y = l
        else:
            sel1 = sel1_x, sel1_y = m
            sel2 = sel2_x, sel2_y = n

        # Parallel lines at gap distance
        gap_cos = gap * cos(theta)
        gap_sin = gap * sin(theta)
        line1_a = [sel1_x - gap_sin, sel1_y + gap_cos]
        line1_b = [sel2_x - gap_sin, sel2_y + gap_cos]
        line2_a = [sel1_x + gap_sin, sel1_y - gap_cos]
        line2_b = [sel2_x + gap_sin, sel2_y - gap_cos]

        # Determine split shapes
        split_shapes = []
        line1_inters = []
        line2_inters = []
        if self.bbox_radio.isChecked():
            line1_inters = bbox_line_intersection(line1_a, line1_b, 0, w2, 0, h2, -100, 100)
            line2_inters = bbox_line_intersection(line2_a, line2_b, 0, w2, 0, h2, -100, 100)

            if len(line1_inters)==2 and len(line2_inters)==2:
                line1_inters = sorted(line1_inters, key=lambda x:x[0])
                line2_inters = sorted(line2_inters, key=lambda x:x[0])

                if h[1]>line1_inters[1][1]:
                    t1_split = [line1_inters[0], line1_inters[1], h, g]
                elif i[0]<line1_inters[0][0]:
                    t1_split = [line1_inters[0], line1_inters[1], g, i]
                else:
                    t1_split = [line1_inters[0], line1_inters[1], g]

                if line2_inters[1][0]<h[0]:
                    br_split = [line2_inters[1], line2_inters[0], j, h]
                elif i[1]<line2_inters[0][1]:

                    br_split = [line2_inters[1], line2_inters[0], i, j]
                else:
                    br_split = [line2_inters[1], line2_inters[0], j]

                split_shapes = [t1_split, br_split]
        elif not self.bbox_radio.isChecked() and not is_invalid:
            line1_inters.append(line_line_intersection(line1_a, line1_b, a, c))
            line1_inters.append(line_line_intersection(line1_a, line1_b, b, d))
            line2_inters.append(line_line_intersection(line2_a, line2_b, a, c))
            line2_inters.append(line_line_intersection(line2_a, line2_b, b, d))

            if (None not in line1_inters) and (None not in line2_inters):
                line1_inters = sorted(line1_inters, key=lambda x: x[0])
                line2_inters = sorted(line2_inters, key=lambda x: x[0])

                top_split = [line1_inters[0], line1_inters[1], b, a]
                bottom_split = [line2_inters[1], line2_inters[0], c, d]

                split_shapes = [top_split, bottom_split]

        # Compute midpoint of the splitting line (between line1_inters and line2_inters)
        #if len(line1_inters) == 2 and len(line2_inters) == 2:
        #    split_mid_x = (line1_inters[0][0] + line1_inters[1][0] + line2_inters[0][0] + line2_inters[1][
        #        0]) / 4
        #    split_mid_y = (line1_inters[0][1] + line1_inters[1][1] + line2_inters[0][1] + line2_inters[1][
        #        1]) / 4
        #    split_mid = (split_mid_x, split_mid_y)
        #else:
        split_mid = ((sel1_x + sel2_x) / 2, (sel1_y + sel2_y) / 2)

        # Compute direction vector of the splitting line (sel1 to sel2)
        split_dx = sel2_x - sel1_x
        split_dy = sel2_y - sel1_y
        split_length = sqrt(split_dx ** 2 + split_dy ** 2)
        # Compute perpendicular vector (counterclockwise 90-degree rotation)
        perp_unit_x = -split_dy / split_length
        perp_unit_y = split_dx / split_length

        # Define perpendicular line through split_mid (extend infinitely)
        perp_a = (split_mid[0] - perp_unit_x * 1000, split_mid[1] - perp_unit_y * 1000)
        perp_b = (split_mid[0] + perp_unit_x * 1000, split_mid[1] + perp_unit_y * 1000)

        # Add groove to split shapes
        if groove_depth_2 is None:
            groove_depth_1 = groove_depth_2
        groove_length = bearing_width + 2 * groove_extra
        for i, shape in enumerate(split_shapes):
            if len(shape) < 3:
                continue

            # First line points
            p1, p2 = shape[0], shape[1]

            # Find intersection of perpendicular line with the shape's first line
            intersection = line_line_intersection(perp_a, perp_b, p1, p2, t_min=-float('inf'), t_max=float('inf'))
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

            # Compute groove start and end points
            groove_half = groove_length / 2
            groove_start = (mid_x - unit_x * groove_half, mid_y - unit_y * groove_half)
            groove_end = (mid_x + unit_x * groove_half, mid_y + unit_y * groove_half)

            # Compute perpendicular vector (counterclockwise 90-degree rotation)
            perp_x = -unit_y
            perp_y = unit_x

            # Compute groove inset points
            gd1 = groove_depth_1 if i==0 else groove_depth_2
            gd2 = groove_depth_2 if i==0 else groove_depth_1
            groove_inset_0 = (groove_start[0] + perp_x * gd1, groove_start[1] + perp_y * gd1)
            groove_inset_1 = (groove_end[0] + perp_x * gd2, groove_end[1] + perp_y * gd2)

            # Adjust for bottom shape direction (reverse groove points)
            new_points = [p1, groove_start, groove_inset_0, groove_inset_1, groove_end] + shape[1:]

            split_shapes[i] = new_points

        inscribed = [c, d, b, a]
        bbox = [i, j, h, g]

        return inscribed, bbox, [e,f], [k,l],[m,n], split_shapes, is_invalid, ef_valid, kl_valid, mn_valid

    def update_plot(self):
        theta = self.theta_slider.value() / 100
        w2 = self.w2_slider.value()
        h2 = self.h2_slider.value()
        gap = self.gap_slider.value() / 100
        bearing_width = self.bearing_width_slider.value() / 100
        groove_extra = self.groove_extra_slider.value() / 100
        groove_depth_1 = self.groove_depth_1_slider.value() / 100
        groove_depth_2 = self.groove_depth_2_slider.value() / 100

        inscribed, bbox, ef, kl, mn, split_shapes, is_invalid, ef_valid, kl_valid, mn_valid = self.calc_points(
            theta, w2, h2, gap, bearing_width, groove_extra, groove_depth_1-gap, groove_depth_2-gap
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
        self.plot_widget.plot(bounding_x, bounding_y, pen='b')

        # Update inscribed rectangle (original points for visualization)
        c, d, b, a = inscribed
        inscribed_x = [c[0], d[0], b[0], a[0], c[0]]
        inscribed_y = [c[1], d[1], b[1], a[1], c[1]]
        self.plot_widget.plot(inscribed_x, inscribed_y, pen='purple')

        # Update split shapes
        if split_shapes:
            for e, shape in enumerate(split_shapes):
                if len(shape) >= 3:
                    x_coords = [p[0] for p in shape] + [shape[0][0]]
                    y_coords = [p[1] for p in shape] + [shape[0][1]]
                    self.plot_widget.plot(x_coords, y_coords, pen=f'#f{8*e:x}0')

        # Update points
        e, f = ef
        points_x = [e[0], f[0]]
        points_y = [e[1], f[1]]
        self.plot_widget.plot(points_x, points_y, symbol='o', symbolPen=None, symbolBrush='pink', symbolSize=10)

        k, l = kl
        points_x = [k[0], l[0]]
        points_y = [k[1], l[1]]
        self.plot_widget.plot(points_x, points_y, symbol='o', symbolPen=None, symbolBrush='red', symbolSize=10)

        m, n = mn
        points_x = [m[0], n[0]]
        points_y = [m[1], n[1]]
        self.plot_widget.plot(points_x, points_y, symbol='o', symbolPen=None, symbolBrush='brown', symbolSize=10)

        # Clear previous split plots if any
        #for item in self.plot_widget.listDataItems():
        #    if item.pen() and item.pen().color().name() == '#ff00ff':  # Magenta pen for split shapes
        #        self.plot_widget.removeItem(item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PlotWindow()
    window.show()
    sys.exit(app.exec_())