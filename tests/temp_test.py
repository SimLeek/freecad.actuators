import FreeCAD
import FreeCADGui
import pytest
def test_create_tapered_roller_bearing():
    from freecad.actuators.tests_base import show_feature_python_group
    import FreeCAD
    import Part
    import BOPTools.SplitAPI

    from freecad import app as App
    from freecad.actuators.bearing.makelThrustBearing import create_tapered_roller_track_cutout
    from freecad.actuators.bearing.makelThrustBearing import create_crowned_tapered_roller
    from freecad.actuators.bearing.makelThrustBearing import create_top_race, create_bottom_race

    doc = FreeCAD.newDocument("TestDoc")
    FreeCAD.setActiveDocument("TestDoc")

    top_race = create_top_race(30, 15, 45, gap=15)
    bottom_race = create_bottom_race(30, 15, 45, gap=15)

    length = 20
    extra = .5
    track_cutout = create_tapered_roller_track_cutout(length+2*extra, 7.5, 3.0, 21, 20-extra)

    races = Part.Compound([top_race, bottom_race])
    races = races.cut(track_cutout)

    # Create a simple cylindrical cage (replace with your actual cage geometry)
    cage = Part.makeCylinder(45, 10, FreeCAD.Vector(0, -5, 0),
                             FreeCAD.Vector(0, 1, 0))  # Outer radius 40, holding rollers in, height 10
    inner_cage = Part.makeCylinder(25, 10, FreeCAD.Vector(0, -5, 0), FreeCAD.Vector(0, 1, 0))  # Inner radius 15
    cage = cage.cut(inner_cage)  # Hollow cylinder
    cage_thickness = 2  # mm

    #obj = App.ActiveDocument.addObject("Part::FeaturePython", "AxialThrustBearing")
    solid = create_crowned_tapered_roller(length, 1, .5, 7.5, 3.0, 21, 2)

    solid = solid.translate(App.Vector(length, 0, 0))

    revolved_shapes = []
    offset_shapes = []
    cage_keep_offset_shapes = []
    hole_radius = 2  # Small enough to fit within cage thickness
    hole_shapes = []
    insert_shapes = []
    num_repetitions = 6
    clearance = 0.5
    angle_increment_degrees = 360 / num_repetitions
    for i in range(num_repetitions):
        # Calculate the rotation angle
        rotated_roller = solid.copy()  # Create a copy of the original roller
        rotation_angle = i * angle_increment_degrees
        rotated_roller.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), rotation_angle)
        revolved_shapes.append(rotated_roller)
        offset_shapes.append(rotated_roller.makeOffsetShape(clearance, tolerance=0.01))
        cage_keep_offset_shapes.append(rotated_roller.makeOffsetShape(clearance+cage_thickness, tolerance=0.01))


    rollers = Part.Compound(revolved_shapes)
    offset_rollers = Part.Compound(offset_shapes)

    # Perform boolean cut on cage with offset rollers
    cage2 = cage.cut(offset_rollers)

    # Create a thin cylinder to hold everything together
    thin_cylinder = Part.makeCylinder(45, 4, FreeCAD.Vector(0, -2, 0), FreeCAD.Vector(0, 1, 0))
    inner_cylinder = Part.makeCylinder(25, 4, FreeCAD.Vector(0, -2, 0), FreeCAD.Vector(0, 1, 0))
    thin_cylinder = thin_cylinder.cut(inner_cylinder)  # Hollow thin cylinder
    cage_intersection_part_1 = Part.Compound([thin_cylinder]+cage_keep_offset_shapes)
    cage_cutter = cage.cut(cage_intersection_part_1)

    cage2 = cage2.cut(cage_cutter)

    # Split the refined cage into two halves
    plane = Part.makePlane(100, 100, FreeCAD.Vector(-50, 0, -50), FreeCAD.Vector(0, 1, 0))  # Plane at z = -5
    #plane_tool = Part.Compound([plane])
    #sliced_parts = cage2.slices(FreeCAD.Vector(0, 1, 0), [1, -1])
    sliced_parts = BOPTools.SplitAPI.slice(cage2, [plane], "Standard")
    cage_half1 = sliced_parts.SubShapes[0]  # First half
    cage_half2 = sliced_parts.SubShapes[1]  # Second half

    # Define colors (RGB tuples normalized to 0-1)
    bread_color = (210/255, 180/255, 140/255)  # Light beige/tan for races
    green_color = (0/255, 128/255, 0/255)      # Green for top cage
    red_color = (255/255, 0/255, 0/255)        # Red for bottom cage
    dark_red_brown = (139/255, 0/255, 0/255)   # Dark red/brown for rollers

    #cage_half2 = cage2.cut(plane.extrude(FreeCAD.Vector(0, 10, 0)))  # Extrude to cut the other half

    show_feature_python_group(doc,[races, cage_half1, cage_half2, rollers], ["races", "cage_half1", "cage_half2", "rollers"], "pressure bearing", colors = [bread_color, green_color, red_color, dark_red_brown])
FreeCADGui.showMainWindow()


test_create_tapered_roller_bearing()
print('Test complete. Press Ctrl+C to close FreeCAD.')
FreeCADGui.exec_loop()
