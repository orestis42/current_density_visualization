import numpy as np
import plotly.graph_objects as go

# Constants
A = 1
b = 0.3
h = 1

def compute_spatial_current_density(x, y):
    """Calculate the spatial current density at a given (x, y)."""
    if 0 < y <= h and x > 0:
        j_x = A * (1 - np.exp(-b * x))
        j_y = A * b * (h - y) * np.exp(-b * x)
        j_z = 0
        return np.array([j_x, j_y, j_z])
    else:
        return np.zeros(3)


def compute_surface_current_density(x, y):
    """Calculate the surface current density at a given (x, y)."""
    if y == 0 and x > 0:
        k_x = -A * h * (1 - np.exp(-b * x))
        k_y = 0
        k_z = 0
        return np.array([k_x, k_y, k_z])
    else:
        return np.zeros(3)


def generate_cone_plot(data, color, name):
    """Generate a plotly cone plot for a set of vector data."""
    x, y, z, u, v, w = data
    return go.Cone(
        x=x, y=y, z=z, u=u, v=v, w=w,
        colorscale=color,
        showscale=False,
        name=name
    )


def visualize_current_densities():
    """Generate a visualization for the spatial and surface current densities."""
    # Grid resolution and limits
    x_values = np.linspace(0, 10, 10)
    y_values = np.linspace(0, h, 10)
    z_values = np.linspace(-3, 3, 7)

    # Collect all current vectors
    spatial_data = [[], [], [], [], [], []]  # x, y, z, u, v, w
    surface_data = [[], [], [], [], [], []]  # x, y, z, u, v, w

    # Compute spatial current density vectors for all z-values
    for x in x_values:
        for y in y_values:
            j_vec = compute_spatial_current_density(x, y)
            for z in z_values:
                spatial_data[0].append(x)
                spatial_data[1].append(y)
                spatial_data[2].append(z)
                spatial_data[3].append(j_vec[0])
                spatial_data[4].append(j_vec[1])
                spatial_data[5].append(j_vec[2])

    # Compute surface current density vectors for all z-values
    for x in x_values:
        k_vec = compute_surface_current_density(x, 0)
        for z in z_values:
            surface_data[0].append(x)
            surface_data[1].append(0)
            surface_data[2].append(z)
            surface_data[3].append(k_vec[0])
            surface_data[4].append(k_vec[1])
            surface_data[5].append(k_vec[2])

    # Create cone plots
    spatial_cones = generate_cone_plot(spatial_data, "Blues", "Spatial Current Density")
    surface_cones = generate_cone_plot(surface_data, "Reds", "Surface Current Density")

    # Combine plots in a single figure
    fig = go.Figure(data=[spatial_cones, surface_cones])
    fig.update_layout(
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z',
            aspectmode='cube'
        ),
        title="Spatial and Surface Current Densities"
    )
    fig.show()


if __name__ == "__main__":
    visualize_current_densities()

