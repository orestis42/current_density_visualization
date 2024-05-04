# Current Density Field Visualizer

## Overview
This Python module provides a class `CurrentDensityField` which models and visualizes a 3D current density field. It is particularly useful for visualizing current densities within specific volumes and surfaces based on user-defined parameters.

## Features
- Definition of current density in a volumetric space and on a surface.
- Visualization of current density components using matplotlib and mpl_toolkits for 3D plotting.
- Customizable grid and current density calculation based on input parameters.

## Requirements
- numpy
- matplotlib
- mpl_toolkits.mplot3d

## Usage
To use this module, instantiate the `CurrentDensityField` class with the required physical and grid parameters. Then, call the `evaluate_currents` method to calculate the current densities across the grid. Finally, use the `visualize` method to generate a 3D visualization of the current density vectors.

### Example
```python
from current_density_field import CurrentDensityField

# Initialize the field with specific parameters
field = CurrentDensityField(A=1.0, b=0.3, h=2.0,
                            x_range=(-1, 4), y_range=(-1, 4), z_range=(-2.5, 2.5),
                            x_points=11, y_points=11, z_points=11)

# Calculate current densities
field.evaluate_currents()

# Visualize the current density field
field.visualize(show_jx=True, show_jy=True, show_jz=True, elevation=-90, azimuth=90)
