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

    def current_density(self, x, y):
        """
        Calculate the current density vectors J and K at all the points of the grid.
        J is defined within the volume confined by y=0 and y=h for x>0.
        K is defined within the surface y=0 for x>0.
        """
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
        for i in range(self.x_points):
            for j in range(self.y_points):
                for k in range(self.z_points):
                    self.J[i, j, k] = self.current_density(self.X[i, j, k], self.Y[i, j, k])

    def visualize(self):
        """Visualize the current density field."""
        fig = plt.figure(figsize=(15, 10))
        ax = fig.add_subplot(111, projection='3d')
        for i in range(self.x_points):
            for j in range(self.y_points):
                for k in range(self.z_points):
                    if self.Y[i, j, k] == 0:
                        color = 'red'
                    else:
                        color = 'blue'
                    ax.quiver(self.X[i, j, k], self.Y[i, j, k], self.Z[i, j, k], self.J[i, j, k, 0], self.J[i, j, k, 1], self.J[i, j, k, 2], length=0.3, color=color)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()

if __name__ == "__main__":
    field = CurrentDensityField(A=1.0, b=0.3, h=2.0,
                            x_range=(-1, 4), y_range=(-1, 4), z_range=(-2.5, 2.5),
                            x_points=11, y_points=11, z_points=11)
    field.evaluate_currents()
    field.visualize()
