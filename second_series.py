import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class CurrentDensityField:
    """
    A class to represent and visualize a 3D current density field based on given parameters and equations for current density.
    """

    def create_grid(self):
        """Creates a 3D grid based on initialized parameters."""
        x = np.linspace(*self.x_range, self.x_points)
        y = np.linspace(*self.y_range, self.y_points)
        z = np.linspace(*self.z_range, self.z_points)
        self.X, self.Y, self.Z = np.meshgrid(x, y, z, indexing='ij')

    def __init__(self, A, b, h, x_range, y_range, z_range, x_points, y_points, z_points):
        """
        Initializes the current density field parameters.
        """
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

    def spatial_current_density(self, x, y):
        """
        Calculate the current density vector J at a point (x, y, z).
        J is defined within the volume confined by y=0 and y=h for x>0.
        """
        if 0 <= y <= self.h and x > 0:
            j_x = self.A * (1 - np.exp(-self.b * x))
            j_y = self.A*self.b * (self.h - y) * np.exp(-self.b * x)
            return np.array([j_x, j_y, 0])
        else:
            return np.array([0, 0, 0])
    
    def evaluate_currents(self):
        """Evaluate the current density field at all points in the grid."""
        self.J = np.zeros((self.x_points, self.y_points, self.z_points, 3))
        for i in range(self.x_points):
            for j in range(self.y_points):
                for k in range(self.z_points):
                    self.J[i, j, k] = self.spatial_current_density(self.X[i, j, k], self.Y[i, j, k])

    def visualize(self):
        """Visualize the current density field."""
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.quiver(self.X, self.Y, self.Z, self.J[..., 0], self.J[..., 1], self.J[..., 2], length=0.3)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()

# Example of using the class
if __name__ == "__main__":
    field = CurrentDensityField(A=1.0, b=0.3, h=2.0,
                            x_range=(0, 3), y_range=(-3, 3), z_range=(-3, 3),
                            x_points=15, y_points=15, z_points=15)
    field.evaluate_currents()
    field.visualize()
