import math


def head_from_D2(D2, N, g=9.81):
    """
    Compute the ideal head H (in meters) given outer diameter D2 (in m)
    and rotational speed N (in RPM). Using:
       H = (π * D2 * (N/60))^2 / (2*g)
    """
    u = math.pi * D2 * (N / 60.0)
    H = (u ** 2) / (2 * g)
    return H


def flow_from_geometry(D1, D2, b, v):
    """
    Compute the flow rate Q (in m^3/s) from the annular passage.

    D1: inner (hub) diameter in m
    D2: outer diameter in m
    b : blade height (channel width) in m
    v : average velocity in m/s
    Using:
       Q = π * (D2 - D1) * b * v
    """
    A = math.pi * (D2 - D1) * b  # cross-sectional area of annulus (rectangular approximation)
    Q = A * v
    return Q


def target_QH(P_h, rho=1000, g=9.81):
    """
    Given hydraulic power P_h (W), compute the required product Q*H.

    Q*H = P_h / (rho*g)
    """
    return P_h / (rho * g)


def f_D2(D2, D1, b, v, N, target_QH_value, g=9.81):
    """
    Function whose zero we seek:

      f(D2) = [flow_from_geometry(D1, D2, b, v) * head_from_D2(D2, N, g)] - target_QH_value

    D1, D2, b in meters, v in m/s, N in RPM.
    """
    Q = flow_from_geometry(D1, D2, b, v)
    H = head_from_D2(D2, N, g)
    return Q * H - target_QH_value


def solve_for_D2(D1, b, v, N, target_QH_value, tol=1e-9, max_iter=100):
    """
    Solve for outer diameter D2 (in m) using bisection.
    We need an interval [low, high] such that f(D2) changes sign.
    We'll choose low = D1 + a small gap, and high = D1 + some reasonable maximum gap.
    """
    low = D1 + 1e-6  # just above D1
    high = D1 + 0.1  # allow up to 100 mm gap as an initial guess

    f_low = f_D2(low, D1, b, v, N, target_QH_value)
    f_high = f_D2(high, D1, b, v, N, target_QH_value)

    # Expand interval if necessary
    iter_expand = 0
    while f_low * f_high > 0 and iter_expand < 20:
        high += 0.05  # increase high by 50 mm
        f_high = f_D2(high, D1, b, v, N, target_QH_value)
        iter_expand += 1
    if f_low * f_high > 0:
        raise ValueError("Could not bracket the root for D2.")

    # Bisection method:
    iter_count = 0
    while iter_count < max_iter:
        mid = (low + high) / 2.0
        f_mid = f_D2(mid, D1, b, v, N, target_QH_value)
        if abs(f_mid) < tol:
            return mid
        if f_low * f_mid < 0:
            high = mid
            f_high = f_mid
        else:
            low = mid
            f_low = f_mid
        iter_count += 1
    return (low + high) / 2.0


def design_impeller(D1_mm, P_h, v, N, b_mm=None, g=9.81, rho=1000):
    """
    Main design function.

    Parameters:
      D1_mm : inner (hub) diameter in millimeters.
      P_h   : desired hydraulic power in Watts (after efficiencies).
              (For example, if motor electrical power is 160 W and pump efficiency is 70%,
              then P_h = 0.7*160 = 112 W.)
      v     : target average velocity in the impeller passage (m/s)
      N     : motor speed in RPM (e.g. 15,540 RPM)
      b_mm  : desired blade height in mm. If None, a default of 10 mm is used.

    The design target is to achieve:

       Q * H = P_h / (rho*g)

    where Q = π (D2 - D1)*b*v  and  H = (π*D2*(N/60))^2/(2*g).

    Returns a dictionary with:
       'D_inner' (mm), 'D_outer' (mm), 'blade_height' (mm), 'Q' (m^3/s), 'H' (m)
    """
    # Convert dimensions to meters
    D1 = D1_mm / 1000.0
    if b_mm is None:
        b = 0.01  # default 10 mm
    else:
        b = b_mm / 1000.0

    # Compute target product Q*H from hydraulic power:
    target_val = target_QH(P_h, rho, g)

    # Solve for outer diameter D2 (in meters) using our function:
    D2 = solve_for_D2(D1, b, v, N, target_val)

    # Compute resulting Q and H
    Q = flow_from_geometry(D1, D2, b, v)
    H = head_from_D2(D2, N, g)

    return {
        'D_inner_mm': D1 * 1000,
        'D_outer_mm': D2 * 1000,
        'blade_height_mm': b * 1000,
        'Q_m3s': Q,
        'H_m': H,
        'Q_times_H': Q * H
    }


# --- Example Usage ---
if __name__ == '__main__':
    # Given parameters:
    # Inner (hub) diameter = 31 mm
    # Motor speed = 15,540 RPM
    # Target average fluid velocity in channel, v = 2 m/s
    # Desired hydraulic power P_h = 112 W  (e.g. 70% of 160W)
    # Design choice: blade height b = 10 mm
    D1_mm = 31
    N = 15540
    v = 2.0  # m/s
    P_h = 112  # W
    b_mm = 10  # mm

    design = design_impeller(D1_mm, P_h, v, N, b_mm)
    print("Impeller Design Dimensions:")
    print(f"Inner Diameter (D1): {design['D_inner_mm']:.2f} mm")
    print(f"Outer Diameter (D2): {design['D_outer_mm']:.2f} mm")
    print(f"Blade Height (b):    {design['blade_height_mm']:.2f} mm")
    print(f"Flow Rate (Q):       {design['Q_m3s']:.6f} m^3/s")
    print(f"Head (H):            {design['H_m']:.2f} m")
    print(f"Q * H:               {design['Q_times_H']:.6f} m^3/s·m (target ≈ 0.0114)")
