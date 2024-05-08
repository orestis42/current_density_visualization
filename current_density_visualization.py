import numpy as np
import plotly.graph_objs as go

class CurrentDensityField:
    """A class to represent and visualize a 3D current density field based on given parameters and equations for current density."""
    def create_grid(self):
        """Creates a 3D grid based on initialized parameters."""
        x = np.linspace(*self.x_range, self.x_points)
        y = np.linspace(*self.y_range, self.y_points)
        z = np.linspace(*self.z_range, self.z_points)
        self.X, self.Y, self.Z = np.meshgrid(x, y, z, indexing='ij')

    def __init__(self, A, b, h, x_range, y_range, z_range, x_points, y_points, z_points):
        """Initializes the current density field parameters."""
        self.A = A
        self.b = b
        self.h = h
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range
        self.x_points = x_points
        self.y_points = y_points
        self.z_points = z_points
        self.create_grid()

    def current_density(self, x, y):
        """Calculate the current density vectors J and K at all points in the grid."""
        if 0 < y <= self.h and x > 0:
            j_x = self.A * (1 - np.exp(-self.b * x))
            j_y = self.A * self.b * (self.h - y) * np.exp(-self.b * x)
            j_z = 0
            return [j_x, j_y, j_z]
        elif y == 0 and x > 0:
            k_x = -self.A * self.h * (1 - np.exp(-self.b * x))
            k_y = 0
            k_z = 0
            return [k_x, k_y, k_z]
        else:
            return [0, 0, 0]

    def evaluate_currents(self):
        """Evaluate the current density field at all points in the grid."""
        self.J = np.zeros((self.x_points, self.y_points, self.z_points, 3))
        self.K = np.zeros((self.x_points, self.y_points, self.z_points, 3))
        for i in range(self.x_points):
            for j in range(self.y_points):
                for k in range(self.z_points):
                    if self.Y[i, j, k] == 0 and self.X[i, j, k] > 0:
                        self.K[i, j, k] = self.current_density(self.X[i, j, k], self.Y[i, j, k])
                    else:
                        self.J[i, j, k] = self.current_density(self.X[i, j, k], self.Y[i, j, k])

    def visualize_current_density(self, component_indices):
        """Visualize the specified components of the current density."""
        quiver_data = {
            "x": [], "y": [], "z": [],
            "u": [], "v": [], "w": []
        }
        for i in range(self.x_points):
            for j in range(self.y_points):
                for k in range(self.z_points):
                    if self.Y[i, j, k] > 0 or self.X[i, j, k] <= 0:
                        current = self.J[i, j, k]
                        quiver_data["x"].append(self.X[i, j, k])
                        quiver_data["y"].append(self.Y[i, j, k])
                        quiver_data["z"].append(self.Z[i, j, k])
                        quiver_data["u"].append(current[0] if component_indices[0] else 0)
                        quiver_data["v"].append(current[1] if component_indices[1] else 0)
                        quiver_data["w"].append(current[2] if component_indices[2] else 0)
        return quiver_data

    def visualize_surface_current(self):
        """Visualize the surface current."""
        surface_data = {
            "x": [], "y": [], "z": [],
            "u": [], "v": [], "w": []
        }
        for i in range(self.x_points):
            for j in range(self.y_points):
                for k in range(self.z_points):
                    if self.Y[i, j, k] == 0 and self.X[i, j, k] > 0:
                        current = self.K[i, j, k]
                        surface_data["x"].append(self.X[i, j, k])
                        surface_data["y"].append(self.Y[i, j, k])
                        surface_data["z"].append(self.Z[i, j, k])
                        surface_data["u"].append(current[0])
                        surface_data["v"].append(current[1])
                        surface_data["w"].append(current[2])
        return surface_data

    def visualize(self, show_jx=True, show_jy=True, show_jz=True, camera_settings=None):
        """Visualize the current density field with Plotly and optional camera settings."""
        surface_data = self.visualize_surface_current()
        quiver_data = self.visualize_current_density([show_jx, show_jy, show_jz])

        # Create 3D quiver plots for both surface and current density
        surface_vectors = go.Cone(
            x=surface_data["x"], y=surface_data["y"], z=surface_data["z"],
            u=surface_data["u"], v=surface_data["v"], w=surface_data["w"],
            colorscale='Reds', sizemode='absolute', sizeref=0.75
        )

        current_density_vectors = go.Cone(
            x=quiver_data["x"], y=quiver_data["y"], z=quiver_data["z"],
            u=quiver_data["u"], v=quiver_data["v"], w=quiver_data["w"],
            colorscale='Blues', sizemode='absolute', sizeref=0.75
        )

        # Add XYZ axes lines crossing at the origin
        axis_lines = [
            go.Scatter3d(
                x=[0, self.x_range[1]],
                y=[0, 0],
                z=[0, 0],
                mode='lines',
                line=dict(color='red', width=5),
                name='X Axis'
            ),
            go.Scatter3d(
                x=[0, 0],
                y=[0, self.y_range[1]],
                z=[0, 0],
                mode='lines',
                line=dict(color='green', width=5),
                name='Y Axis'
            ),
            go.Scatter3d(
                x=[0, 0],
                y=[0, 0],
                z=[0, self.z_range[1]],
                mode='lines',
                line=dict(color='blue', width=5),
                name='Z Axis'
            )
        ]

        layout = go.Layout(
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z',
                camera=camera_settings if camera_settings else dict()
            ),
            title="3D Current Density Field"
        )

        fig = go.Figure(data=[surface_vectors, current_density_vectors] + axis_lines, layout=layout)
        fig.show()

def parse_or_default(input_str, default_values):
    """Parse user input into a tuple of two values or return default values."""
    try:
        values = tuple(map(float, input_str.split()))
        if len(values) != 2:
            raise ValueError("Invalid number of values.")
        return values
    except ValueError:
        return default_values

def main():
    """Main function to gather user input and visualize the current density field."""
    try:
        A = float(input("Enter A (default=1.0): ") or 1.0)
        b = float(input("Enter b (default=0.3): ") or 0.3)
        h = float(input("Enter h (default=2.0): ") or 2.0)
        x_range = parse_or_default(input("Enter x_range as two values (default=-1, 4): "), (-1, 4))
        y_range = parse_or_default(input("Enter y_range as two values (default=-1, 4): "), (-1, 4))
        z_range = parse_or_default(input("Enter z_range as two values (default=-2.5, 2.5): "), (-2.5, 2.5))
        x_points = int(input("Enter number of x_points (default=16): ") or 16)
        y_points = int(input("Enter number of y_points (default=16): ") or 16)
        z_points = int(input("Enter number of z_points (default=16): ") or 16)
    except ValueError as e:
        print(f"Invalid input provided: {e}. Using default values.")
        A, b, h = 1.0, 0.3, 2.0
        x_range, y_range, z_range = (-1, 4), (-1, 4), (-2.5, 2.5)
        x_points, y_points, z_points = 16, 16, 16

    # Prompt for component selection
    show_jx = input("Visualize J_x component? (y/n, default=y): ").lower() != 'n'
    show_jy = input("Visualize J_y component? (y/n, default=y): ").lower() != 'n'
    show_jz = input("Visualize J_z component? (y/n, default=y): ").lower() != 'n'

    # Prompt for camera plane selection
    plane = input("Choose initial plane (xy/xz/yz, default=xy): ").lower() or 'xy'
    camera_settings = {
        'xy': dict(eye=dict(x=1.25, y=1.25, z=1.25)),
        'xz': dict(eye=dict(x=2, y=0, z=1.5)),
        'yz': dict(eye=dict(x=0, y=1.5, z=2)),
    }.get(plane, dict(eye=dict(x=1.25, y=1.25, z=1.25)))

    # Create and visualize the field
    field = CurrentDensityField(A, b, h, x_range, y_range, z_range, x_points, y_points, z_points)
    field.evaluate_currents()
    field.visualize(show_jx, show_jy, show_jz, camera_settings)

if __name__ == "__main__":
    main()
