import FreeCAD, Part, os
import numpy as np

# Import OCC classes to build the BSpline scaling law.
try:
    from OCC.Core.GeomAPI import GeomAPI_PointsToBSpline
    from OCC.Core.gp import gp_Pnt2d, gp_Pnt, gp_Circ, gp_Ax2, gp_Dir
    from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
    from OCC.Core.BRepOffsetAPI import MakePipeShell
except ImportError:
    FreeCAD.Console.PrintError("OCC modules not found. Scaling pipe shell method not available\n")
    #raise


# --------------------------------------------------------------------
def create_scaling_law(sample_function, increment, t_min, t_max):
    """
    Samples the given sample_function from t_min to t_max at the given increment,
    then builds a 2D BSpline curve through points (t, f(t)). This BSpline is used as the scaling law.

    sample_function: a function that takes a t (mm) and returns a diameter (mm).
    """
    ts = np.arange(t_min, t_max + increment, increment)
    values = [sample_function(t) for t in ts]
    pts = [gp_Pnt2d(t, v) for t, v in zip(ts, values)]
    law_bspline = GeomAPI_PointsToBSpline(pts)
    return law_bspline.Curve()


# --------------------------------------------------------------------
def create_spine(points):
    """
    Creates a spine (wire) by interpolating a BSpline curve through the given list of FreeCAD.Vector points.
    """
    spine_curve = Part.BSplineCurve()
    spine_curve.interpolate(points)
    spine_edge = Part.Edge(spine_curve)
    spine_wire = Part.Wire([spine_edge])
    return spine_wire


# --------------------------------------------------------------------
def create_pipe_shell(spine, profile, sample_function, increment, t_min, t_max):
    """
    Creates a pipe shell using the given spine (wire) and profile (wire) with a variable scaling law.

    sample_function: callback function returning diameter at a given t.
    increment: sampling interval (mm)
    t_min, t_max: axial range (mm) along the spine where the law is defined.

    Returns the resulting shape.
    """
    law = create_scaling_law(sample_function, increment, t_min, t_max)
    pipeShell = MakePipeShell(spine)
    # The SetLaw method applies the scaling law to the profile.
    # Parameters: profile, law, align (False), and continuous law (True).
    pipeShell.SetLaw(profile, law, False, True)
    pipeShell.Build()
    return pipeShell.Shape()


# --------------------------------------------------------------------
if __name__ == '__main__':
    # Example usage:

    # 1. Define a sample scaling function (callback) that returns a diameter in mm.
    def my_scaling_function(t):
        # For example, base diameter 10 mm modulated by a sine function.
        return 10 + 1.5 * np.sin(t * 2 * np.pi / 50)


    # 2. Define the spine as a list of FreeCAD.Vector points.
    spine_points = [FreeCAD.Vector(1, 4, 0),
                    FreeCAD.Vector(2, 2, 0),
                    FreeCAD.Vector(3, 3, 0),
                    FreeCAD.Vector(4, 3, 0),
                    FreeCAD.Vector(5, 5, 0)]
    spine = create_spine(spine_points)

    # 3. Create a profile (wire) to be swept along the spine.
    #    In this example, we create a circle with radius 1 mm.
    center = spine_points[0]  # use the first spine point as the profile's center.
    from OCC.Core.gp import gp_Ax2

    ax2 = gp_Ax2(gp_Pnt(center.x, center.y, center.z), gp_Dir(0, 0, 1))
    circle = gp_Circ(ax2, 1)
    profile_edge = BRepBuilderAPI_MakeEdge(circle).Edge()
    profile_wire = BRepBuilderAPI_MakeWire(profile_edge).Wire()

    # 4. Set the axial sampling parameters.
    t_min = 0
    t_max = spine.Length  # use the spine length as the range

    # 5. Create the pipe shell using the parameters.
    result_shape = create_pipe_shell(spine, profile_wire, my_scaling_function, 0.5, t_min, t_max)

    # 6. Display the resulting shape in the active document.
    Part.show(result_shape)
