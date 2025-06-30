import numpy as np
import vtk

# Parameters
H = 2.0  # Width of prism
W = 1.0  # Height of prism
D = 3.0  # Depth of prism
c = 0.1  # wire radius
#p = 0.25  # Pitch (z-advance per turn)
p = c
turns = [[0, 12], [11, 1], [2, 10], [9, 3], [4, 8], [7, 5]]  # Number of full turns
points_per_turn = 600  # Number of points for smooth curve



# Generate t values for 12 turns
#t = np.linspace(0, num_turns * 2 * np.pi, num_points)

# Initialize arrays for points
points = vtk.vtkPoints()
#x_coords = np.zeros(num_points)
#y_coords = np.zeros(num_points)
#z_coords = np.zeros(num_points)
x_coords = []
y_coords = []
z_coords = []
from freecad.actuators.util import traverse_tuple
# Parametric equations
for l, layer in enumerate(turns):
    for t in traverse_tuple(layer):
        print(t)
        c_l = c+l*c*2


        # Perimeter of the coil's path in xy-plane
        P = 2 * H + 2 * W + 2 * np.pi * c_l

        # Transition points in t (for one turn, t in [0, 2pi])
        t1 = 2 * np.pi * W / P
        t2 = 2 * np.pi * (W + np.pi * c_l / 2) / P
        t3 = 2 * np.pi * (W + H + np.pi * c_l / 2) / P
        t4 = 2 * np.pi * (W + H + np.pi * c_l) / P
        t5 = 2 * np.pi * (2 * W + H + np.pi * c_l) / P
        t6 = 2 * np.pi * (2 * W + H + 3 * np.pi * c_l / 2) / P
        t7 = 2 * np.pi * (2 * W + 2 * H + 3 * np.pi * c_l / 2) / P
        t8 = 2 * np.pi

        if l==0:
            t_lin = [0, t1]
        else:
            t_lin = [t1]
        t_lin.extend(np.linspace(t1, t2, 12))
        t_lin.extend([t2, t3])
        t_lin.extend(np.linspace(t3, t4, 12))
        t_lin.extend([t4, t5])
        t_lin.extend(np.linspace(t5, t6, 12))
        t_lin.extend([t6, t6])
        t_lin.extend(np.linspace(t7, t8, 12))

        for t_mod in t_lin:
            if 0 <= t_mod < t1:
                # Right side
                x_coords.append(H / 2 + c_l)
                y_coords.append(W / 2 - P * t_mod / (2 * np.pi))
            elif t1 <= t_mod < t2:
                # Bottom-right corner
                theta = -(P * t_mod - 2 * np.pi * W) / (2 * np.pi * c_l)
                x_coords.append(H / 2 + c_l * np.cos(theta))
                y_coords.append(-W / 2 + c_l * np.sin(theta))
            elif t2 <= t_mod < t3:
                # Bottom side
                x_coords.append(H / 2 - (P * t_mod / (2 * np.pi) - (W + np.pi * c_l / 2)))
                y_coords.append(-(W / 2 + c_l))
            elif t3 <= t_mod < t4:
                # Bottom-left corner
                theta = -np.pi / 2 - (P * t_mod - 2 * np.pi * (W + H + np.pi * c_l / 2)) / (2 * np.pi * c_l)
                x_coords.append(-H / 2 + c_l * np.cos(theta))
                y_coords.append(-W / 2 + c_l * np.sin(theta))
            elif t4 <= t_mod < t5:
                # Left side
                x_coords.append(-(H / 2 + c_l))
                y_coords.append(-W / 2 + (P * t_mod / (2 * np.pi) - (W + H + np.pi * c_l)))
            elif t5 <= t_mod < t6:
                # Top-left corner
                theta = -np.pi - (P * t_mod - 2 * np.pi * (2 * W + H + np.pi * c_l)) / (2 * np.pi * c_l)
                x_coords.append(-H / 2 + c_l * np.cos(theta))
                y_coords.append(W / 2 + c_l * np.sin(theta))
            elif t6 <= t_mod < t7:
                # Top side
                x_coords.append(-H / 2 + (P * t_mod / (2 * np.pi) - (2 * W + H + 3 * np.pi * c_l / 2)))
                y_coords.append(W / 2 + c_l)
            else:  # t7 <= t_mod < t8
                # Top-right corner
                theta = -3 * np.pi / 2 - (P * t_mod - 2 * np.pi * (2 * W + 2 * H + 3 * np.pi * c_l / 2)) / (2 * np.pi * c_l)
                x_coords.append(H / 2 + c_l * np.cos(theta))
                y_coords.append(W / 2 + c_l * np.sin(theta))
            if l%2==0:
                z_coords.append(p * t_mod / (2 * np.pi) + t*p)
            else:  # reverse
                z_coords.append(p * (2*np.pi - t_mod) / (2 * np.pi) + t*p)

# Add points to VTK
for i in range(len(z_coords)):
    points.InsertNextPoint(x_coords[i], y_coords[i], z_coords[i])

# Create polyline
polyline = vtk.vtkPolyLine()
polyline.GetPointIds().SetNumberOfIds(len(z_coords))
for i in range(len(z_coords)):
    polyline.GetPointIds().SetId(i, i)

# Create cells
cells = vtk.vtkCellArray()
cells.InsertNextCell(polyline)

# Create polydata
polydata = vtk.vtkPolyData()
polydata.SetPoints(points)
polydata.SetLines(cells)

# Mapper for coil
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(polydata)

# Actor for coil
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1, 0, 0)  # Red coil
actor.GetProperty().SetLineWidth(2)

# Create prism for reference (wireframe)
cube = vtk.vtkCubeSource()
cube.SetXLength(H)
cube.SetYLength(W)
cube.SetZLength(D)
cube.Update()

prism_mapper = vtk.vtkPolyDataMapper()
prism_mapper.SetInputConnection(cube.GetOutputPort())

prism_actor = vtk.vtkActor()
prism_actor.SetMapper(prism_mapper)
prism_actor.GetProperty().SetColor(0, 0, 1)  # Blue prism
prism_actor.GetProperty().SetRepresentationToWireframe()

# Renderer
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(prism_actor)
renderer.SetBackground(0.9, 0.9, 0.9)  # Dark background

# Render window
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 600)

# Interactor
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Initialize and start
interactor.Initialize()
render_window.Render()
interactor.Start()