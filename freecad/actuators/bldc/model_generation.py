from freecad.actuators.bldc.serialize import BLDCParameters
from freecad.actuators.tests_base import run_in_freecad, show_feature_python_group
from typing import Any

@run_in_freecad
def test_generate_bldc_model():
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
