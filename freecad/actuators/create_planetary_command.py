import os
import time
import math as m
import FreeCAD
import FreeCADGui as Gui
import Part
from freecad import app
import freecad.gears.connector as gear_connector
import freecad.gears.commands as gears  # For access to the gear creation functions

try:
    from PySide2 import QtWidgets, QtCore
except ImportError:
    from PySide import QtWidgets, QtCore
# Import your custom dialog
from .planetary_dialog import PlanetaryDialog

def create_planetary(
sun_teeth,
planet_teeth,
num_planets,
module,
height,
beta,
double_helix,
        pressure_angle,
        thickness=None,  # thickness MUST be larger than 1 module
        clearance=0.25  # mm
):
    # ensure types
    sun_teeth = int(sun_teeth)
    planet_teeth = int(planet_teeth)
    num_planets = int(num_planets)
    module = float(module)
    height = float(height)
    beta = float(beta)
    double_helix = bool(double_helix)
    print(f"module: {module}")
    if thickness is None:
        thickness = 2.5*module
    thickness = float(thickness)  # thickness MUST be larger than 1 module
    clearance = float(clearance)
    print(f"thickness: {thickness}")
    print(f"height: {height}")

    # Calculate ring teeth from provided parameters.
    ring_teeth = 2 * planet_teeth + sun_teeth

    # --- Create the Planetary Gears Assembly in the Main Thread ---

    # Create the Sun Gear
    sun_gear = gears.CreateInvoluteGear.create()
    sun_gear.Label = "Sun Gear"
    sun_gear.teeth = sun_teeth
    sun_gear.height = height
    sun_gear.module = module
    sun_gear.beta = -beta
    sun_gear.double_helix = double_helix
    sun_gear.clearance = clearance
    sun_gear.pressure_angle = pressure_angle

    # Create the Ring Gear
    ring_gear = gears.CreateInternalInvoluteGear.create()
    ring_gear.Label = "Ring Gear"
    ring_gear.teeth = ring_teeth
    ring_gear.height = height
    ring_gear.module = module
    ring_gear.beta = beta
    ring_gear.double_helix = double_helix
    ring_gear.thickness = thickness  # mm
    ring_gear.clearance = clearance
    ring_gear.pressure_angle = pressure_angle

    # Create the Planet Gears
    planet_gears = []
    for i in range(num_planets):
        planet_gear = gears.CreateInvoluteGear.create()
        planet_gear.Label = f"Planet Gear {i + 1}"
        planet_gear.teeth = planet_teeth
        planet_gear.height = height
        planet_gear.module = module
        planet_gear.beta = beta
        planet_gear.double_helix = double_helix
        planet_gear.clearance = clearance
        planet_gear.pressure_angle = pressure_angle
        planet_gears.append(planet_gear)

    #FreeCAD.ActiveDocument.recompute()

    # Position the Ring Gear
    if ring_teeth % 2 == 0:
        ring_gear.Placement = FreeCAD.Placement(
            FreeCAD.Vector(0, 0, 0),
            FreeCAD.Rotation(180.0 / ring_teeth, 0, 0)
        )

    # Create Gear Connectors between the Sun and each Planet Gear
    for i, planet_gear in enumerate(planet_gears):
        connector = app.ActiveDocument.addObject("Part::FeaturePython", f"Sun to Planet {i + 1} Connector")
        # Instantiate a GearConnector to join the sun gear with the current planet gear.
        gear_connector.GearConnector(connector, master_gear=sun_gear, slave_gear=planet_gear)
        connector.angle1 = (360.0 / num_planets) * i

    # Create the Connector between a Planet Gear and the Ring Gear
    connector = app.ActiveDocument.addObject("Part::FeaturePython", "Planet to Ring Connector")
    gear_connector.GearConnector(connector, master_gear=planet_gears[0], slave_gear=ring_gear)
    connector.angle1 = 0


class CreatePlanetary:
    """Command that opens the PlanetaryDialog and creates the planetary gear assembly
    once the user clicks Finish."""

    def GetResources(self):
        return {
            'MenuText': 'Create Planetary',
            'ToolTip': 'Open the Planetary Dialog and create a planetary gear set',
            'Pixmap': os.path.join(os.path.dirname(__file__), "icons", "planetary.svg")
        }

    def Activated(self):
        # Open the PlanetaryDialog non-modally (no separate tasks panel)
        self.dialog = PlanetaryDialog()
        self.dialog.ui.finishButton.clicked.connect(self.finish_clicked)
        self.dialog.ui.cancelButton.clicked.connect(self.dialog.close)
        self.dialog.setWindowModality(QtCore.Qt.NonModal)
        self.dialog.show()

    def finish_clicked(self):
        # Retrieve information from the dialog.
        info = self.dialog.finish_return()
        # Close the dialog.
        self.dialog.close()

        create_planetary(info.sun_teeth,
                         info.planet_teeth,
                         info.num_planets,
                         info.module,
                         info.height,
                         info.beta,
                         info.is_double_helix,
                         info.pressure_angle)

        # Recompute the document to reflect the new objects.
        FreeCAD.ActiveDocument.recompute()

    def IsActive(self):
        return True
