import numpy as np
import plotly.graph_objects as go

# Constants
A = 1
B = 0.3
H = 1

def compute_spatial_current_density(x, y):
    """
    Calculate the spatial current density at a given (x, y).
    Vectorized to handle arrays efficiently.
    """
    mask = (0 < y) & (y <= H) & (x > 0)
    j_x = A * (1 - np.exp(-B * x)) * mask
    j_y = A * B * (H - y) * np.exp(-B * x) * mask
    j_z = np.zeros_like(j_x)
    return np.stack([j_x, j_y, j_z], axis=-1)

def compute_surface_current_density(x):
    """
    Calculate the surface current density at a given x.
    Vectorized to handle arrays efficiently.
    """
    k_x = np.zeros_like(x)
    mask = x > 0
    k_x[mask] = -A * H * (1 - np.exp(-B * x[mask]))
    k_y = np.zeros_like(k_x)
    k_z = np.zeros_like(k_x)
    return np.stack([k_x, k_y, k_z], axis=-1)

def generate_cone_plot(x, y, z, u, v, w, color, name):
    """
    Generate a Plotly cone plot for a set of vector data.
    Declarative approach to visualize vector fields.
    """
    return go.Cone(x=x, y=y, z=z, u=u, v=v, w=w, colorscale=color, showscale=False, name=name)

def create_meshgrid(x_values, y_values=None, z_values=None):
    """
    Create a meshgrid for given x, y, and z values.
    """
    if y_values is not None and z_values is not None:
        return np.meshgrid(x_values, y_values, z_values)
    elif z_values is not None:
        return np.meshgrid(x_values, z_values)
    else:
        return np.meshgrid(x_values)

def prepare_spatial_data(x_values, y_values, z_values):
    """
    Prepare data for spatial current density plot.
    """
    X, Y, Z = create_meshgrid(x_values, y_values, z_values)
    J = compute_spatial_current_density(X, Y)
    return [X.ravel(), Y.ravel(), Z.ravel(), J[..., 0].ravel(), J[..., 1].ravel(), J[..., 2].ravel()]

def prepare_surface_data(x_values, z_values):
    """
    Prepare data for surface current density plot.
    """
    X_surface, Z_surface = create_meshgrid(x_values, z_values=z_values)
    Y_surface = np.zeros_like(X_surface)
    K = compute_surface_current_density(x_values)
    return [X_surface.ravel(), Y_surface.ravel(), Z_surface.ravel(),
            np.tile(K[..., 0], Z_surface.shape[0]),
            np.tile(K[..., 1], Z_surface.shape[0]),
            np.tile(K[..., 2], Z_surface.shape[0])]

def create_camera_orientation():
    """
    Create a default camera orientation for the 3D plot.
    """
    return dict(
        up=dict(x=0, y=1, z=0),
        center=dict(x=0, y=0, z=0),
        eye=dict(x=0, y=0, z=2)
    )

def create_plot(spatial_data, surface_data):
    """
    Create a Plotly plot combining spatial and surface current densities.
    """
    spatial_cones = generate_cone_plot(*spatial_data, "Blues", "Spatial Current Density")
    surface_cones = generate_cone_plot(*surface_data, "Reds", "Surface Current Density")

    camera = create_camera_orientation()

    fig = go.Figure(data=[spatial_cones, surface_cones])
    fig.update_layout(
        scene=dict(
            xaxis=dict(
                title='X',
                zeroline=True,
                zerolinecolor='red',
                showline=True,
                showgrid=True
            ),
            yaxis=dict(
                title='Y',
                zeroline=True,
                zerolinecolor='green',
                showline=True,
                showgrid=True
            ),
            zaxis=dict(
                title='Z',
                zeroline=True,
                zerolinecolor='blue',
                showline=True,
                showgrid=True
            ),
            aspectmode='cube',
            camera=camera
        ),
        title="Spatial and Surface Current Densities",
        template="plotly_dark"
    )
    fig.show()

def visualize_current_densities():
    """
    Generate a visualization for the spatial and surface current densities.
    Uses vectorized computations and Plotly for professional visualization.
    """
    x_values = np.linspace(0.1, 10, 10)
    y_values = np.linspace(0, H, 10)
    z_values = np.linspace(-3, 3, 7)

    spatial_data = prepare_spatial_data(x_values, y_values, z_values)
    surface_data = prepare_surface_data(x_values, z_values)

    create_plot(spatial_data, surface_data)

if __name__ == "__main__":
    visualize_current_densities()

