import os.path
import sys
from freecad import app
from freecad import gui

__dirname__ = os.path.dirname(__file__)

if sys.version_info[0] == 3 and sys.version_info[1] >= 11:
    # only works with 0.21.2 and above

    FC_MAJOR_VER_REQUIRED = 0
    FC_MINOR_VER_REQUIRED = 21
    FC_PATCH_VER_REQUIRED = 2
    FC_COMMIT_REQUIRED = 33772

    # Check FreeCAD version
    app.Console.PrintLog("Checking FreeCAD version\n")
    ver = app.Version()
    major_ver = int(ver[0])
    minor_vers = ver[1].split(".")
    minor_ver = int(minor_vers[0])
    if minor_vers[1:] and minor_vers[1]:
        patch_ver = int(minor_vers[1])
    else:
        patch_ver = 0
    gitver = ver[2].split()
    if gitver:
        gitver = gitver[0]
    if gitver and gitver != "Unknown":
        gitver = int(gitver)
    else:
        # If we don't have the git version, assume it's OK.
        gitver = FC_COMMIT_REQUIRED

    if major_ver < FC_MAJOR_VER_REQUIRED or (
            major_ver == FC_MAJOR_VER_REQUIRED
            and (
                    minor_ver < FC_MINOR_VER_REQUIRED
                    or (
                            minor_ver == FC_MINOR_VER_REQUIRED
                            and (
                                    patch_ver < FC_PATCH_VER_REQUIRED
                                    or (
                                            patch_ver == FC_PATCH_VER_REQUIRED
                                            and gitver < FC_COMMIT_REQUIRED
                                    )
                            )
                    )
            )
    ):
        app.Console.PrintWarning(
            "FreeCAD version (currently {}.{}.{} ({})) must be at least {}.{}.{} ({}) in order to work with Python 3.11 and above\n".format(
                int(ver[0]),
                minor_ver,
                patch_ver,
                gitver,
                FC_MAJOR_VER_REQUIRED,
                FC_MINOR_VER_REQUIRED,
                FC_PATCH_VER_REQUIRED,
                FC_COMMIT_REQUIRED,
            )
        )


class ActuatorWorkbench(gui.Workbench):
    MenuText = "Actuator"
    ToolTip = "Actuator Workbench"
    Icon = os.path.join(__dirname__, "icons", "actuatorworkbench.svg")
    commands = [
        #"CreateMotor",
        "CreatePlanetary",
        "CreateAxleConnector",
        "CreateBearing"
        #"CreateSplitRing",
        #"CreateBevel",
        #"CreatePulley",
        #"CreateRollerScrew",
        #"CreateSpring"
    ]

    def GetClassName(self):
        return "Gui::ActuatorWorkbench"

    def Initialize(self):
        # gui.addLanguagePath(os.path.join(os.path.dirname(__file__), "translations"))
        # gui.updateLocale()

        from .commands import (
            #CreateMotor,
            CreatePlanetary,
            CreateAxleConnector,
            CreateAxialThrustBearingCommand
            #CreateSplitRing,
            #CreateBevel,
            #CreatePulley,
            #CreateRollerScrew,
            #CreateSpring,
        )

        self.appendToolbar("Actuator", self.commands)
        self.appendMenu("Actuator", self.commands)
        #gui.addCommand("CreateMotor", CreateMotor())
        gui.addCommand("CreatePlanetary", CreatePlanetary())
        gui.addCommand("CreateAxleConnector", CreateAxleConnector())
        gui.addCommand("CreateBearing", CreateAxialThrustBearingCommand())

        #gui.addCommand("CreateSplitRing", CreateSplitRing())
        #gui.addCommand("CreateBevel", CreateBevel())
        #gui.addCommand("CreatePulley", CreatePulley())
        #gui.addCommand("CreateRollerScrew", CreateRollerScrew())
        #gui.addCommand("CreateSpring", CreateSpring())

    def Activated(self):
        pass

    def Deactivated(self):
        pass


gui.addWorkbench(ActuatorWorkbench())
