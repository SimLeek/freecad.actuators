# -*- coding: utf-8 -*-
# ***************************************************************************
# *                                                                         *
# * This program is free software: you can redistribute it and/or modify    *
# * it under the terms of the GNU General Public License as published by    *
# * the Free Software Foundation, either version 3 of the License, or       *
# * (at your option) any later version.                                     *
# *                                                                         *
# * This program is distributed in the hope that it will be useful,         *
# * but WITHOUT ANY WARRANTY; without even the implied warranty of          *
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           *
# * GNU General Public License for more details.                            *
# *                                                                         *
# * You should have received a copy of the GNU General Public License       *
# * along with this program.  If not, see <http://www.gnu.org/licenses/>.   *
# *                                                                         *
# ***************************************************************************

import os
import sys
import numpy as np

from freecad import app
from freecad import gui
import Part
import FreeCAD

from .organic.makefill_tube import build_axle_solid

# ---------------------------------------------------------------------------
# View Provider for the Axle Connector
# ---------------------------------------------------------------------------
class ViewProviderAxleConnector(object):
    def __init__(self, vobj, icon_fn=None):
        vobj.Proxy = self
        dirname = os.path.dirname(__file__)
        # Use a different icon if desired:
        self.icon_fn = icon_fn or os.path.join(dirname, "icons", "axleconnector.svg")

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


# ---------------------------------------------------------------------------
# AxleConnector: A connector that mates an arbitrary number of gears by
# projecting their centers onto an axle (defined by the connector’s Placement)
# and aligning their rotations. For each gear, if gear.fixed is True the gear
# exactly follows the axle’s rotation; if not, it preserves its twist about
# the axle.
# ---------------------------------------------------------------------------
class AxleConnector(object):
    def __init__(self, obj, gears):
        # A version property for compatibility
        obj.addProperty(
            "App::PropertyString",
            "version",
            "version",
            "freecad.actuator-version",
            1,
        )
        # A list property for the gears attached to this axle connector.
        obj.addProperty(
            "App::PropertyLinkList",
            "gears",
            "gear",
            "List of gears on the axle",
            0
        )
        obj.addProperty(
            "App::PropertyLength",
                        "clearance",
                        "Axle",
                        "Clearance between gear and axle",
                        0
        )
        obj.addProperty(
            "App::PropertyLength",
            "sweep_increment",
            "Axle",
            "Axial sampling increment (mm)",
            0
        )
        obj.addProperty(
            "App::PropertyEnumeration",
            "cross_section_type",
            "Axle",
            "Type of cross section",
            0)
        obj.cross_section_type = ["Circle", "Square", "Hexagon", "D", "Double-D", "Spline"]
        obj.addProperty(
            "App::PropertyBool",
            "organic",
            "Axle",
            "If true, make the in-air shaft diameter always equal to what's required for the safety factor, "
            "not just the max",
            0)
        obj.addProperty(
            "App::PropertyBool",
            "is_air_cross_section_same",
            "Axle",
            "If true, the cross section in air is the same as when connecting to gears. If false, it's circular.",
            0)
        obj.clearance = 0
        obj.sweep_increment = 0.5
        obj.organic = False
        obj.is_air_cross_section_same = True
        obj.version = "0.0.0"
        obj.gears = gears  # initial list of gears
        obj.Proxy = self
        self.auto_compute_shape = True
        self.shape_func = Part.Circle  # one function or a list of tuples of function-mm distance pairs

    def get_diameters(self, fp, t):
        return 10 + 1.5 * np.sin(t * 2 * np.pi / 50)  # example func, not real

    def generateAxle(self, fp):
        pl = fp.Placement
        base = pl.Base
        #rot = pl.Rotation
        axle_dir = pl.Rotation * FreeCAD.Vector(0,0,1)
        #axle_dir = pl.Rotation.Axis
        ts = []
        for gear in fp.gears:
            v1 = gear.Placement.Base - base
            v2 = gear.Placement.Base + float(gear.height)*axle_dir - base

            t1 = v1.dot(axle_dir)
            t2 = v2.dot(axle_dir)

            ts.append((t1, t2))
        if not ts:
            return None
        print(ts)

        t_min = min([t[0] for t in ts])
        t_max = max([t[1] for t in ts])
        length = t_max - t_min
        if length < 1e-6:
            return None

        def gen_gear_axle_part(gear_len):
            length = gear_len[1] - gear_len[0]
            if length < 1e-6:
                return
            d_max=-1
            for i in np.arange(gear_len[0], gear_len[1] + float(fp.sweep_increment), float(fp.sweep_increment)):
                d = self.get_diameters(fp, i)
                if d > d_max:
                    d_max = d

            start_point = gear_len[0] * FreeCAD.Vector(0,0,1)
            # Create a circle in a plane perpendicular to the axle.
            circle = self.shape_func(start_point, FreeCAD.Vector(0,0,1), d_max/2.0)
            circle_edge = circle.toShape()
            circle_wire = Part.Wire([circle_edge])
            circle_face = Part.Face(circle_wire)
            extrusion = circle_face.extrude(FreeCAD.Vector(0,0,1) * length)
            return extrusion

        def get_air_axle_part(air_len):
            if fp.organic:
                d_start = self.get_diameters(fp, air_len[0])
                start_point = air_len[0] * FreeCAD.Vector(0,0,1)
                if fp.is_air_cross_section_same:
                    circle = self.shape_func(start_point, FreeCAD.Vector(0,0,1), d_start / 2)
                else:
                    circle = Part.Circle(start_point, FreeCAD.Vector(0,0,1), d_start / 2)
                circle_edge = circle.toShape()
                circle_wire = Part.Wire([circle_edge])
                #circle_face = Part.Face(circle_wire)

                extrusion = build_axle_solid(circle_wire, FreeCAD.Vector(0,0,1), air_len[0], air_len[1], self.get_diameters,fp, float(fp.sweep_increment))
            else:
                length = air_len[1] - air_len[0]
                start_point = air_len[0] * FreeCAD.Vector(0,0,1)
                if length < 1e-6:
                    return
                d_max = -1
                for i in np.arange(air_len[0], air_len[1] + float(fp.sweep_increment), float(fp.sweep_increment)):
                    d = self.get_diameters(fp, i)
                    if d > d_max:
                        d_max = d
                if fp.is_air_cross_section_same:
                    circle = self.shape_func(start_point, FreeCAD.Vector(0,0,1), d_max/2)
                else:
                    circle = Part.Circle(start_point, FreeCAD.Vector(0,0,1), d_max/2)
                circle_edge = circle.toShape()
                circle_wire = Part.Wire([circle_edge])
                circle_face = Part.Face(circle_wire)
                extrusion = circle_face.extrude(FreeCAD.Vector(0,0,1) * length)
            return extrusion

        parts = []
        for e, gear_start_end in enumerate(ts):
            print(f"ad:{axle_dir}")
            parts.append(gen_gear_axle_part(gear_start_end))

            try:
                print(f"ad:{axle_dir}")
                air_len = (gear_start_end[1], ts[e+1][0])
                parts.append(get_air_axle_part(air_len))
            except IndexError:
                pass  # done

        full_axle = Part.Compound(parts)
        #full_axle.Placement.rotate(pl.Rotation)
        #full_axle.Placement.Rotation = pl.Rotation.inverse()

        return full_axle


    def onChanged(self, fp, prop):
        # The connector's Placement defines the axle.
        axle_base = fp.Placement.Base
        axle_rot = fp.Placement.Rotation
        # Assume the axle runs along the connector's local Z-axis.
        axle_dir = axle_rot.multVec(app.Vector(0, 0, 1))
        # Use the local X-axis as reference for twist calculations.
        axle_x = axle_rot.multVec(app.Vector(1, 0, 0))

        # Process every gear attached to the connector.
        for gear in fp.gears:
            # Project the gear's center onto the axle.
            v = gear.Placement.Base - axle_base
            t = v.dot(axle_dir)
            new_center = axle_base + t * axle_dir

            # Check the gear's "fixed" property.
            if hasattr(gear, "fixed") and gear.fixed:
                # If the gear is fixed, it should match the axle's rotation exactly.
                new_rot = axle_rot
            else:
                # Otherwise, allow the gear to twist freely.
                # Compute the twist angle by projecting the gear's local X-axis into
                # the plane perpendicular to the axle.
                gear_x = gear.Placement.Rotation.multVec(app.Vector(1, 0, 0))
                proj = gear_x - (gear_x.dot(axle_dir)) * axle_dir
                twist_angle = 0
                if proj.Length > 1e-6:
                    proj.normalize()
                    # Calculate the angle between the connector's X-axis and the projected gear X-axis.
                    dot = axle_x.dot(proj)
                    dot = max(min(dot, 1.0), -1.0)
                    twist_angle = np.arccos(dot)
                    # Determine the sign of the twist using the cross product.
                    cross = axle_x.cross(proj)
                    if cross.dot(axle_dir) < 0:
                        twist_angle = -twist_angle

                twist_rot = app.Rotation(axle_dir, twist_angle)
                new_rot = axle_rot * twist_rot

            # Update the gear's placement with the new center and rotation.
            new_placement = app.Placement(new_center, new_rot)
            gear.Placement = new_placement

    def execute(self, fp):
        self.onChanged(fp, None)

        inc = float(fp.sweep_increment)
        cs_type_index = fp.cross_section_type

        #todo: fill in the rest of the 6 shapes
        cs_type_str = {0: "circle", 1: "square", 2: "hexagon"}.get(cs_type_index, "circle")
        if cs_type_str=="circle":
            self.shape_func = Part.Circle

        solid = self.generateAxle(fp)
        if solid:
            fp.Shape = solid
        #FreeCAD.ActiveDocument.recompute()

class CreateAxleConnector:
    def GetResources(self):
        return {
            'MenuText': 'Create Axle Connection between Gears',
            'ToolTip': 'Create an axle connection between multiple gears',
            'Pixmap': os.path.join(os.path.dirname(__file__), "compiled_ui", "axle-connector.svg")
        }

    def Activated(self):
        try:
            selection = gui.Selection.getSelection()

            obj = app.ActiveDocument.addObject("Part::FeaturePython", "AxleConnector")
            if len(selection) >= 1:
                obj.Placement = selection[0].Placement
            AxleConnector(obj, selection)
            ViewProviderAxleConnector(obj.ViewObject)

            #AxleConnectorDialog(obj).show()

            app.ActiveDocument.recompute()
            return obj
        except Exception as e:
            app.Console.PrintError(f"Error: {str(e)}\n")
            return None
