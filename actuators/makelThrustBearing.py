import FreeCAD, FreeCADGui, Part, math
import os
import sys
from freecad import app as App
from freecad import gui as Gui




# Geometric functions (modified to return shapes)
def CheckForInputErrors(in_d, out_d, height, wall_thick, roller_rounding):
    if out_d <= in_d:
        print("out_d <= in_d")
        return -99
    if wall_thick * 2 >= height:
        print("wall_thick * 2 >= height")
        return -99
    roller_d = CalculateRollerDiameter(height, wall_thick, roller_rounding)
    if roller_d < roller_rounding:
        print("Roller too small")
        return -99
    if in_d + wall_thick + roller_d + roller_d >= out_d:
        print("Can't fit roller ", roller_d, "mm between the races")
        return -99
    return 0


def CalculateRollerDiameter(height, wall_thickness, roller_rounding):
    precise_roller_diameter = height - (2 * wall_thickness)
    rounded_down_roller_diameter = math.floor(precise_roller_diameter / roller_rounding) * roller_rounding
    return rounded_down_roller_diameter


def create_bottom_race(height, int_radius, ext_radius, gap=0.5):
    # Create tube shape
    z_start = (height + gap) / 2.0
    tube = Part.makeCylinder(ext_radius, (height-gap)/2, FreeCAD.Vector(0, -gap/2, 0), FreeCAD.Vector(0, -1, 0))
    inner_hole = Part.makeCylinder(int_radius, (height-gap)/2, FreeCAD.Vector(0, -gap/2, 0), FreeCAD.Vector(0, -1, 0))
    tube = tube.cut(inner_hole)

    # Create groove (cylindrical cut)
    #groove_z = (height - roller_diam) / 2.0
    #mid_rad = (ext_radius + int_radius)/2.0
    #tube2 = Part.makeCylinder(mid_rad + roller_holder_len / 2 + gap, height, FreeCAD.Vector(0, 0, groove_z), FreeCAD.Vector(0, 0, 1))
    #inner_hole2 = Part.makeCylinder(mid_rad - roller_holder_len / 2 - gap, height, FreeCAD.Vector(0, 0, groove_z), FreeCAD.Vector(0, 0, 1))
    #groove = tube2.cut(inner_hole2)

    # Cut groove from tube
    #inner_race = tube.cut(groove)
    return tube


def create_top_race(height, int_radius, ext_radius, gap=0.5):
    # Create tube shape
    z_start = (height + gap) / 2.0
    tube = Part.makeCylinder(ext_radius, (height-gap)/2, FreeCAD.Vector(0, gap/2, 0), FreeCAD.Vector(0, 1, 0))
    inner_hole = Part.makeCylinder(int_radius, (height-gap)/2, FreeCAD.Vector(0, gap/2, 0), FreeCAD.Vector(0, 1, 0))
    tube = tube.cut(inner_hole)

    # Create groove (cylindrical cut)
    #mid_rad = (ext_radius + int_radius)/2.0
    #tube2 = Part.makeCylinder(mid_rad + roller_holder_len / 2 + gap, roller_diam/2-gap/2, FreeCAD.Vector(0, 0, z_start), FreeCAD.Vector(0, 0, 1))
    #inner_hole2 = Part.makeCylinder(mid_rad - roller_holder_len / 2 - gap, roller_diam/2-gap/2, FreeCAD.Vector(0, 0, z_start), FreeCAD.Vector(0, 0, 1))
    #groove = tube2.cut(inner_hole2)

    # Cut groove from tube
    #inner_race = tube.cut(groove)
    return tube


def CreateCage(in_radius, out_radius, roller_diam, roller_length, cage_height, height):
    # Create tube shape
    tube = Part.makeCylinder(out_radius, cage_height,
                             FreeCAD.Vector(0, 0, (height - cage_height) / 2),
                             FreeCAD.Vector(0, 0, 1))
    inner_hole = Part.makeCylinder(in_radius, cage_height,
                                   FreeCAD.Vector(0, 0, (height - cage_height) / 2),
                                   FreeCAD.Vector(0, 0, 1))
    tube = tube.cut(inner_hole)

    roller_placement_radius = (out_radius + in_radius) / 2
    roller_z = (height - cage_height) / 2 + cage_height / 2

    # Create first roller cut
    roller_cut = Part.makeCylinder(roller_diam / 2, roller_length,
                                   FreeCAD.Vector(roller_placement_radius, 0, roller_z),
                                   FreeCAD.Vector(0, 1, 0))
    tube = tube.cut(roller_cut)

    # Calculate number of rollers and their angular positions
    circumference = 2 * math.pi * roller_placement_radius
    num_rollers = math.floor(circumference / (roller_diam * 1.5))  # Space rollers for clearance
    if num_rollers > 0:
        separation_angle = (2 * math.pi) / num_rollers
        for i in range(1, num_rollers):
            angle = i * separation_angle
            roller_cut = Part.makeCylinder(roller_diam / 2, roller_length,
                                           FreeCAD.Vector(roller_placement_radius * math.cos(angle),
                                                          roller_placement_radius * math.sin(angle),
                                                          roller_z),
                                           FreeCAD.Vector(0, 1, 0))
            tube = tube.cut(roller_cut)

    return tube


def CreateNeedleRoller(roller_diam, roller_length, placement_radius):
    # Create a single needle roller
    roller = Part.makeCylinder(roller_diam / 2, roller_length,
                               FreeCAD.Vector(placement_radius, 0, roller_diam / 2),
                               FreeCAD.Vector(0, 1, 0))
    return roller


# View Provider for the Axial Thrust Bearing (unchanged)
class ViewProviderAxialThrustBearing(object):
    def __init__(self, vobj, icon_fn=None):
        vobj.Proxy = self
        dirname = os.path.dirname(__file__)
        # TODO: PROVIDE AN SVG ICON FOR THE AXIAL THRUST BEARING IN THE SPECIFIED PATH
        self.icon_fn = icon_fn or os.path.join(dirname, "icons", "axialthrustbearing.svg")

    def attach(self, vobj):
        self.vobj = vobj

    def getIcon(self):
        return self.icon_fn

    if sys.version_info[0] == 3 and sys.version_info[1] >= 11:
        def dumps(self):
            return {"icon_fn": self.icon_fn}

        def loads(self, state):
            self.icon_fn = state["icon_fn"]
    else:
        def __getstate__(self):
            return {"icon_fn": self.icon_fn}

        def __setstate__(self, state):
            self.icon_fn = state["icon_fn"]


# Axial Thrust Bearing FeaturePython Object
class AxialThrustBearing(object):
    def __init__(self, obj, int_diam, ext_diam, height, wall_thickness, roller_rounding):
        obj.addProperty("App::PropertyString", "version", "version", "freecad.axialthrustbearing-version", 1)
        obj.addProperty("App::PropertyLength", "int_diam", "Bearing", "Internal diameter of the bearing", 0)
        obj.addProperty("App::PropertyLength", "ext_diam", "Bearing", "External diameter of the bearing", 0)
        obj.addProperty("App::PropertyLength", "height", "Bearing", "Height of the bearing", 0)
        obj.addProperty("App::PropertyLength", "wall_thickness", "Bearing", "Minimum wall thickness of races", 0)
        obj.addProperty("App::PropertyLength", "roller_rounding", "Bearing", "Rounding increment for roller diameter",
                        0)

        obj.version = "0.0.1"
        obj.int_diam = int_diam
        obj.ext_diam = ext_diam
        obj.height = height
        obj.wall_thickness = wall_thickness
        obj.roller_rounding = roller_rounding
        obj.Proxy = self

    def generateBearing(self, fp):
        roller_diam = CalculateRollerDiameter(float(fp.height), float(fp.wall_thickness), float(fp.roller_rounding))
        roller_length = roller_diam * 2  # Needle rollers are longer than their diameter
        mid_radius = (float(fp.ext_diam) + float(fp.int_diam)) / 4

        # Create shapes for each component
        inner_race = create_bottom_race(float(fp.height), float(fp.int_diam) / 2, mid_radius, roller_diam)
        '''outer_race = CreateOuterRace(float(fp.height), mid_radius, float(fp.ext_diam) / 2, roller_diam)

        cage_in_radius = mid_radius - roller_diam / 4
        cage_out_radius = mid_radius + roller_diam / 4
        cage_height = roller_diam * 0.75 + float(fp.wall_thickness)
        cage = CreateCage(cage_in_radius, cage_out_radius, roller_diam, roller_length, cage_height, float(fp.height))

        roller = CreateNeedleRoller(roller_diam, roller_length, mid_radius)

        # Combine all shapes into a compound
        parts = [inner_race, outer_race, cage, roller]
        compound = Part.Compound([p for p in parts if p])
        return compound'''
        return inner_race

    def execute(self, fp):
        if CheckForInputErrors(float(fp.int_diam), float(fp.ext_diam), float(fp.height),
                               float(fp.wall_thickness), float(fp.roller_rounding)) != 0:
            fp.Shape = Part.Shape()  # Empty shape on error
            return
        solid = self.generateBearing(fp)
        if solid:
            fp.Shape = solid
        App.ActiveDocument.recompute()


# Task Panel for UI (unchanged)
class BoxTaskPanel:
    def __init__(self, obj):
        self.obj = obj
        dirname = os.path.dirname(__file__)
        # TODO: ENSURE THE form.ui FILE IS IN THE SPECIFIED PATH
        self.form = FreeCADGui.PySideUic.loadUi(os.path.join(dirname, "form.ui"))
        self.form.Int_Diam.setValue(float(obj.int_diam))
        self.form.Ext_Diam.setValue(float(obj.ext_diam))
        self.form.B_Height.setValue(float(obj.height))
        self.form.Min_Wall_Thick.setValue(float(obj.wall_thickness))
        self.form.Ball_Rounding.setValue(float(obj.roller_rounding))

    def accept(self):
        in_d = self.form.Int_Diam.value()
        out_d = self.form.Ext_Diam.value()
        height = self.form.B_Height.value()
        wall_thick = self.form.Min_Wall_Thick.value()
        roller_rounding = self.form.Ball_Rounding.value()

        if CheckForInputErrors(in_d, out_d, height, wall_thick, roller_rounding) != 0:
            FreeCADGui.Control.closeDialog()
            return False

        self.obj.int_diam = in_d
        self.obj.ext_diam = out_d
        self.obj.height = height
        self.obj.wall_thickness = wall_thick
        self.obj.roller_rounding = roller_rounding

        FreeCADGui.Control.closeDialog()
        App.ActiveDocument.recompute()
        Gui.SendMsgToActiveView("ViewFit")
        Gui.activeDocument().activeView().viewIsometric()
        return True

    def reject(self):
        FreeCADGui.Control.closeDialog()
        return False


# Command to create the Axial Thrust Bearing (unchanged)
class CreateAxialThrustBearingCommand:
    def GetResources(self):
        dirname = os.path.dirname(__file__)
        # TODO: PROVIDE AN SVG ICON FOR THE COMMAND IN THE SPECIFIED PATH
        return {
            'MenuText': 'Create Axial Thrust Bearing',
            'ToolTip': 'Create a needle roller axial thrust bearing',
            'Pixmap': os.path.join(dirname, "icons", "axialthrustbearing.svg")
        }

    def Activated(self):
        try:
            selection = Gui.Selection.getSelection()
            obj = App.ActiveDocument.addObject("Part::FeaturePython", "AxialThrustBearing")
            # Default parameters
            int_diam = 8.0
            ext_diam = 22.0
            height = 7.0
            wall_thickness = 1.0
            roller_rounding = 0.5
            if selection:
                obj.Placement = selection[0].Placement
            AxialThrustBearing(obj, int_diam, ext_diam, height, wall_thickness, roller_rounding)
            ViewProviderAxialThrustBearing(obj.ViewObject)
            panel = BoxTaskPanel(obj)
            FreeCADGui.Control.showDialog(panel)
            return obj
        except Exception as e:
            App.Console.PrintError(f"Error: {str(e)}\n")
            return None

    #def IsActive(self):
    #    return App.ActiveDocument is not None


# Register the command
#FreeCADGui.addCommand('CreateAxialThrustBearing', CreateAxialThrustBearingCommand())
def create_tapered_roller_track_cutout(L, R_small, alpha, num_points, translation):
    """
    Create a solid tapered roller with logarithmic crowning in FreeCAD.

    Parameters:
    - L (float): Roller length (mm)
    - delta (float): Crown drop at ends (mm)
    - R_small (float): Radius at small end (mm)
    - alpha (float): Taper angle (degrees)
    - num_points (int): Number of points for B-spline curve

    Returns:
    - FreeCAD object: Solid crowned roller
    """
    # Convert alpha to radians
    alpha_rad = math.radians(alpha)

    # Generate points for logarithmic crown (outer profile)
    crown_points = []
    for i in range(num_points):
        x = (i / (num_points - 1)) * L  # x from 0 to L
        R_base = R_small + x * math.tan(alpha_rad)  # Base radius at x
        crown_points.append(FreeCAD.Vector(x, R_base, 0))

    # Create B-spline for crowned outer surface
    spline = Part.BSplineCurve()
    spline.interpolate(crown_points)

    crown2_points = []
    for i in reversed(range(num_points)):
        x = (i / (num_points - 1)) * L  # x from L to 0
        R_base = -(R_small + x * math.tan(alpha_rad))  # Base radius at x
        crown2_points.append(FreeCAD.Vector(x, R_base, 0))

    # Create B-spline for crowned outer surface
    spline2 = Part.BSplineCurve()
    spline2.interpolate(crown2_points)

    # Create closed sketch for solid revolution
    # Points: crown spline (top), line to axis (right), axis (bottom), line to start (left)
    end_x = L
    end_y = R_small + L * math.tan(alpha_rad)  # Radius at x=L
    start_x = 0
    start_y = R_small  # Radius at x=0

    # Create lines to close the shape
    line1 = Part.LineSegment(FreeCAD.Vector(end_x, end_y, 0), FreeCAD.Vector(end_x, -end_y, 0))  # Right edge
    #line2 = Part.LineSegment(FreeCAD.Vector(end_x, 0, 0), FreeCAD.Vector(start_x, 0, 0))  # Bottom (axis)
    line3 = Part.LineSegment(FreeCAD.Vector(start_x, -start_y, 0), FreeCAD.Vector(start_x, start_y, 0))  # Left edge

    # Combine into a wire
    shape = Part.Wire([spline.toShape(), line1.toShape(), spline2.toShape(), line3.toShape()])

    # Create face and revolve to solid
    face = Part.Face(shape)
    face = face.translate(App.Vector(translation, 0, 0))
    solid = face.revolve(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), 360)

    return solid

def create_crowned_tapered_roller(L, delta, zeta, R_small, alpha, num_points, r_fillet):
    """
    Create a solid tapered roller with logarithmic crowning in FreeCAD.

    Parameters:
    - L (float): Roller length (mm)
    - delta (float): Crown drop at ends (mm)
    - R_small (float): Radius at small end (mm)
    - alpha (float): Taper angle (degrees)
    - num_points (int): Number of points for B-spline curve

    Returns:
    - FreeCAD object: Solid crowned roller
    """
    # Convert alpha to radians
    alpha_rad = math.radians(alpha)

    # Generate points for logarithmic crown (outer profile)
    crown_points = []
    for i in range(num_points):
        x = (i / (num_points - 1)) * L  # x from 0 to L
        x_centered = x - L / 2  # Center x for crowning (-L/2 to L/2)
        h = (delta / 2.0) * math.log(1 + zeta*(2 * x_centered / L) ** 2)  # Crown height
        R_base = R_small + x * math.tan(alpha_rad)  # Base radius at x
        R_crowned = R_base - h  # Adjusted radius
        crown_points.append(FreeCAD.Vector(x, R_crowned, 0))

    # Create B-spline for crowned outer surface
    spline = Part.BSplineCurve()
    spline.interpolate(crown_points)

    # Create closed sketch for solid revolution
    # Points: crown spline (top), line to axis (right), axis (bottom), line to start (left)
    end_x = L
    end_y = R_small + L * math.tan(alpha_rad) - (delta / 2.0) * math.log(1 + zeta)  # Radius at x=L
    start_x = 0
    start_y = R_small - (delta / 2.0) * math.log(1 + zeta)  # Radius at x=0

    # Create lines to close the shape
    line1 = Part.LineSegment(FreeCAD.Vector(end_x, end_y, 0), FreeCAD.Vector(end_x, 0, 0))  # Right edge
    line2 = Part.LineSegment(FreeCAD.Vector(end_x, 0, 0), FreeCAD.Vector(start_x, 0, 0))  # Bottom (axis)
    line3 = Part.LineSegment(FreeCAD.Vector(start_x, 0, 0), FreeCAD.Vector(start_x, start_y, 0))  # Left edge

    # Combine into a wire
    shape = Part.Wire([spline.toShape(), line1.toShape(), line2.toShape(), line3.toShape()])

    # Create face and revolve to solid
    face = Part.Face(shape)
    solid = face.revolve(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(1, 0, 0), 360)
    filleted_solid = solid.makeFillet(r_fillet, solid.Edges)

    return filleted_solid