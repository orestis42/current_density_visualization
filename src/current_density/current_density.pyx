import numpy as np
cimport numpy as np

def compute_spatial_current_density(np.ndarray[double, ndim=2] x, np.ndarray[double, ndim=2] y, double A, double B, double H):
    cdef np.ndarray[double, ndim=2] j_x = np.zeros_like(x, dtype=np.float64)
    cdef np.ndarray[double, ndim=2] j_y = np.zeros_like(x, dtype=np.float64)
    cdef np.ndarray[double, ndim=2] j_z = np.zeros_like(x, dtype=np.float64)
    cdef np.ndarray[char, ndim=2] mask = (0 < y) & (y <= H) & (x > 0)

    j_x[mask] = A * (1 - np.exp(-B * x[mask]))
    j_y[mask] = A * B * (H - y[mask]) * np.exp(-B * x[mask])

    return np.stack([j_x, j_y, j_z], axis=-1)

def compute_surface_current_density(np.ndarray[double, ndim=1] x, double A, double B, double H):
    cdef np.ndarray[double, ndim=1] k_x = np.zeros_like(x, dtype=np.float64)
    cdef np.ndarray[double, ndim=1] k_y = np.zeros_like(x, dtype=np.float64)
    cdef np.ndarray[double, ndim=1] k_z = np.zeros_like(x, dtype=np.float64)
    cdef np.ndarray[char, ndim=1] mask = x > 0

    k_x[mask] = -A * H * (1 - np.exp(-B * x[mask]))

    return np.stack([k_x, k_y, k_z], axis=-1)
