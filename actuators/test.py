# macro recording stuff

import freecad.gears.commands
freecad.gears.commands.CreateInvoluteGear.create()
FreeCAD.getDocument('Unnamed1').getObject('InvoluteGear').teeth = 12
FreeCAD.getDocument('Unnamed1').getObject('InvoluteGear').module = '1 mm'
FreeCAD.getDocument('Unnamed1').getObject('InvoluteGear').height = '5 mm'