import FreeCAD, Part, numpy as np
from FreeCAD import Vector
from Part import BRepOffsetAPI

'''
def example_diameter_callback(t):
    # Example: a simple sine modulation on a base diameter of 10.
    return 10 + 1.5 * np.sin(t * 2 * np.pi / 50)
'''

def sample_axial_path(t_min, t_max, increment, diameter_callback, fp):
    ts = np.arange(t_min, t_max + increment, increment)
    diameters = [diameter_callback(fp, t) for t in ts]
    return ts, diameters


#def extract_profile_wires(sketch_obj):
#    """
#    Given a Sketch object, return its wires (as a list).
#    Assumes that sketch_obj.Shape contains the geometry.
#    """
#    shape = sketch_obj.Shape
#    return shape.Wires  # returns a list of wires


def transform_wire(wire, scale, translation):
    """
    Returns a transformed copy of the given wire by scaling about (0,0,0)
    and then translating.
    """
    wire_copy = wire.copy()
    # Apply scaling: create a scaling matrix.
    # Note: FreeCAD does not have a direct scaling transform for wires;
    # one common approach is to convert to a compound and use a scaling matrix.
    m = FreeCAD.Matrix()
    m.A11 = scale
    m.A22 = scale
    m.A33 = scale
    wire_copy.transformGeometry(m)
    # Now translate:
    wire_copy.translate(translation)
    return wire_copy


def generate_transformed_profiles(baseProfileSketch, dir, ts, diameters, ):
    """
    For each axial sample, extract the base profile wires from the base sketch,
    scale them by factor = (diameter / D_max) and translate them along the axle.
    Returns a list (one per sample) of lists of wires.
    """
    #base_wires = extract_profile_wires(baseProfileSketch)
    base_wires = baseProfileSketch
    # Determine maximum distance from center of the base profile.
    # Here, we assume the base profile's wires are drawn centered at (0,0).
    print(base_wires.Vertexes)
    r_max = max([np.sqrt(sum([x**2 for x in v])) for v in base_wires.Vertexes])
    transformed_profiles = []
    for t, dia in zip(ts, diameters):
        scale = dia / (r_max*2.0)
        translation = dir.multiply(t)
        transformed = [transform_wire(w, scale, translation) for w in base_wires]
        transformed_profiles.append(transformed)
    return transformed_profiles


def create_surface_from_rails(rail_wires):
    """
    Given a list of wires (one from each sample for a given profile curve),
    create a filling surface using BRepOffsetAPI_MakeFill.
    """
    # Build a list of edges from each wire.
    # We assume each rail_wire is a continuous edge (or wire) and use them directly.
    fillMaker = BRepOffsetAPI.MakeFill(rail_wires)
    fillMaker.Build()
    return fillMaker.Shape()


def generate_axle_surfaces(base_drawing, dir, t1, t2, diameter_callback, fp, increment=0.5):
    # Determine axial limits from gears.
    ts, diameters = sample_axial_path(t1, t2, increment, diameter_callback, fp)

    # Generate transformed profile wires at each axial sample.
    profiles = generate_transformed_profiles(base_drawing, dir, ts, diameters)
    # every sample yields the same number of wires.
    n = len(profiles[0])
    rails = []
    # For each wire index, collect that wire from every sample.
    for i in range(n):
        rail = [profiles[j][i] for j in range(len(profiles))]
        rails.append(rail)
    # Create surfaces for each rail.
    surfaces = [create_surface_from_rails(rail) for rail in rails]

    # Create end caps from first and last profiles (by joining the wires)
    def cap_from_profile(profile_wires):
        # Create a compound of all wires and attempt to form a face.
        comp = Part.Compound(profile_wires)
        try:
            face = Part.Face(comp)
        except Exception:
            # Fallback: if it fails, simply return None.
            face = None
        return face

    cap1 = cap_from_profile(profiles[0])
    cap2 = cap_from_profile(profiles[-1])
    return surfaces, (cap1, cap2)


def build_axle_solid(base_drawing, dir, t1, t2, diameter_callback, fp, increment=0.5):
    surfaces, caps = generate_axle_surfaces(base_drawing, dir, t1, t2, diameter_callback, fp, increment)
    if surfaces is None:
        return None
    # Sew all surfaces together.
    all_surfs = surfaces[:]
    for cap in caps:
        if cap is not None:
            all_surfs.append(cap)
    shell = Part.makeShell(all_surfs)
    try:
        solid = Part.makeSolid(shell)
    except Exception as e:
        FreeCAD.Console.PrintError("Solid creation failed: " + str(e) + "\n")
        solid = shell
    return solid
