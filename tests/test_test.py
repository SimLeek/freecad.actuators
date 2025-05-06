def test_points():
    from math import sin, cos, pi, sqrt
    import matplotlib.pyplot as plt

    def calc_points(theta, w2, h2):
        # Calculate initial trigonometric values
        t = theta
        sin_t, cos_t = sin(t), cos(t)
        print(sin_t, cos_t)
        sec_2t = 1 / cos(2 * t)  # Secant of 2theta
        print(sec_2t)

        if abs(theta - pi / 4) < 1e-10:  # Close to 45 degrees
            h1 = w1 = w2 / sqrt(2)
        else:
            # Compute H1 and W1
            h1 = sec_2t * (h2 * cos_t - w2 * sin_t)
            w1 = sec_2t * (w2 * cos_t - h2 * sin_t)
            print(h1, w1)

            h2_2 = w1*sin_t+h1*cos_t
            w2_2 = w1*cos_t+h1*sin_t
            print(w2, w2_2)
            print(h2, h2_2)
            h1 = h1
            w1 = w1

        # bounding rectangle points
        i = (0, 0)
        g = (0, h2)
        h = (w2, h2)
        j = (w2, 0)

        # inscribed rotated rectangle points
        c = (sin_t * h1, 0)
        a = (0, cos_t * h1)
        b = (cos_t * w1, h2)
        d = (w2, sin_t * w1)

        # Adjust inscribed rectangle by finding intersections with bounding box
        def line_intersection(p1, p2, x_min, x_max, y_min, y_max):
            x1, y1 = p1
            x2, y2 = p2
            intersections = []

            # Intersect with x=x_min (left)
            if abs(x2 - x1) > 1e-10:
                t = (x_min - x1) / (x2 - x1)
                if 0 <= t <= 1:
                    y = y1 + t * (y2 - y1)
                    if y_min <= y <= y_max:
                        intersections.append((x_min, y))

            # Intersect with x=x_max (right)
            if abs(x2 - x1) > 1e-10:
                t = (x_max - x1) / (x2 - x1)
                if 0 <= t <= 1:
                    y = y1 + t * (y2 - y1)
                    if y_min <= y <= y_max:
                        intersections.append((x_max, y))

            # Intersect with y=y_min (bottom)
            if abs(y2 - y1) > 1e-10:
                t = (y_min - y1) / (y2 - y1)
                if 0 <= t <= 1:
                    x = x1 + t * (x2 - x1)
                    if x_min <= x <= x_max:
                        intersections.append((x, y_min))

            # Intersect with y=y_max (top)
            if abs(y2 - y1) > 1e-10:
                t = (y_max - y1) / (y2 - y1)
                if 0 <= t <= 1:
                    x = x1 + t * (x2 - x1)
                    if x_min <= x <= x_max:
                        intersections.append((x, y_max))

            return intersections

        # Find intersections of c-d, d-b, b-a, a-c with bounding box
        new_points = []
        sides = [(c, d), (d, b), (b, a), (a, c)]
        for p1, p2 in sides:
            intersects = line_intersection(p1, p2, 0, w2, 0, h2)
            for point in intersects:
                if point not in new_points:
                    new_points.append(point)

        print(new_points)

        # If we have 4 points, form a new parallelogram
        if len(new_points) >= 4:
            # Sort points to form a ccw parallelogram
            new_points.sort(key=lambda p: (p[1], p[0]))  # Bottom to top, left to right
            c, d = new_points[:2]  # Bottom-left, bottom-right
            new_points.sort(key=lambda p: (-p[1], p[0]))  # Top to bottom, left to right
            b, a = new_points[:2]  # Top-right, top-left


        # slice line between upper and lower bearing races (rotated rectangle)
        e = (h1 * sin_t / 2, h1 * cos_t / 2)  # Point E
        f = ((w1 * cos_t + w2) / 2, (w1 * sin_t + h2) / 2)  # Point F

        # Calculate k (x=0) and l (x=w2) using line from e to f
        ex, ey = e
        fx, fy = f
        k_y = ey + (0 - ex) * (fy - ey) / (fx - ex) if fx != ex else ey
        l_y = ey + (w2 - ex) * (fy - ey) / (fx - ex) if fx != ex else ey
        k = (0, k_y)
        l = (w2, l_y)

        # Calculate m (y=0) and n (y=h2) using line from e to f
        m_x = ex + (0 - ey) * (fx - ex) / (fy - ey) if fy != ey else ex
        n_x = ex + (h2 - ey) * (fx - ex) / (fy - ey) if fy != ey else ex
        m = (m_x, 0)
        n = (n_x, h2)

        return i, j, h, g, c, d, b, a, e, f, k, l, m, n

    def determine_valid_slice(points):
        k, l, m, n = points[-4:]
        k_neg = any(x <= 0 for x in k) or any(x <= 0 for x in l)
        return k_neg

    # Example usage
    theta, w2, h2 = pi/4 + pi / 16, 10, 5  # Adjusted theta to 22.5 degrees to avoid div by 0
    points = calc_points(theta, w2, h2)
    k_neg = determine_valid_slice(points)

    # Unpack points for plotting
    i, j, h, g, c, d, b, a, e, f, k, l, m, n = points

    # Plotting
    fig, ax = plt.subplots()
    # Bounding rectangle (ccw: i, j, h, g)
    ax.plot([i[0], j[0], h[0], g[0], i[0]], [i[1], j[1], h[1], g[1], i[1]], 'b-')
    # Inscribed rectangle (ccw: c, d, b, a)
    ax.plot([c[0], d[0], b[0], a[0], c[0]], [c[1], d[1], b[1], a[1], c[1]], 'r-')
    # Slice line and points
    if k_neg:
        ax.plot([k[0], e[0], f[0], l[0]], [k[1], e[1], f[1], l[1]], 'g--')  # Solid for k-l
        ax.plot([m[0], n[0]], [m[1], n[1]], 'g-')  # Dashed for m-n
    else:
        ax.plot([k[0], e[0], f[0], l[0]], [k[1], e[1], f[1], l[1]], 'g-')  # Dashed for k-l
        ax.plot([m[0], n[0]], [m[1], n[1]], 'g--')  # Solid for m-n
    ax.plot(e[0], e[1], 'go', f[0], f[1], 'go', k[0], k[1], 'go', l[0], l[1], 'go', m[0], m[1], 'go', n[0], n[1], 'go')

    ax.set_aspect('equal')
    # plt.savefig('points_plot.png')
    plt.show(block=True)
