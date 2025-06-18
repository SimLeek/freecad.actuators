from freecad.actuators.bldc.serialize import BLDCParameters
from freecad.actuators.tests_base import run_in_freecad, show_feature_python_group
from typing import Any

@run_in_freecad
def test_generate_stator():
    from freecad.actuators.bldc.top_view_visualization_drawing import _calculate_slot_points
    from freecad.actuators.bldc.serialize import BLDCParameters, load_from_file
    from freecad.actuators.tests_base import show_feature_python_group
    from typing import Any
    import FreeCAD
    import os
    from freecad.actuators.bldc.arcs import to_freecad_arcs_and_lines, detect_arc_segments
    #import sys
    #sys.path.append("/usr/lib/python3.13")
    dir_path = "/home/simleek/.local/share/FreeCAD/Mod/freecad.actuators/freecad/actuators/bldc"
    params = load_from_file(dir_path + os.sep + '24mm_example.json')

    def generate_bldc_model(params: BLDCParameters) -> Any:
        """Generate a FreeCAD Part::FeaturePython group containing the BLDC stator."""
        # Extract stator parameters
        stator = params.stator
        num_slots = stator.num_slots
        slot_width_half = stator.slot_width_half
        hammerhead_width = stator.hammerhead_width
        hammerhead_length = stator.hammerhead_length
        r_inner = stator.stator_inner_radius
        r_outer = stator.r_outer
        cnc_milling = stator.cnc_milling
        drill_bit_radius = stator.drill_bit_radius
        stator_height = stator.height

        # Calculate stator slot points
        all_x, all_y = [], []
        for slot_idx in range(num_slots):
            # todo: use fillets to create the arc/circle sections. LLMs are not intelligent enough to do this.
            x_slot, y_slot = _calculate_slot_points(
                slot_idx,
                num_slots,
                slot_width_half,
                hammerhead_width,
                hammerhead_length,
                r_inner,
                r_outer,
                cnc_milling,
                drill_bit_radius
            )
            all_x.extend(x_slot)
            all_y.extend(y_slot)

        # Close the profile by connecting to the first point
        all_x.append(all_x[0])
        all_y.append(all_y[0])

        # Create a closed wire and face
        #edges = []
        #for i in range(len(all_points) - 1):
        #    edges.append(Part.LineSegment(all_points[i], all_points[i + 1]).toShape())
        edges = to_freecad_arcs_and_lines(all_x, all_y)
        sort_edges = Part.sortEdges(list(reversed(edges)))[0]
        wire = Part.Wire(sort_edges)
        #if not wire.isClosed():
        #    wire = wire.fix()
        face = Part.Face(wire)

        # Extrude to create 3D stator
        stator_shape = face.extrude(FreeCAD.Vector(0, 0, stator_height))
        #solid_stator = Part.makeSolid(stator_shape)  # Convert to solid to ensure volume

        return stator_shape

    stator_shape = generate_bldc_model(params)
    # Create or activate document
    try:
        doc = FreeCAD.getDocument("BLDCMotor")
    except NameError:
        doc = FreeCAD.newDocument("BLDCMotor")
    FreeCAD.setActiveDocument("BLDCMotor")
    show_feature_python_group(doc, [stator_shape], "stator_shape", "BLDCGroup")


@run_in_freecad
def test_generate_stator():
    from freecad.actuators.bldc.top_view_visualization_drawing import _calculate_slot_points
    from freecad.actuators.bldc.serialize import BLDCParameters, load_from_file
    from freecad.actuators.tests_base import show_feature_python_group
    from typing import Any
    import FreeCAD
    import os
    from freecad.actuators.bldc.arcs import to_freecad_arcs_and_lines, detect_arc_segments
    #import sys
    #sys.path.append("/usr/lib/python3.13")
    dir_path = "/home/simleek/.local/share/FreeCAD/Mod/freecad.actuators/freecad/actuators/bldc"
    params = load_from_file(dir_path + os.sep + '24mm_example.json')

    def generate_bldc_model(params: BLDCParameters) -> Any:
        """Generate a FreeCAD Part::FeaturePython group containing the BLDC stator."""
        # Extract stator parameters
        stator = params.stator
        num_slots = stator.num_slots
        slot_width_half = stator.slot_width_half
        hammerhead_width = stator.hammerhead_width
        hammerhead_length = stator.hammerhead_length
        r_inner = stator.stator_inner_radius
        r_outer = stator.r_outer
        cnc_milling = stator.cnc_milling
        drill_bit_radius = stator.drill_bit_radius
        stator_height = stator.height

        # Calculate stator slot points
        all_x, all_y = [], []
        for slot_idx in range(num_slots):
            # todo: use fillets to create the arc/circle sections. LLMs are not intelligent enough to do this.
            x_slot, y_slot = _calculate_slot_points(
                slot_idx,
                num_slots,
                slot_width_half,
                hammerhead_width,
                hammerhead_length,
                r_inner,
                r_outer,
                cnc_milling,
                drill_bit_radius
            )
            all_x.extend(x_slot)
            all_y.extend(y_slot)

        # Close the profile by connecting to the first point
        all_x.append(all_x[0])
        all_y.append(all_y[0])

        # Create a closed wire and face
        #edges = []
        #for i in range(len(all_points) - 1):
        #    edges.append(Part.LineSegment(all_points[i], all_points[i + 1]).toShape())
        edges = to_freecad_arcs_and_lines(all_x, all_y)
        sort_edges = Part.sortEdges(list(reversed(edges)))[0]
        wire = Part.Wire(sort_edges)
        #if not wire.isClosed():
        #    wire = wire.fix()
        face = Part.Face(wire)

        # Extrude to create 3D stator
        stator_shape = face.extrude(FreeCAD.Vector(0, 0, stator_height))
        #solid_stator = Part.makeSolid(stator_shape)  # Convert to solid to ensure volume

        return stator_shape

    stator_shape = generate_bldc_model(params)
    # Create or activate document
    try:
        doc = FreeCAD.getDocument("BLDCMotor")
    except NameError:
        doc = FreeCAD.newDocument("BLDCMotor")
    FreeCAD.setActiveDocument("BLDCMotor")
    show_feature_python_group(doc, [stator_shape], "magnet_shape", "BLDCGroup")


@run_in_freecad
def test_generate_square_magnets():
    from freecad.actuators.bldc.top_view_visualization_drawing import get_square_magnet_points
    from freecad.actuators.bldc.serialize import BLDCParameters, load_from_file
    from freecad.actuators.tests_base import show_feature_python_group
    from typing import Any
    import FreeCAD
    import os
    from freecad.actuators.bldc.arcs import to_freecad_arcs_and_lines, detect_arc_segments
    #import sys
    #sys.path.append("/usr/lib/python3.13")
    dir_path = "/home/simleek/.local/share/FreeCAD/Mod/freecad.actuators/freecad/actuators/bldc"
    params = load_from_file(dir_path + os.sep + '24mm_example.json')
    #params.magnet.square_magnet_rounded_corners = False
    #params.magnet.square_magnet_rounding_radius = 0

    def generate_bldc_model(params: BLDCParameters) -> Any:
        """Generate a FreeCAD Part::FeaturePython group containing the BLDC stator."""
        # Extract stator parameters
        magnet = params.magnet
        num_magnets = magnet.num_magnets
        magnet_outer_radius = magnet.magnet_outer_radius
        dist_from_wall = magnet.dist_from_wall
        rounding_radius = magnet.square_magnet_rounding_radius if magnet.square_magnet_rounded_corners else 0
        width = magnet.magnet_width
        thickness = magnet.magnet_thickness
        magnet_height = magnet.magnet_height

        # Calculate stator slot points
        xy_groups = get_square_magnet_points(num_magnets, magnet_outer_radius, dist_from_wall, rounding_radius, width, thickness)

        # Close the profile by connecting to the first point

        #all_x.append(all_x[0])
        #all_y.append(all_y[0])



        # Create a closed wire and face
        #edges = []
        #for i in range(len(all_points) - 1):
        #    edges.append(Part.LineSegment(all_points[i], all_points[i + 1]).toShape())
        edges = [to_freecad_arcs_and_lines(xy[0], xy[1]) for xy in xy_groups]
        #sort_edges = [Part.sortEdges(e)[0] for e in edges]
        wires = [Part.Wire(s) for s in edges]
        #if not wire.isClosed():
        #    wire = wire.fix()
        faces = [Part.Face(w) for w in wires]

        # Extrude to create 3D stator
        magnets = [f.extrude(FreeCAD.Vector(0, 0, magnet_height)) for f in faces]
        #solid_stator = Part.makeSolid(stator_shape)  # Convert to solid to ensure volume

        return magnets

    magnets = generate_bldc_model(params)
    # Create or activate document
    try:
        doc = FreeCAD.getDocument("BLDCMotor")
    except NameError:
        doc = FreeCAD.newDocument("BLDCMotor")
    FreeCAD.setActiveDocument("BLDCMotor")
    #
    show_feature_python_group(doc, magnets, [f"magnet {i}" for _, i in enumerate(magnets)], "Magnets")


@run_in_freecad
def test_generate_arc_magnets():
    from freecad.actuators.bldc.top_view_visualization_drawing import get_arc_magnet_points
    from freecad.actuators.bldc.serialize import BLDCParameters, load_from_file
    from freecad.actuators.tests_base import show_feature_python_group
    from typing import Any
    import FreeCAD
    import os
    from freecad.actuators.bldc.arcs import to_freecad_arcs_and_lines, detect_arc_segments
    #import sys
    #sys.path.append("/usr/lib/python3.13")
    dir_path = "/home/simleek/.local/share/FreeCAD/Mod/freecad.actuators/freecad/actuators/bldc"
    params = load_from_file(dir_path + os.sep + '24mm_example.json')
    params.magnet.square_magnet_rounded_corners = False
    #params.magnet.square_magnet_rounding_radius = 0

    def generate_bldc_model(params: BLDCParameters) -> Any:
        """Generate a FreeCAD Part::FeaturePython group containing the BLDC stator."""
        # Extract stator parameters
        magnet = params.magnet
        num_magnets = magnet.num_magnets
        magnet_outer_radius = magnet.magnet_outer_radius
        #arc_width = magnet.magnet_width
        magnet_height = magnet.magnet_height
        magnet_inner_radius = magnet.magnet_inner_radius
        arc_width = 23.7142857143  # degrees
        # Calculate stator slot points
        xy_groups = get_arc_magnet_points(num_magnets, arc_width, magnet_inner_radius, magnet_outer_radius)

        # Close the profile by connecting to the first point

        #all_x.append(all_x[0])
        #all_y.append(all_y[0])



        # Create a closed wire and face
        #edges = []
        #for i in range(len(all_points) - 1):
        #    edges.append(Part.LineSegment(all_points[i], all_points[i + 1]).toShape())
        edges = [to_freecad_arcs_and_lines(xy[0], xy[1]) for xy in xy_groups]
        #sort_edges = [Part.sortEdges(e)[0] for e in edges]
        wires = [Part.Wire(s) for s in edges]
        #if not wire.isClosed():
        #    wire = wire.fix()
        faces = [Part.Face(w) for w in wires]

        # Extrude to create 3D stator
        magnets = [f.extrude(FreeCAD.Vector(0, 0, magnet_height)) for f in faces]
        #solid_stator = Part.makeSolid(stator_shape)  # Convert to solid to ensure volume

        return magnets

    magnets = generate_bldc_model(params)
    # Create or activate document
    try:
        doc = FreeCAD.getDocument("BLDCMotor")
    except NameError:
        doc = FreeCAD.newDocument("BLDCMotor")
    FreeCAD.setActiveDocument("BLDCMotor")
    #
    show_feature_python_group(doc, magnets, [f"magnet {i}" for _, i in enumerate(magnets)], "Magnets")

@run_in_freecad
def test_generate_wire():
    from freecad.actuators.tests_base import show_feature_python_group
    import FreeCAD
    import Part
    import BOPTools.SplitAPI
    import numpy as np
    from FreeCAD import Vector, Rotation

    from freecad import app as App

    doc = FreeCAD.newDocument("TestDoc")
    FreeCAD.setActiveDocument("TestDoc")

    # Parameters
    H = 2.0  # Width of prism
    W = 1.0  # Height of prism
    D = 3.0  # Depth of prism
    c = 0.1  # wire radius
    # p = 0.25  # Pitch (z-advance per turn)
    p = c * 2
    turns = [[0, 12], [11, 1], [2, 10], [9, 3], [4, 8], [7, 5]]
    points_per_turn = 600  # Number of points for smooth curve

    edges = []

    from freecad.actuators.util import traverse_tuple

    def get_xyz_spiral(t_mod, c_l):
        x_coords, y_coords, z_coords = [], [], []
        if 0 <= t_mod < t1:
            # Right side
            x_coords.append(H / 2 + c_l)
            y_coords.append(W / 2 - P * t_mod / (2 * np.pi))
        elif t1 <= t_mod < t2:
            # Bottom-right corner
            theta = -(P * t_mod - 2 * np.pi * W) / (2 * np.pi * c_l)
            x_coords.append(H / 2 + c_l * np.cos(theta))
            y_coords.append(-W / 2 + c_l * np.sin(theta))
        elif t2 <= t_mod < t3:
            # Bottom side
            x_coords.append(H / 2 - (P * t_mod / (2 * np.pi) - (W + np.pi * c_l / 2)))
            y_coords.append(-(W / 2 + c_l))
        elif t3 <= t_mod < t4:
            # Bottom-left corner
            theta = -np.pi / 2 - (P * t_mod - 2 * np.pi * (W + H + np.pi * c_l / 2)) / (2 * np.pi * c_l)
            x_coords.append(-H / 2 + c_l * np.cos(theta))
            y_coords.append(-W / 2 + c_l * np.sin(theta))
        elif t4 <= t_mod < t5:
            # Left side
            x_coords.append(-(H / 2 + c_l))
            y_coords.append(-W / 2 + (P * t_mod / (2 * np.pi) - (W + H + np.pi * c_l)))
        elif t5 <= t_mod < t6:
            # Top-left corner
            theta = -np.pi - (P * t_mod - 2 * np.pi * (2 * W + H + np.pi * c_l)) / (2 * np.pi * c_l)
            x_coords.append(-H / 2 + c_l * np.cos(theta))
            y_coords.append(W / 2 + c_l * np.sin(theta))
        elif t6 <= t_mod < t7:
            # Top side
            x_coords.append(-H / 2 + (P * t_mod / (2 * np.pi) - (2 * W + H + 3 * np.pi * c_l / 2)))
            y_coords.append(W / 2 + c_l)
        else:  # t7 <= t_mod < t8
            # Top-right corner
            theta = -3 * np.pi / 2 - (P * t_mod - 2 * np.pi * (2 * W + 2 * H + 3 * np.pi * c_l / 2)) / (
                    2 * np.pi * c_l)
            x_coords.append(H / 2 + c_l * np.cos(theta))
            y_coords.append(W / 2 + c_l * np.sin(theta))
        if l % 2 == 0:
            z_coords.append(p * t_mod / (2 * np.pi) + t * p)
        else:  # reverse
            z_coords.append(p * (2 * np.pi - t_mod) / (2 * np.pi) + t * p)
        return x_coords[0], y_coords[0], z_coords[0]

    # Parametric equations
    xyz_prev = 0
    start_dir = None
    start_point = None
    for l, layer in enumerate(turns):
        for t in traverse_tuple(layer):
            print(t)
            c_l = c + l * c * 2

            # Perimeter of the coil's path in xy-plane
            P = 2 * H + 2 * W + 2 * np.pi * c_l

            # Transition points in t (for one turn, t in [0, 2pi])
            t1 = 2 * np.pi * W / P
            t2 = 2 * np.pi * (W + np.pi * c_l / 2) / P
            t3 = 2 * np.pi * (W + H + np.pi * c_l / 2) / P
            t4 = 2 * np.pi * (W + H + np.pi * c_l) / P
            t5 = 2 * np.pi * (2 * W + H + np.pi * c_l) / P
            t6 = 2 * np.pi * (2 * W + H + 3 * np.pi * c_l / 2) / P
            t7 = 2 * np.pi * (2 * W + 2 * H + 3 * np.pi * c_l / 2) / P
            t8 = 2 * np.pi

            if l == 0:
                t_lin = [get_xyz_spiral(0, c_l), get_xyz_spiral(t1, c_l)]
                start_point = Vector(*t_lin[0])
                start_dir = Vector(*t_lin[-1]) - start_point
            else:
                t_lin = [xyz_prev, get_xyz_spiral(t1, c_l)]
            edges.append(Part.LineSegment(Vector(*t_lin[0]), Vector(*t_lin[1])).toShape())

            edge = Part.BSplineCurve()
            edge.interpolate([Vector(*get_xyz_spiral(t_l, c_l)) for t_l in np.linspace(t1, t2, 12)])
            edges.append(edge.toShape())

            edges.append(
                Part.LineSegment(Vector(*get_xyz_spiral(t2, c_l)), Vector(*get_xyz_spiral(t3, c_l))).toShape())

            edge = Part.BSplineCurve()
            edge.interpolate([Vector(*get_xyz_spiral(t_l, c_l)) for t_l in np.linspace(t3, t4, 12)])
            edges.append(edge.toShape())

            edges.append(
                Part.LineSegment(Vector(*get_xyz_spiral(t4, c_l)), Vector(*get_xyz_spiral(t5, c_l))).toShape())

            edge = Part.BSplineCurve()
            edge.interpolate([Vector(*get_xyz_spiral(t_l, c_l)) for t_l in np.linspace(t5, t6, 12)])
            edges.append(edge.toShape())

            edges.append(
                Part.LineSegment(Vector(*get_xyz_spiral(t6, c_l)), Vector(*get_xyz_spiral(t7, c_l))).toShape())

            edge = Part.BSplineCurve()
            edge.interpolate([Vector(*get_xyz_spiral(t_l, c_l)) for t_l in np.linspace(t7, t8, 12)])
            edges.append(edge.toShape())

            xyz_prev = get_xyz_spiral(t8, c_l)

    wire = Part.Wire(edges)

    if start_dir is not None:
        normal = start_dir.normalize()
    else:
        raise ValueError('no lines made')

    circle = Part.makeCircle(c, start_point, normal)
    section = Part.Wire([circle])
    # face = Part.Face(Part.Wire(circle))

    makeSolid = True
    isFrenet = False  # True here doesn't work either!
    sweep = wire.makePipeShell([section], makeSolid, isFrenet)

    # Define colors (RGB tuples normalized to 0-1)
    bread_color = (210 / 255, 180 / 255, 140 / 255)  # Light beige/tan for races
    green_color = (0 / 255, 128 / 255, 0 / 255)  # Green for top cage
    red_color = (255 / 255, 0 / 255, 0 / 255)  # Red for bottom cage
    dark_red_brown = (139 / 255, 0 / 255, 0 / 255)  # Dark red/brown for rollers

    # cage_half2 = cage2.cut(plane.extrude(FreeCAD.Vector(0, 10, 0)))  # Extrude to cut the other half

    show_feature_python_group(doc, [sweep], ["wire"], "wires", colors=[bread_color])