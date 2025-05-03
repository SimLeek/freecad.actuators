import FreeCAD,FreeCADGui,Part,math
from BasicShapes import Shapes
from BOPTools import BOPFeatures



def CheckForInputErrors(in_d, out_d, height, wall_thick, ball_rounding):
	if out_d <= in_d:
		print ("out_d <= in_d")
		return -99

	if wall_thick * 2 >= height:
		print ("wall_thick * 2 >= height")
		return -99

	ball_d = CalculateBallDiameter(height, wall_thick, ball_rounding)
	if ball_d < ball_rounding:
		print ("Ball too small")
		return -99

	if in_d + wall_thick + ball_d + ball_d >= out_d:
		print ("Can't fit ball ",ball_d, "mm between the races")
		return -99
	return 0



def CalculateBallDiameter(height, wall_thickness, ball_rounding):
	precise_ball_diameter = height - (2 * wall_thickness)
	rounded_down_ball_diameter = math.floor(precise_ball_diameter/ball_rounding) * ball_rounding

	return rounded_down_ball_diameter
	
	
	
def CreateInnerRace(height, int_radius, ext_radius, ball_diam):
	tube = Shapes.addTube(FreeCAD.ActiveDocument, "myTube")
	tube.Height = height
	tube.InnerRadius = int_radius
	tube.OuterRadius = ext_radius/2 + int_radius/2
	App.ActiveDocument.getObject('Part').addObject(App.ActiveDocument.ActiveObject)
	
	doc = App.activeDocument()
	torus = doc.addObject("Part::Torus", "torus")
	torus.Radius1 = ext_radius
	torus.Radius2 = ball_diam/2
	torus.Placement = App.Placement(App.Vector(0, 0, height/2), App.Rotation())
	
	bp = BOPFeatures.BOPFeatures(App.activeDocument())
	bp.make_cut(["myTube", "torus", ])
	
	App.ActiveDocument.recompute()
	
	return



def CreateOuterRace(height, int_radius, ext_radius, ball_diam):
	tube = Shapes.addTube(FreeCAD.ActiveDocument, "myTube001")
	tube.Height = height
	tube.InnerRadius = ext_radius/2 + int_radius/2
	tube.OuterRadius = ext_radius
	App.ActiveDocument.getObject('Part001').addObject(App.ActiveDocument.ActiveObject)
	
	doc = App.activeDocument()
	torus = doc.addObject("Part::Torus", "torus001")
	torus.Radius1 = int_radius
	torus.Radius2 = ball_diam/2
	torus.Placement = App.Placement(App.Vector(0, 0, height/2), App.Rotation())
	
	bp = BOPFeatures.BOPFeatures(App.activeDocument())
	bp.make_cut(["myTube001", "torus001", ])
	
	FreeCAD.ActiveDocument.recompute()
	return



def CreateCage(in_radius, out_radius, ball_diam, cage_height, height):
	
	tube = Shapes.addTube(FreeCAD.ActiveDocument, "myTube002")
	tube.Height = cage_height
	tube.InnerRadius = in_radius
	tube.OuterRadius = out_radius
	tube_z = (height - (cage_height + ball_diam * 0.25)) / 2
	tube.Placement = App.Placement(App.Vector(0, 0, tube_z), App.Rotation())
	
	ball_placement_radius = out_radius / 2 + in_radius / 2
	ball_z = (cage_height + ball_diam * 0.25) - ball_diam * 0.5
	
	doc = App.activeDocument()
	sphere = doc.addObject("Part::Sphere", "mySphere")
	sphere.Radius = ball_diam / 2
	sphere.Placement = App.Placement(App.Vector(ball_placement_radius, 0, ball_z), App.Rotation())
	
	App.ActiveDocument.getObject('Part002').addObject(App.ActiveDocument.ActiveObject)
	bp = BOPFeatures.BOPFeatures(App.activeDocument())
	bp.make_cut(["myTube002", "mySphere", ])
	


	half_circumference = ball_placement_radius * math.pi
	num_balls = math.floor(half_circumference/ball_diam)
	separation_angle = (2 * math.pi) / num_balls
	next_angle = separation_angle

	for i in range(1,num_balls):
		part_name = "mySphere00" + str(i)
		cut_name = "Cut00" + str(i+1)
		sphere = doc.addObject("Part::Sphere", part_name)
		sphere.Radius = ball_diam / 2
		sphere.Placement = App.Placement(App.Vector(ball_placement_radius * math.cos(next_angle), ball_placement_radius * math.sin(next_angle), ball_z), App.Rotation())
		
		App.ActiveDocument.getObject('Part002').addObject(App.ActiveDocument.ActiveObject)
		bp = BOPFeatures.BOPFeatures(App.activeDocument())

		bp.make_cut([cut_name, part_name, ])

		
		next_angle += separation_angle

	return

def CreateBallBearing(int_diam, ext_diam, height, wall_thickness, ball_rounding):
#	
#	if CheckForInputErrors((int_diam, ext_diam, height, wall_thicknes, ball_rounding) !=0:
#		return 1
#		
	ball_diam = CalculateBallDiameter(height, wall_thickness, ball_rounding)
#	if ball_diam < ball_rounding:
#		<<error handling>>

#	ext_diam is diameter. 1/2 diameter = radius. 1/2 of that radius gives us the mid-point radius.
	mid_radius = ext_diam/4 + int_diam/4
	inner = App.ActiveDocument.addObject("App::Part", "Part")
	inner.Label = 'Inner Race'
	CreateInnerRace(height, int_diam/2, mid_radius, ball_diam)

	outer = App.ActiveDocument.addObject("App::Part", "Part001")
	outer.Label = "Outer Race"
	CreateOuterRace(height, mid_radius, ext_diam/2, ball_diam)

	#note that we take adjust the radii to allow for fitting
	#into the bearing and lubrication in operation
	cage_in_radius = mid_radius/2 + int_diam/4 + ball_diam / 4
	cage_out_radius = ext_diam/4 + mid_radius/2 - ball_diam / 4
	
	cage_height = 0.75 * ball_diam + wall_thickness
	cage = App.ActiveDocument.addObject("App::Part", "Part002")
	cage.Label = "Cage"
	
	CreateCage(cage_in_radius, cage_out_radius, ball_diam, cage_height, height)
	
	ball = App.ActiveDocument.addObject("App::Part", "Part003")
	ball.Label = "Bearing Ball"
	doc = App.activeDocument()
	sphere = doc.addObject("Part::Sphere", "mySphere")
	sphere.Radius = ball_diam / 2
	App.ActiveDocument.getObject('Part003').addObject(App.ActiveDocument.ActiveObject)
	

	FreeCAD.ActiveDocument.recompute()
	Gui.SendMsgToActiveView("ViewFit")
	Gui.activeDocument().activeView().viewIsometric()



class BoxTaskPanel():
	def __init__(self):
		# this will create a Qt widget from our ui file
		self.form = FreeCADGui.PySideUic.loadUi(path_to_ui)

	#Things to do if user presses the "OK" button
	def accept(self):

		FreeCADGui.Control.closeDialog()
		in_d = self.form.Int_Diam.value()
		out_d = self.form.Ext_Diam.value()
		height =self.form.B_Height.value()
		wall_thick = self.form.Min_Wall_Thick.value()
		ball_rounding = self.form.Ball_Rounding.value()

		if (CheckForInputErrors(in_d, out_d, height, wall_thick, ball_rounding)) != 0:
			FreeCADGui.Control.closeDialog()
			return 1

		CreateBallBearing(in_d, out_d, height, wall_thick, ball_rounding)

		return 0

	#Things to do if user presses the "Cancel" button
	def reject(self):
		FreeCADGui.Control.closeDialog()



path_to_ui = os.path.join(os.path.dirname(__file__), "form.ui")
App.newDocument("Ball_Bearing")
doc_name = FreeCAD.ActiveDocument.Name
panel = BoxTaskPanel()
FreeCADGui.Control.showDialog(panel)