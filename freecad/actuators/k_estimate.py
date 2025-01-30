import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# Given data from here: https://roymech.org/Useful_Tables/Drive/Gears.html?
no_teeth = np.array([12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 43, 45, 50, 55, 60, 65, 70, 75, 80, 90, 100, 150, 200, 300])
pressure_angle = np.array([14.5] * len(no_teeth) + [20] * len(no_teeth) + [25] * len(no_teeth))
values = np.array([
    0.355, 0.377, 0.399, 0.415, 0.43, 0.446, 0.459, 0.471, 0.481, 0.49, 0.496, 0.502, 0.509, 0.515, 0.522,
    0.528, 0.534, 0.537, 0.54, 0.554, 0.547, 0.55, 0.553, 0.556, 0.559, 0.563, 0.565, 0.568, 0.57, 0.574,
    0.579, 0.588, 0.596, 0.603, 0.607, 0.61, 0.613, 0.615, 0.619, 0.622, 0.635, 0.64, 0.65,
    0.415, 0.443, 0.468, 0.49, 0.503, 0.512, 0.522, 0.534, 0.544, 0.553, 0.559, 0.565, 0.572, 0.58, 0.584,
    0.588, 0.592, 0.599, 0.606, 0.611, 0.617, 0.623, 0.628, 0.633, 0.639, 0.645, 0.65, 0.655, 0.659, 0.668,
    0.678, 0.694, 0.704, 0.713, 0.721, 0.728, 0.735, 0.739, 0.747, 0.755, 0.778, 0.787, 0.801,
    0.4701462585, 0.4879849504, 0.5220922992, 0.5430802909, 0.5723331339, 0.5818564118, 0.5947428571, 0.6140295477,
    0.6274303887, 0.6398203876, 0.6486714819, 0.6620045045, 0.6768544029, 0.6927425265, 0.6921212625,
    0.6928031933, 0.6934707585, 0.7052932163, 0.7171287024, 0.7094765755, 0.7323554706, 0.7401381236,
    0.7432153192, 0.7503516574, 0.7541111962, 0.75821563, 0.7633014264, 0.7710100379, 0.7731280297,
    0.7758191153, 0.79351977, 0.8121110167, 0.8226012048, 0.8290936871, 0.8419155833, 0.8514469697,
    0.8586102627, 0.8631079309, 0.8714381722, 0.8833205059, 0.9150730131, 0.9300132561, 0.9366741535,
])

def math_func(x, y, a, b, c):
    return a+(np.sin((b+y)/180*np.pi))*np.log1p(c*x)

# Define exponential function
def exp_func(data, a, b, c):
    x, y = data
    return math_func(x, y, a, b, c)

# Fit the function
popt, _ = opt.curve_fit(exp_func, (np.tile(no_teeth, 3), pressure_angle), values, p0=(0.5, 0.01, 0.01))

# Extract estimated parameters
a_est, b_est, c_est = popt
print(a_est, b_est, c_est)
#safety=0.08
print(f"f(num_teeth,pressure_angle)={a_est}*({b_est}/num_teeth+e^({c_est}*pressure_angle))")

# Create a 3D plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot the data points
x_data, y_data = np.tile(no_teeth, 3), pressure_angle
ax.scatter(x_data, y_data, values, color='red', label='Data Points')

# Create grid for surface plot
X, Y = np.meshgrid(np.linspace(no_teeth.min(), no_teeth.max(), 100),
                   np.linspace(pressure_angle.min(), pressure_angle.max(), 100))
#Z = a_est * np.exp(b_est * X + c_est * Y)
Z = math_func(X, Y, a_est, b_est, c_est)

# Plot the fitted surface
surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)

# Labels and title
ax.set_xlabel('Number of Teeth')
ax.set_ylabel('Pressure angle')
ax.set_zlabel('Middle Teeth Load')
ax.set_title('3D Plot of Exponential Function Fit')

# Add a color bar which maps values to colors
fig.colorbar(surf, shrink=0.5, aspect=5)

# Add legend
ax.legend()

# Show the plot
plt.show()