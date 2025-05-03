from freecad.actuators.tests_base import run_in_freecad
import pytest

@run_in_freecad
def test_create_cube():
    import FreeCAD
    import FreeCADGui
    import Part
    doc = FreeCAD.newDocument("TestDoc")
    FreeCAD.setActiveDocument("TestDoc")  # Activate the document
    box = doc.addObject("Part::Box", "MyBox")
    box.Length = 10
    box.Width = 10
    box.Height = 10
    doc.recompute()
    FreeCADGui.ActiveDocument.ActiveView.fitAll()  # Zoom to show the cube
    assert pytest.approx(box.Shape.Volume, 0.0000001) == 1000  # Check cube volume
    # GUI will show the cube


@run_in_freecad
def test_create_bottom_race():
    from freecad.actuators.makelThrustBearing import create_bottom_race
    from freecad.actuators.tests_base import show_feature_python
    import FreeCAD
    import FreeCADGui
    from freecad import app as App
    import Part
    doc = FreeCAD.newDocument("TestDoc")
    FreeCAD.setActiveDocument("TestDoc")

    obj = App.ActiveDocument.addObject("Part::FeaturePython", "AxialThrustBearing")
    solid = create_bottom_race(10, 5, 15, 6, 7)

    show_feature_python(obj, doc, solid)


@run_in_freecad
def test_create_top_race():
    from freecad.actuators.makelThrustBearing import create_top_race, create_bottom_race
    from freecad.actuators.tests_base import show_feature_python
    import FreeCAD
    import FreeCADGui
    from freecad import app as App
    import Part
    doc = FreeCAD.newDocument("TestDoc")
    FreeCAD.setActiveDocument("TestDoc")

    obj = App.ActiveDocument.addObject("Part::FeaturePython", "AxialThrustBearing")
    solid = create_top_race(10, 5, 15, 6, 7)
    solid2 = create_bottom_race(10, 5, 15, 6, 7)
    solid3 = Part.Compound([solid, solid2])
    show_feature_python(obj, doc, solid3)

@run_in_freecad
def test_create_crowned_tapered_roller():
    from freecad.actuators.tests_base import show_feature_python
    import FreeCAD
    import Part
    from freecad import app as App
    from freecad.actuators.makelThrustBearing import create_tapered_roller_track_cutout

    doc = FreeCAD.newDocument("TestDoc")
    FreeCAD.setActiveDocument("TestDoc")

    obj = App.ActiveDocument.addObject("Part::FeaturePython", "AxialThrustBearing")
    solid = create_tapered_roller_track_cutout(20, 7.5, 15.0, 21, 10)
    #solid3 = Part.Compound([solid, solid2])
    show_feature_python(obj, doc, solid)

@run_in_freecad
def test_create_crowned_tapered_roller_good():
    from freecad.actuators.tests_base import show_feature_python
    import FreeCAD
    import Part
    from freecad import app as App
    from freecad.actuators.makelThrustBearing import create_crowned_tapered_roller

    doc = FreeCAD.newDocument("TestDoc")
    FreeCAD.setActiveDocument("TestDoc")

    obj = App.ActiveDocument.addObject("Part::FeaturePython", "AxialThrustBearing")
    solid = create_crowned_tapered_roller(20, 1, .5, 7.5, 3.0, 21, 2)
    # solid3 = Part.Compound([solid, solid2])
    show_feature_python(obj, doc, solid)

@run_in_freecad
def test_create_tapered_roller_bearing():
    from freecad.actuators.tests_base import show_feature_python
    import FreeCAD
    import Part
    from freecad import app as App
    from freecad.actuators.makelThrustBearing import create_tapered_roller_track_cutout
    from freecad.actuators.makelThrustBearing import create_crowned_tapered_roller
    from freecad.actuators.makelThrustBearing import create_top_race, create_bottom_race

    doc = FreeCAD.newDocument("TestDoc")
    FreeCAD.setActiveDocument("TestDoc")

    top_race = create_top_race(30, 15, 45, gap=5)
    bottom_race = create_bottom_race(30, 15, 45, gap=5)

    length = 20
    extra = .5
    track_cutout = create_tapered_roller_track_cutout(length+2*extra, 7.5, 3.0, 21, 20-extra)

    races = Part.Compound([top_race, bottom_race])
    races = races.cut(track_cutout)

    obj = App.ActiveDocument.addObject("Part::FeaturePython", "AxialThrustBearing")
    solid = create_crowned_tapered_roller(length, 1, .5, 7.5, 3.0, 21, 2)

    solid = solid.translate(App.Vector(length, 0, 0))

    revolved_shapes = []
    num_repetitions = 6
    angle_increment_degrees = 360 / num_repetitions
    for i in range(num_repetitions):
        # Calculate the rotation angle
        rotated_roller = solid.copy()  # Create a copy of the original roller
        rotation_angle = i * angle_increment_degrees
        rotated_roller.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), rotation_angle)
        revolved_shapes.append(rotated_roller)

    solid = Part.Compound([races]+revolved_shapes)
    show_feature_python(obj, doc, solid)