import numpy as np


def fit_circle(x_points, y_points):
    """
    Fit a circle to points using linear least squares.
    Returns center (h, k), radius r, errors, and angles.
    """
    n = len(x_points)
    if n != len(y_points) or n < 3:
        raise ValueError("At least 3 points required with matching x and y coordinates.")

    # Formulate: x^2 + y^2 + Dx + Ey + F = 0
    A = np.zeros((n, 3))
    b = np.zeros(n)
    for i in range(n):
        A[i] = [x_points[i], y_points[i], 1]
        b[i] = -(x_points[i] ** 2 + y_points[i] ** 2)

    # Solve least squares
    try:
        v = np.linalg.lstsq(A, b, rcond=None)[0]
    except np.linalg.LinAlgError:
        raise ValueError("Singular matrix: points may be collinear.")

    D, E, F = v
    h = -D / 2
    k = -E / 2
    r = np.sqrt(h ** 2 + k ** 2 - F)

    # Compute errors
    algebraic_error = 0
    geometric_errors = []
    for i in range(n):
        alg_dist = x_points[i] ** 2 + y_points[i] ** 2 + D * x_points[i] + E * y_points[i] + F
        algebraic_error += alg_dist ** 2
        geom_dist = abs(np.sqrt((x_points[i] - h) ** 2 + (y_points[i] - k) ** 2) - r)
        geometric_errors.append(geom_dist)

    mean_geometric_error = np.mean(geometric_errors)
    max_geometric_error = np.max(geometric_errors)

    # Compute angles
    angles = [np.arctan2(y_points[i] - k, x_points[i] - h) for i in range(n)]
    angle_rules = np.asarray(angles[1:]) - np.array(angles[:-1])
    invalid_rules = np.where(abs(angle_rules)>np.pi)[0]
    # fix non-linear
    if invalid_rules.size>0:
        for invalid_rule in invalid_rules:
            for i in range(invalid_rule+1, len(angles)):
                if angle_rules[invalid_rule]>np.pi:
                    angles[i] -= np.pi*2
                elif angle_rules[invalid_rule]<-np.pi:
                    angles[i] += np.pi*2


    print(angle_rules)
    start_angle = angles[0]
    start_p1_angle = angles[1]

    end_angle = angles[-1]

    return {
        'center': (h, k),
        'radius': r,
        'algebraic_error': algebraic_error,
        'mean_geometric_error': mean_geometric_error,
        'max_geometric_error': max_geometric_error,
        'start_angle': start_angle,
        'start_p1_angle': start_p1_angle,
        'end_angle': end_angle,
        'points_used': n
    }


def generate_rounded_square(side_length=2, corner_radius=0.5, points_per_corner=10):
    """
    Generate points for a square with rounded corners, with increasing points per corner.
    """
    x_points, y_points = [], []

    # Corner centers
    centers = [
        (side_length / 2 - corner_radius, side_length / 2 - corner_radius),  # Top-right
        (-side_length / 2 + corner_radius, side_length / 2 - corner_radius),  # top left
        (-side_length / 2 + corner_radius, -side_length / 2 + corner_radius),  # Bottom-left
        (side_length / 2 - corner_radius, -side_length / 2 + corner_radius)  # Top-left
    ]

    # Generate arcs with increasing points: 10, 12, 14, 16
    for i, (cx, cy) in enumerate(centers):
        theta_start = i * np.pi / 2
        theta_end = (i + 1) * np.pi / 2
        theta = np.linspace(theta_start, theta_end, points_per_corner + i * 2)
        x_points.extend(cx + corner_radius * np.cos(theta))
        y_points.extend(cy + corner_radius * np.sin(theta))

        # Add straight segment
        if i < 3:
            next_center = centers[i + 1]
        else:
            next_center = centers[0]
        x_start = cx + corner_radius * np.cos(theta_end)
        y_start = cy + corner_radius * np.sin(theta_end)
        x_end = next_center[0] + corner_radius * np.cos(theta_end)
        y_end = next_center[1] + corner_radius * np.sin(theta_end)
        t = np.linspace(0, 1, points_per_corner)
        x_points.extend((1 - t) * x_start + t * x_end)
        y_points.extend((1 - t) * y_start + t * y_end)

    return np.array(x_points), np.array(y_points)


def detect_arc_segments(x_points, y_points, min_points=8, error_threshold=1e-6):
    """
    Dynamically detect circular arc segments in ordered points.
    """
    results = []
    i = 0
    n = len(x_points)

    while i < n:
        # Start with min_points and expand until error increases
        j = i + min_points
        current_x = x_points[i:j]
        current_y = y_points[i:j]

        try:
            fit = fit_circle(current_x, current_y)
            current_error = fit['mean_geometric_error']
            radius = fit['radius']

            if (
                    current_error < error_threshold and
                    np.isfinite(radius) and
                    0 < radius < 1e6
            ):
                best_fit = fit
                best_j = j
            else:
                # If initial fit is bad, skip to next segment
                i += 1
                continue
        except ValueError:
            i += 1
            continue

        # Try to expand the arc
        while j < n:
            current_x = x_points[i:j + 1]
            current_y = y_points[i:j + 1]
            try:
                fit = fit_circle(current_x, current_y)
                current_error = fit['mean_geometric_error']
                radius = fit['radius']

                if (
                        current_error < error_threshold and
                        np.isfinite(radius) and
                        0 < radius < 1e6
                ):
                    best_fit = fit
                    best_j = j + 1
                else:
                    break
            except ValueError:
                break
            j += 1

        if best_fit:
            results.append({
                'corner': len(results) + 1,
                'start_index': i,
                'end_index': best_j - 1,
                'fit': best_fit
            })
            i = best_j  # Move to end of detected arc
        else:
            i += 1

    return results

def to_freecad_arcs_and_lines(x_points, y_points, results=None):
    """
    Create a FreeCAD wire from points and detected arc segments within FreeCAD.
    """
    import FreeCAD, Part
    if results is None:
        results = detect_arc_segments(x_points, y_points, min_points=8, error_threshold=1e-6)
    edges = []
    p = 0
    r = 0
    last_circ = p
    while p < len(x_points):
        if r < len(results) and p == results[r]['start_index']:
            if (r == 0 and p > 0) or (last_circ != results[r-1]['start_index'] if r > 0 else False):
                # Add line segment from p-1 to p
                v1 = FreeCAD.Vector(x_points[p-1], y_points[p-1], 0)
                v2 = FreeCAD.Vector(x_points[p], y_points[p], 0)
                line = Part.LineSegment(v1, v2)
                edges.append(line.toShape())
            result = results[r]
            fit = result['fit']
            # Add arc segment
            center = FreeCAD.Vector(fit['center'][0], fit['center'][1], 0)
            radius = fit['radius']
            start_angle = fit['start_angle'] # Convert to degrees
            end_angle = fit['end_angle']
            if start_angle>end_angle:
                temp_angle = start_angle
                start_angle = end_angle
                end_angle = temp_angle
            arc = Part.ArcOfCircle(Part.Circle(center, FreeCAD.Vector(0,0,1), radius), start_angle, end_angle)
            edges.append(arc.toShape())
            p = result['end_index']
            last_circ = p
            r += 1
        else:
            if p > 0:
                # Add line segment from p-1 to p
                v1 = FreeCAD.Vector(x_points[p-1], y_points[p-1], 0)
                v2 = FreeCAD.Vector(x_points[p], y_points[p], 0)
                line = Part.LineSegment(v1, v2)
                edges.append(line.toShape())
            p += 1
    return edges

if __name__ == "__main__":
    # Generate points
    x_points, y_points = generate_rounded_square(side_length=2, corner_radius=0.5, points_per_corner=10)

    # correctly detects no circles
    #x_points, y_points = [1,2,3,4,5,6,7,8], [1,2,3,4,5,6,7,8]

    # Detect arcs
    results = detect_arc_segments(x_points, y_points, min_points=8, error_threshold=1e-6)

    # Print results
    for result in results:
        fit = result['fit']
        print(f"Corner {result['corner']} (Points {result['start_index']} to {result['end_index']}):")
        print(f"  Center: ({fit['center'][0]:.4f}, {fit['center'][1]:.4f})")
        print(f"  Radius: {fit['radius']:.4f}")
        print(f"  Start Angle: {fit['start_angle']:.4f} radians")
        print(f"  End Angle: {fit['end_angle']:.4f} radians")
        print(f"  Points Used: {fit['points_used']}")
        print(f"  Mean Geometric Error: {fit['mean_geometric_error']:.6f}")
        print(f"  Max Geometric Error: {fit['max_geometric_error']:.6f}")
        print()

    # Visualize
    import matplotlib.pyplot as plt

    p=0
    r = 0
    last_circ = p
    while p<len(x_points):
        if r<len(results) and p==results[r]['start_index']:
            if (r==0 and p>0) or last_circ!=results[r-1]['start_index']:
                plt.plot([x_points[p-1], x_points[p]], [y_points[p-1], y_points[p]], label=f'Line {p}')
            result = results[r]
            fit = result['fit']
            dir = fit['start_p1_angle'] - fit['start_angle']
            theta = np.linspace(fit['start_angle'], fit['end_angle'], 100)
            x_circle = fit['center'][0] + fit['radius'] * np.cos(theta)
            y_circle = fit['center'][1] + fit['radius'] * np.sin(theta)
            plt.plot(x_circle, y_circle, label=f'Arc {result["corner"]}')
            p=result['end_index']
            last_circ = p
            r+=1
        else:
            if p>0:
                plt.plot([x_points[p-1], x_points[p]], [y_points[p-1], y_points[p]], label=f'Line {p}')
        p += 1
    plt.axis('equal')
    plt.legend()
    plt.show()