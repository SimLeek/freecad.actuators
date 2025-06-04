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
    from freecad.actuators.bearing.makelThrustBearing import create_bottom_race
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
    from freecad.actuators.bearing.makelThrustBearing import create_top_race, create_bottom_race
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
    from freecad.actuators.bearing.makelThrustBearing import create_tapered_roller_track_cutout

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
    from freecad.actuators.bearing.makelThrustBearing import create_crowned_tapered_roller

    doc = FreeCAD.newDocument("TestDoc")
    FreeCAD.setActiveDocument("TestDoc")

    obj = App.ActiveDocument.addObject("Part::FeaturePython", "AxialThrustBearing")
    solid = create_crowned_tapered_roller(20, 1, .5, 7.5, 3.0, 21, 2)
    # solid3 = Part.Compound([solid, solid2])
    show_feature_python(obj, doc, solid)

@run_in_freecad
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

@run_in_freecad
def test_create_tapered_roller_bearing_2():
    import FreeCAD
    import Part
    import BOPTools.SplitAPI
    import math
    from freecad import app as App
    from freecad.actuators.bearing.makelThrustBearing import (
        create_tapered_roller_track_cutout,
        create_crowned_tapered_roller,
        create_top_race,
        create_bottom_race,
    )

    from freecad.actuators.tests_base import show_feature_python_group

    class OffsetConfig:
        def __init__(self, loose_clearance, tight_fit_clearance, offset_tolerance):
            assert loose_clearance > 0, "Loose clearance must be positive"
            assert tight_fit_clearance > 0, "Tight fit clearance must be positive"
            assert offset_tolerance > 0, "Offset tolerance must be positive"
            self.loose_clearance = loose_clearance
            self.tight_fit_clearance = tight_fit_clearance
            self.offset_tolerance = offset_tolerance

    class BearingConfig:
        def __init__(self, external_radius, internal_radius, height, gap):
            assert external_radius > internal_radius, "External radius must be greater than internal radius"
            assert internal_radius > 0, "Internal radius must be positive"
            assert height > 0, "Height must be positive"
            assert gap > 0, "Gap must be positive"
            self.external_radius = external_radius
            self.internal_radius = internal_radius
            self.height = height
            self.gap = gap

    class RollerConfig:
        def __init__(self, length, radius_near, radius_far, taper_angle, track_radius, crown_drop, crown_drop_2, num_points,
                     fillet_radius, num_rollers):
            assert length > 0, "Roller length must be positive"
            assert radius_near > 0, "Radius near must be positive"
            assert radius_far > 0, "Radius far must be positive"
            assert 0 < taper_angle < 90, f"Taper angle {taper_angle} must be between 0 and 90 degrees"
            assert track_radius > 0, "Track radius must be positive"
            assert crown_drop >= 0, "Crown drop must not be negative"
            assert crown_drop_2 >= 0, "Crown drop 2 must not be negative"
            assert num_points > 3, "Number of points must be greater than 3"
            assert fillet_radius > 0, "Fillet radius must be positive"
            assert num_rollers > 0, "Number of rollers must be positive"
            self.length = length
            self.radius_near = radius_near
            self.radius_far = radius_far
            self.taper_angle = taper_angle
            self.track_radius = track_radius
            self.crown_drop = crown_drop
            self.crown_drop_2 = crown_drop_2
            self.num_points = num_points
            self.fillet_radius = fillet_radius
            self.num_rollers = num_rollers

        @staticmethod
        def from_length_radius_near_radius_far(length, radius_near, radius_far, track_radius, crown_drop, crown_drop_2,
                                               num_points, fillet_radius, num_rollers):
            taper_angle = math.degrees(math.atan2(radius_far - radius_near, length))
            return RollerConfig(length, radius_near, radius_far, taper_angle, track_radius, crown_drop, crown_drop_2,  num_points,
                                fillet_radius, num_rollers)

        @staticmethod
        def from_length_radius_near_taper_angle(length, radius_near, taper_angle, track_radius, crown_drop, crown_drop_2,
                                                num_points, fillet_radius, num_rollers):
            radius_far = radius_near + length * math.tan(math.radians(taper_angle))
            return RollerConfig(length, radius_near, radius_far, taper_angle, track_radius, crown_drop, crown_drop_2,  num_points,
                                fillet_radius, num_rollers)

        @staticmethod
        def from_length_radius_far_taper_angle(length, radius_far, taper_angle, track_radius, crown_drop, crown_drop_2,
                                               num_points, fillet_radius, num_rollers):
            radius_near = radius_far - length * math.tan(math.radians(taper_angle))
            return RollerConfig(length, radius_near, radius_far, taper_angle, track_radius, crown_drop, crown_drop_2,  num_points,
                                fillet_radius, num_rollers)

        @staticmethod
        def from_radius_near_radius_far_taper_angle(radius_near, radius_far, taper_angle, track_radius, crown_drop, crown_drop_2,
                                                    num_points, fillet_radius, num_rollers):
            length = (radius_far - radius_near) / math.tan(math.radians(taper_angle))
            return RollerConfig(length, radius_near, radius_far, taper_angle, track_radius, crown_drop, crown_drop_2,  num_points,
                                fillet_radius, num_rollers)

    class CageConfig:
        def __init__(self, outer_radius, inner_radius, height, wall_thickness):
            assert outer_radius > inner_radius, "Outer radius must be greater than inner radius"
            assert inner_radius >= 0, "Inner radius cannot be negative"
            assert height > 0, "Height must be positive"
            assert wall_thickness > 0, "Wall thickness must be positive"
            self.outer_radius = outer_radius
            self.inner_radius = inner_radius
            self.height = height
            self.wall_thickness = wall_thickness
            self.thin_height = 2 * wall_thickness

    class HoleConfig:
        def __init__(self, side_length, cage_config):
            assert side_length > 0, "Hole side length must be positive"
            assert side_length < (cage_config.outer_radius - cage_config.inner_radius), "Hole side length too large for cage"
            self.side_length = side_length
            self.radial_position = (cage_config.outer_radius + cage_config.inner_radius - side_length/2) / 2

    class Config:
        def __init__(self, bearing, roller, cage, hole, offset):
            self.bearing = bearing
            self.roller = roller
            self.cage = cage
            self.hole = hole
            self.offset = offset
            self.split_plane_size = 2*self.bearing.external_radius+2

    def create_tapered_roller_bearing(config):
        # Derived variables
        cage_z_offset = -config.cage.height / 2
        thin_cylinder_z_offset = -config.cage.thin_height / 2
        split_plane_offset = -config.split_plane_size / 2
        insert_side_length = config.hole.side_length - 2 * config.offset.tight_fit_clearance

        # Create races
        top_race = create_top_race(config.bearing.height, config.bearing.internal_radius,
                                   config.bearing.external_radius, gap=config.bearing.gap)
        bottom_race = create_bottom_race(config.bearing.height, config.bearing.internal_radius,
                                         config.bearing.external_radius, gap=config.bearing.gap)
        track_cutout = create_tapered_roller_track_cutout(
            config.roller.length + 2 * config.offset.loose_clearance, config.roller.radius_near, config.roller.taper_angle,
            config.roller.num_points, config.roller.track_radius
        )
        #races = Part.Compound([top_race, bottom_race]).cut(track_cutout)
        top_race = top_race.cut(track_cutout)
        bottom_race = bottom_race.cut(track_cutout)

        # Create cage
        cage = Part.makeCylinder(config.cage.outer_radius, config.cage.height, FreeCAD.Vector(0, cage_z_offset, 0),
                                 FreeCAD.Vector(0, 1, 0))
        cage_hole = Part.makeCylinder(config.cage.inner_radius, config.cage.height,
                                       FreeCAD.Vector(0, cage_z_offset, 0),
                                       FreeCAD.Vector(0, 1, 0))
        cage = cage.cut(cage_hole)

        # Create rollers
        solid = create_crowned_tapered_roller(
            config.roller.length, config.roller.crown_drop, config.roller.crown_drop_2, config.roller.radius_near,
            config.roller.taper_angle, config.roller.num_points, config.roller.fillet_radius
        )
        solid = solid.translate(App.Vector(config.roller.length, 0, 0))

        revolved_shapes = []
        offset_shapes = []
        cage_keep_offset_shapes = []
        angle_increment_degrees = 360 / config.roller.num_rollers
        for i in range(config.roller.num_rollers):
            rotated_roller = solid.copy()
            rotation_angle = i * angle_increment_degrees
            rotated_roller.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), rotation_angle)
            revolved_shapes.append(rotated_roller)
            offset_shapes.append(
                rotated_roller.makeOffsetShape(config.offset.loose_clearance, tolerance=config.offset.offset_tolerance))
            cage_keep_offset_shapes.append(
                rotated_roller.makeOffsetShape(config.offset.loose_clearance + config.cage.wall_thickness,
                                               tolerance=config.offset.offset_tolerance)
            )
        rollers = Part.Compound(revolved_shapes)
        offset_rollers = Part.Compound(offset_shapes)

        # Create square holes and inserts
        hole_shapes = []
        insert_shapes = []
        for i in range(config.roller.num_rollers):
            angle = (i * angle_increment_degrees + angle_increment_degrees / 2) % 360
            hole = Part.makeBox(
                config.hole.side_length, config.cage.wall_thickness*2, config.hole.side_length,
                FreeCAD.Vector(-config.hole.side_length / 2, -config.cage.wall_thickness, -config.hole.side_length / 2),
                FreeCAD.Vector(0, 1, 0)
            )
            hole.translate(FreeCAD.Vector(config.hole.radial_position, 0, 0))
            hole.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), angle)
            hole_shapes.append(hole)
            insert = Part.makeBox(
                insert_side_length, config.cage.wall_thickness*2, insert_side_length,
                FreeCAD.Vector(-insert_side_length / 2, -config.cage.wall_thickness, -insert_side_length / 2),
                FreeCAD.Vector(0, 1, 0)
            )
            insert.translate(FreeCAD.Vector(config.hole.radial_position, 0, 0))
            insert.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), angle)
            insert_shapes.append(insert)
        holes = Part.Compound(hole_shapes)
        inserts = Part.Compound(insert_shapes)

        # Cut holes from cage
        cage = cage.cut(holes)

        # Cut rollers from cage
        cage2 = cage.cut(offset_rollers)

        # Create thin cylinder
        thin_cylinder = Part.makeCylinder(config.cage.outer_radius, config.cage.thin_height,
                                          FreeCAD.Vector(0, thin_cylinder_z_offset, 0),
                                          FreeCAD.Vector(0, 1, 0))
        inner_cylinder = Part.makeCylinder(config.cage.inner_radius, config.cage.thin_height,
                                           FreeCAD.Vector(0, thin_cylinder_z_offset, 0),
                                           FreeCAD.Vector(0, 1, 0))
        thin_cylinder = thin_cylinder.cut(inner_cylinder)
        cage_intersection_part_1 = Part.Compound([thin_cylinder] + cage_keep_offset_shapes)
        cage_cutter = cage.cut(cage_intersection_part_1)
        cage2 = cage2.cut(cage_cutter)

        # Split cage into halves
        plane = Part.makePlane(config.split_plane_size, config.split_plane_size,
                               FreeCAD.Vector(split_plane_offset, 0, split_plane_offset),
                               FreeCAD.Vector(0, 1, 0))
        sliced_parts = BOPTools.SplitAPI.slice(cage2, [plane], "Standard")
        cage_half1 = sliced_parts.SubShapes[0]
        cage_half2 = sliced_parts.SubShapes[1]

        # Aluminum colors
        aluminum_light = (0.95, 0.95, 0.95)  # Races, cage halves
        aluminum_dark = (0.85, 0.85, 0.85)  # Rollers, inserts

        #todo: add the initial bearing and insert to the shapes, but hidden, for 3d printing

        shapes = [top_race, bottom_race, cage_half1, cage_half2, rollers, inserts]
        names = ["top_race", "bottom_race", "cage_half1", "cage_half2", "rollers", "inserts"]
        colors = [aluminum_light, aluminum_light, aluminum_light, aluminum_light, aluminum_dark, aluminum_dark]

        return shapes, names, colors


    # Create document
    doc = FreeCAD.newDocument("TestDoc")
    FreeCAD.setActiveDocument("TestDoc")

    config = Config(
        bearing=BearingConfig(external_radius=45.0, internal_radius=15.0, height=30.0, gap=15.0),
        roller=RollerConfig.from_length_radius_near_radius_far(
            length=20.0, radius_near=7.5, radius_far=10, track_radius=19.5, crown_drop=1.0, crown_drop_2=0.5, num_points=21,
            fillet_radius=2, num_rollers=6
        ),
        cage=CageConfig(outer_radius=45.0, inner_radius=25.0, height=10.0, wall_thickness=2.0),
        hole=HoleConfig(side_length=4.0,
                        cage_config=CageConfig(outer_radius=45.0, inner_radius=25.0, height=10.0, wall_thickness=2.0)),
        offset=OffsetConfig(loose_clearance=0.5, tight_fit_clearance=0.125, offset_tolerance=0.01),
    )
    shapes, names, colors = create_tapered_roller_bearing(config)

    # Visualize
    show_feature_python_group(
        doc,
        shapes,
        names,
        "TaperedRollerBearing",
        colors=colors
    )

@run_in_freecad
def test_create_tapered_roller_bearing_3():
    import FreeCAD
    import Part
    import BOPTools.SplitAPI
    import math
    from freecad import app as App
    from freecad.actuators.bearing.makelThrustBearing import (
        create_tapered_roller_track_cutout,
        create_crowned_tapered_roller,
        create_top_race,
        create_bottom_race,
    )
    from freecad.actuators.tests_base import show_feature_python_group

    class OffsetConfig:
        def __init__(self, loose_clearance, tight_fit_clearance, offset_tolerance):
            assert loose_clearance > 0, "Loose clearance must be positive"
            assert tight_fit_clearance > 0, "Tight fit clearance must be positive"
            assert offset_tolerance > 0, "Offset tolerance must be positive"
            self.loose_clearance = loose_clearance
            self.tight_fit_clearance = tight_fit_clearance
            self.offset_tolerance = offset_tolerance

    class BearingConfig:
        def __init__(self, external_radius, internal_radius, height, gap):
            assert external_radius > internal_radius, "External radius must be greater than internal radius"
            assert internal_radius > 0, "Internal radius must be positive"
            assert height > 0, "Height must be positive"
            assert gap > 0, "Gap must be positive"
            self.external_radius = external_radius
            self.internal_radius = internal_radius
            self.height = height
            self.gap = gap

    class RollerConfig:
        def __init__(self, length, radius_near, radius_far, taper_angle, track_radius, crown_drop, crown_drop_2, num_points,
                     fillet_radius, num_rollers):
            assert length > 0, "Roller length must be positive"
            assert radius_near > 0, "Radius near must be positive"
            assert radius_far > 0, "Radius far must be positive"
            assert 0 < taper_angle < 90, f"Taper angle {taper_angle} must be between 0 and 90 degrees"
            assert track_radius > 0, "Track radius must be positive"
            assert crown_drop >= 0, "Crown drop must not be negative"
            assert crown_drop_2 >= 0, "Crown drop 2 must not be negative"
            assert num_points > 3, "Number of points must be greater than 3"
            assert fillet_radius > 0, "Fillet radius must be positive"
            assert num_rollers > 0, "Number of rollers must be positive"
            self.length = length
            self.radius_near = radius_near
            self.radius_far = radius_far
            self.taper_angle = taper_angle
            self.track_radius = track_radius
            self.crown_drop = crown_drop
            self.crown_drop_2 = crown_drop_2
            self.num_points = num_points
            self.fillet_radius = fillet_radius
            self.num_rollers = num_rollers

        @staticmethod
        def from_length_radius_near_radius_far(length, radius_near, radius_far, track_radius, crown_drop, crown_drop_2,
                                               num_points, fillet_radius, num_rollers):
            taper_angle = math.degrees(math.atan2(radius_far - radius_near, length))
            return RollerConfig(length, radius_near, radius_far, taper_angle, track_radius, crown_drop, crown_drop_2, num_points,
                                fillet_radius, num_rollers)

        @staticmethod
        def from_length_radius_near_taper_angle(length, radius_near, taper_angle, track_radius, crown_drop, crown_drop_2,
                                                num_points, fillet_radius, num_rollers):
            radius_far = radius_near + length * math.tan(math.radians(taper_angle))
            return RollerConfig(length, radius_near, radius_far, taper_angle, track_radius, crown_drop, crown_drop_2, num_points,
                                fillet_radius, num_rollers)

        @staticmethod
        def from_length_radius_far_taper_angle(length, radius_far, taper_angle, track_radius, crown_drop, crown_drop_2,
                                               num_points, fillet_radius, num_rollers):
            radius_near = radius_far - length * math.tan(math.radians(taper_angle))
            return RollerConfig(length, radius_near, radius_far, taper_angle, track_radius, crown_drop, crown_drop_2, num_points,
                                fillet_radius, num_rollers)

        @staticmethod
        def from_radius_near_radius_far_taper_angle(radius_near, radius_far, taper_angle, track_radius, crown_drop, crown_drop_2,
                                                    num_points, fillet_radius, num_rollers):
            length = (radius_far - radius_near) / math.tan(math.radians(taper_angle))
            return RollerConfig(length, radius_near, radius_far, taper_angle, track_radius, crown_drop, crown_drop_2, num_points,
                                fillet_radius, num_rollers)

    class CageConfig:
        def __init__(self, outer_radius, inner_radius, height, wall_thickness):
            assert outer_radius > inner_radius, "Outer radius must be greater than inner radius"
            assert inner_radius >= 0, "Inner radius cannot be negative"
            assert height > 0, "Height must be positive"
            assert wall_thickness > 0, "Wall thickness must be positive"
            self.outer_radius = outer_radius
            self.inner_radius = inner_radius
            self.height = height
            self.wall_thickness = wall_thickness
            self.thin_height = 2 * wall_thickness

    class HoleConfig:
        def __init__(self, side_length, cage_config):
            assert side_length > 0, "Hole side length must be positive"
            assert side_length < (cage_config.outer_radius - cage_config.inner_radius), "Hole side length too large for cage"
            self.side_length = side_length
            self.radial_position = (cage_config.outer_radius + cage_config.inner_radius - side_length / 2) / 2

    class Config:
        def __init__(self, bearing, roller, cage, hole, offset):
            self.bearing = bearing
            self.roller = roller
            self.cage = cage
            self.hole = hole
            self.offset = offset
            self.split_plane_size = 2 * self.bearing.external_radius + 2

    def create_races(config):
        top_race = create_top_race(config.bearing.height, config.bearing.internal_radius,
                                   config.bearing.external_radius, gap=config.bearing.gap)
        bottom_race = create_bottom_race(config.bearing.height, config.bearing.internal_radius,
                                         config.bearing.external_radius, gap=config.bearing.gap)
        track_cutout = create_tapered_roller_track_cutout(
            config.roller.length + 2 * config.offset.loose_clearance, config.roller.radius_near, config.roller.taper_angle,
            config.roller.num_points, config.roller.track_radius
        )
        top_race = top_race.cut(track_cutout)
        bottom_race = bottom_race.cut(track_cutout)
        return top_race, bottom_race

    def create_rollers(config):
        solid = create_crowned_tapered_roller(
            config.roller.length, config.roller.crown_drop, config.roller.crown_drop_2, config.roller.radius_near,
            config.roller.taper_angle, config.roller.num_points, config.roller.fillet_radius
        )
        solid = solid.translate(App.Vector(config.roller.length, 0, 0))
        revolved_shapes = []
        offset_shapes = []
        cage_keep_offset_shapes = []
        angle_increment_degrees = 360 / config.roller.num_rollers
        for i in range(config.roller.num_rollers):
  # continuation of roller creation
            rotated_roller = solid.copy()
            rotation_angle = i * angle_increment_degrees
            rotated_roller.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), rotation_angle)
            revolved_shapes.append(rotated_roller)
            offset_shapes.append(
                rotated_roller.makeOffsetShape(config.offset.loose_clearance, tolerance=config.offset.offset_tolerance))
            cage_keep_offset_shapes.append(
                rotated_roller.makeOffsetShape(config.offset.loose_clearance + config.cage.wall_thickness,
                                               tolerance=config.offset.offset_tolerance))
        rollers = Part.Compound(revolved_shapes)
        offset_rollers = Part.Compound(offset_shapes)
        return rollers, offset_rollers, cage_keep_offset_shapes

    def create_holes_and_inserts(config, cage_z_offset):
        hole_shapes = []
        insert_shapes = []
        angle_increment_degrees = 360 / config.roller.num_rollers
        insert_side_length = config.hole.side_length - 2 * config.offset.tight_fit_clearance
        for i in range(config.roller.num_rollers):
            angle = (i * angle_increment_degrees + angle_increment_degrees / 2) % 360
            hole = Part.makeBox(
                config.hole.side_length, config.cage.wall_thickness * 2, config.hole.side_length,
                FreeCAD.Vector(-config.hole.side_length / 2, -config.cage.wall_thickness, -config.hole.side_length / 2),
                FreeCAD.Vector(0, 1, 0)
            )
            hole.translate(FreeCAD.Vector(config.hole.radial_position, 0, 0))
            hole.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), angle)
            hole_shapes.append(hole)
            insert = Part.makeBox(
                insert_side_length, config.cage.wall_thickness * 2, insert_side_length,
                FreeCAD.Vector(-insert_side_length / 2, -config.cage.wall_thickness, -insert_side_length / 2),
                FreeCAD.Vector(0, 1, 0)
            )
            insert.translate(FreeCAD.Vector(config.hole.radial_position, 0, 0))
            insert.rotate(FreeCAD.Vector(0, 0, 0), FreeCAD.Vector(0, 1, 0), angle)
            insert_shapes.append(insert)
        holes = Part.Compound(hole_shapes)
        inserts = Part.Compound(insert_shapes)
        return holes, inserts

    def create_cage(config, offset_rollers, cage_keep_offset_shapes, holes):
        cage_z_offset = -config.cage.height / 2
        thin_cylinder_z_offset = -config.cage.thin_height / 2
        split_plane_offset = -config.split_plane_size / 2

        # Create base cage
        cage = Part.makeCylinder(config.cage.outer_radius, config.cage.height, FreeCAD.Vector(0, cage_z_offset, 0),
                                 FreeCAD.Vector(0, 1, 0))
        cage_hole = Part.makeCylinder(config.cage.inner_radius, config.cage.height,
                                      FreeCAD.Vector(0, cage_z_offset, 0), FreeCAD.Vector(0, 1, 0))
        cage = cage.cut(cage_hole)

        # Cut holes and rollers
        cage = cage.cut(holes)
        cage = cage.cut(offset_rollers)

        # Create thin cylinder
        thin_cylinder = Part.makeCylinder(config.cage.outer_radius, config.cage.thin_height,
                                         FreeCAD.Vector(0, thin_cylinder_z_offset, 0), FreeCAD.Vector(0, 1, 0))
        inner_cylinder = Part.makeCylinder(config.cage.inner_radius, config.cage.thin_height,
                                          FreeCAD.Vector(0, thin_cylinder_z_offset, 0), FreeCAD.Vector(0, 1, 0))
        thin_cylinder = thin_cylinder.cut(inner_cylinder)

        # Final cage cuts
        cage_intersection_part_1 = Part.Compound([thin_cylinder] + cage_keep_offset_shapes)
        cage_cutter = cage.cut(cage_intersection_part_1)
        cage = cage.cut(cage_cutter)

        # Split cage
        plane = Part.makePlane(config.split_plane_size, config.split_plane_size,
                               FreeCAD.Vector(split_plane_offset, 0, split_plane_offset),
                               FreeCAD.Vector(0, 1, 0))
        sliced_parts = BOPTools.SplitAPI.slice(cage, [plane], "Standard")
        cage_half1 = sliced_parts.SubShapes[0]
        cage_half2 = sliced_parts.SubShapes[1]

        return cage_half1, cage_half2

    def create_tapered_roller_bearing(config):
        # Create components
        top_race, bottom_race = create_races(config)
        rollers, offset_rollers, cage_keep_offset_shapes = create_rollers(config)
        holes, inserts = create_holes_and_inserts(config, -config.cage.height / 2)
        cage_half1, cage_half2 = create_cage(config, offset_rollers, cage_keep_offset_shapes, holes)

        # Aluminum colors
        aluminum_light = (0.95, 0.95, 0.95)  # Races, cage halves
        aluminum_dark = (0.85, 0.85, 0.85)   # Rollers, inserts

        # TODO: add the initial bearing and insert to the shapes, but hidden, for 3D printing
        shapes = [top_race, bottom_race, cage_half1, cage_half2, rollers, inserts]
        names = ["top_race", "bottom_race", "cage_half1", "cage_half2", "rollers", "inserts"]
        colors = [aluminum_light, aluminum_light, aluminum_light, aluminum_light, aluminum_dark, aluminum_dark]

        return shapes, names, colors

    # Create document
    doc = FreeCAD.newDocument("TestDoc")
    FreeCAD.setActiveDocument("TestDoc")

    config = Config(
        bearing=BearingConfig(external_radius=45.0, internal_radius=15.0, height=30.0, gap=15.0),
        roller=RollerConfig.from_length_radius_near_radius_far(
            length=20.0, radius_near=7.5, radius_far=10.0, track_radius=19.5, crown_drop=1.0, crown_drop_2=0.5, num_points=21,
            fillet_radius=2.0, num_rollers=6
        ),
        cage=CageConfig(outer_radius=45.0, inner_radius=25.0, height=10.0, wall_thickness=2.0),
        hole=HoleConfig(side_length=4.0,
                        cage_config=CageConfig(outer_radius=45.0, inner_radius=25.0, height=10.0, wall_thickness=2.0)),
        offset=OffsetConfig(loose_clearance=0.5, tight_fit_clearance=0.125, offset_tolerance=0.01),
    )
    shapes, names, colors = create_tapered_roller_bearing(config)

    # Visualize
    show_feature_python_group(
        doc,
        shapes,
        names,
        "TaperedRollerBearing",
        colors=colors
    )