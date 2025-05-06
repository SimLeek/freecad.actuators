from math import sin, cos, pi, sqrt
import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider, QLabel
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
        self.ef_label = QLabel("inscribed slice: valid")
        self.ef_label.setStyleSheet("background-color: green; color: white; padding: 5px;")
        layout.addWidget(self.ef_label)

        # slice indicator
        self.slice_label = QLabel("bbox slice: use kl")
        self.slice_label.setStyleSheet("background-color: green; color: white; padding: 5px;")
        layout.addWidget(self.slice_label)

        # Sliders for theta, w2, h2
        self.theta_slider = QSlider(Qt.Horizontal)
        self.theta_slider.setMinimum(0)
        self.theta_slider.setMaximum(314/2)  # 0 to pi in 100ths
        self.theta_slider.setValue(157)  # Start at pi/2
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

        # Connect sliders to update function
        self.theta_slider.valueChanged.connect(self.update_plot)
        self.w2_slider.valueChanged.connect(self.update_plot)
        self.h2_slider.valueChanged.connect(self.update_plot)

        # Initial plot items
        self.bounding_plot = self.plot_widget.plot(pen='b')
        self.inscribed_plot = self.plot_widget.plot(pen='r')
        self.points_plot = self.plot_widget.plot(symbol='o', symbolPen=None, symbolBrush='pink', symbolSize=10)
        self.slice2_plot = self.plot_widget.plot(pen=pg.mkPen('y', style=Qt.DashLine))
        self.slice1_plot = self.plot_widget.plot(pen=pg.mkPen('g', style=Qt.SolidLine))

        # Initial plot
        self.update_plot()

    def calc_points(self, theta, w2, h2):
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

        def line_intersection(p1, p2, x_min, x_max, y_min, y_max):
            x1, y1 = p1
            x2, y2 = p2
            intersections = []
            if abs(x2 - x1) > 1e-10:
                t = (x_min - x1) / (x2 - x1)
                if 0 <= t <= 1:
                    y = y1 + t * (y2 - y1)
                    if y_min <= y <= y_max:
                        intersections.append((x_min, y))
            if abs(x2 - x1) > 1e-10:
                t = (x_max - x1) / (x2 - x1)
                if 0 <= t <= 1:
                    y = y1 + t * (y2 - y1)
                    if y_min <= y <= y_max:
                        intersections.append((x_max, y))
            if abs(y2 - y1) > 1e-10:
                t = (y_min - y1) / (y2 - y1)
                if 0 <= t <= 1:
                    x = x1 + t * (x2 - x1)
                    if x_min <= x <= x_max:
                        intersections.append((x, y_min))
            if abs(y2 - y1) > 1e-10:
                t = (y_max - y1) / (y2 - y1)
                if 0 <= t <= 1:
                    x = x1 + t * (x2 - x1)
                    if x_min <= x <= x_max:
                        intersections.append((x, y_max))
            return intersections

        new_points = [c, d, b, a]
        sides = [(c, d), (d, b), (b, a), (a, c)]
        for p1, p2 in sides:
            intersects = line_intersection(p1, p2, 0, w2, 0, h2)
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
            # Fallback: Use center line with theta
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

        # Return points and validity condition
        is_invalid = points_outside and not len(new_points) >= 4
        ef_valid = not any(p[0] < 0 or p[0] > w2 or p[1] > h2 for p in [e, f])
        kl_valid = not any(p[0] < 0 or p[0] > w2 or p[1] > h2 for p in [k, l])
        mn_valid = not any(p[0] < 0 or p[0] > w2 or p[1] > h2 for p in [m, n])
        return i, j, h, g, c, d, b, a, e, f, k, l, m, n, is_invalid, ef_valid, kl_valid, mn_valid

    def update_plot(self):
        theta = self.theta_slider.value() / 100
        w2 = self.w2_slider.value()
        h2 = self.h2_slider.value()

        points = self.calc_points(theta, w2, h2)
        i, j, h, g, c, d, b, a, e, f, k, l, m, n, is_invalid, ef_valid, kl_valid, mn_valid = points

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

        # Update bounding rectangle
        bounding_x = [i[0], j[0], h[0], g[0], i[0]]
        bounding_y = [i[1], j[1], h[1], g[1], i[1]]
        self.bounding_plot.setData(bounding_x, bounding_y)

        # Update inscribed rectangle
        inscribed_x = [c[0], d[0], b[0], a[0], c[0]]
        inscribed_y = [c[1], d[1], b[1], a[1], c[1]]
        self.inscribed_plot.setData(inscribed_x, inscribed_y)

        # Update slice lines
        if kl_valid:
            self.slice1_plot.setData([k[0], e[0], f[0], l[0]], [k[1], e[1], f[1], l[1]])
            self.slice2_plot.setData([m[0], n[0]], [m[1], n[1]])
        else:
            self.slice1_plot.setData([m[0], n[0]], [m[1], n[1]])
            self.slice2_plot.setData([k[0], e[0], f[0], l[0]], [k[1], e[1], f[1], l[1]])

        # Update points
        points_x = [e[0], f[0], k[0], l[0], m[0], n[0]]
        points_y = [e[1], f[1], k[1], l[1], m[1], n[1]]
        self.points_plot.setData(points_x, points_y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PlotWindow()
    window.show()
    sys.exit(app.exec_())