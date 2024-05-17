import numpy as np
import plotly.graph_objects as go
import current_density

# Constants
A = 1
B = 0.3
H = 1

def generate_cone_plot(x, y, z, u, v, w, color, name):
    return go.Cone(x=x, y=y, z=z, u=u, v=v, w=w, colorscale=color, showscale=False, name=name)

def create_meshgrid(x_values, y_values=None, z_values=None):
    if y_values is not None and z_values is not None:
        return np.meshgrid(x_values, y_values, z_values, indexing='ij')
    elif y_values is not None:
        return np.meshgrid(x_values, y_values, indexing='ij')
    elif z_values is not None:
        return np.meshgrid(x_values, z_values, indexing='ij')
    else:
        return np.meshgrid(x_values, indexing='ij')

def prepare_spatial_data(x_values, y_values, z_values):
    """
    Prepare data for spatial current density plot.
    """
    X, Y, Z = create_meshgrid(x_values, y_values, z_values)
    J = current_density.compute_spatial_current_density(X[:, :, 0], Y[:, :, 0], A, B, H)
    J_tiled = np.repeat(J[:, :, np.newaxis, :], Z.shape[2], axis=2)
    return [X.ravel(), Y.ravel(), Z.ravel(), J_tiled[..., 0].ravel(), J_tiled[..., 1].ravel(), J_tiled[..., 2].ravel()]


def prepare_surface_data(x_values, z_values):
    X_surface, Z_surface = create_meshgrid(x_values, z_values=z_values)
    Y_surface = np.zeros_like(X_surface)
    K = current_density.compute_surface_current_density(x_values, A, B, H)
    tiled_K_x = np.repeat(K[:, 0], Z_surface.shape[1])
    tiled_K_y = np.repeat(K[:, 1], Z_surface.shape[1])
    tiled_K_z = np.repeat(K[:, 2], Z_surface.shape[1])
    return [X_surface.ravel(), Y_surface.ravel(), Z_surface.ravel(), tiled_K_x, tiled_K_y, tiled_K_z]

def create_camera_orientation():
    return dict(up=dict(x=0, y=1, z=0), center=dict(x=0, y=0, z=0), eye=dict(x=0, y=0, z=2))

def create_plot(spatial_data, surface_data):
    spatial_cones = generate_cone_plot(*spatial_data, "Blues", "Spatial Current Density")
    surface_cones = generate_cone_plot(*surface_data, "Reds", "Surface Current Density")
    camera = create_camera_orientation()
    fig = go.Figure(data=[spatial_cones, surface_cones])
    fig.update_layout(
        scene=dict(
            xaxis=dict(title='X', zeroline=True, zerolinecolor='red', showline=True, showgrid=True),
            yaxis=dict(title='Y', zeroline=True, zerolinecolor='green', showline=True, showgrid=True),
            zaxis=dict(title='Z', zeroline=True, zerolinecolor='blue', showline=True, showgrid=True),
            aspectmode='cube',
            camera=camera
        ),
        title="Spatial and Surface Current Densities",
        template="plotly_dark"
    )
    fig.show()

def visualize_current_densities():
    x_values = np.linspace(0.1, 10, 10)
    y_values = np.linspace(0, H, 10)
    z_values = np.linspace(-3, 3, 7)
    spatial_data = prepare_spatial_data(x_values, y_values, z_values)
    surface_data = prepare_surface_data(x_values, z_values)
    create_plot(spatial_data, surface_data)

if __name__ == "__main__":
    visualize_current_densities()

