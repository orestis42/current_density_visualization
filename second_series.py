import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class CurrentDensityField:
    """
    A class to represent and visualize a 3D current density field.
    """
    def __init__(self, A, b, h, x_max, x_points, y_points, z_layer):
        """
        Initializes the current density field parameters.
        
        Parameters:
            A (float): Amplitude of the current density.
            b (float): Exponential decay factor.
            h (float): Height of the y-dimension.
            x_max (float): Maximum value of x to evaluate.
            x_points (int): Number of points in the x-axis grid.
            y_points (int): Number of points in the y-axis grid.
            z_layer (float): Single layer depth in the z-axis for visualization.
        """
        self.A = A
        self.b = b
        self.h = h
        self.x_max = x_max
        self.x_points = x_points
        self.y_points = y_points
        self.z_layer = z_layer
        self.create_grid()

    def create_grid(self):
        """Creates a 3D grid based on initialized parameters."""
        x_range = np.linspace(0.1, self.x_max, self.x_points)
        y_range = np.linspace(0, self.h, self.y_points)
        z_range = np.array([self.z_layer])  
        self.X, self.Y, self.Z = np.meshgrid(x_range, y_range, z_range, indexing='ij')

    def spatial_current_density(self, x, y):
        """
        Calculate the current density vector J at a point (x, y).
        
        Parameters:
            x (float): x-coordinate.
            y (float): y-coordinate.
        
        Returns:
            np.array: Current density vector (Jx, Jy, Jz).
        """
        if x > 0 and 0 <= y <= self.h:
            j_x = self.A * (1 - np.exp(-self.b * x))
            j_y = self.b * (self.h - y) * np.exp(-self.b * x)
            return np.array([j_x, j_y, 0])
        else:
            return np.array([0, 0, 0])

    def evaluate_currents(self):
        """Evaluate the current density vectors over the grid."""
        vectorized_J = np.vectorize(self.spatial_current_density, signature='(),()->(3)')
        V = vectorized_J(self.X, self.Y)
        self.Vx, self.Vy, self.Vz = V[..., 0], V[..., 1], V[..., 2]

    def visualize(self):
        """Visualize the current density field in 3D."""
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.quiver(self.X, self.Y, self.Z, self.Vx, self.Vy, self.Vz, length=0.1, color='b', normalize=True)
        ax.set_xlim([0, self.x_max])
        ax.set_ylim([0, self.h])
        ax.set_zlim([-0.1, 0.1])
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.title('3D Vector Field of Current Density')
        plt.show()

# Example of using the class
if __name__ == "__main__":
    field = CurrentDensityField(A=1.0, b=1.0, h=1.0, x_max=2, x_points=10, y_points=5, z_layer=0)
    field.evaluate_currents()
    field.visualize()
