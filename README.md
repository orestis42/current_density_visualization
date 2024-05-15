# Exercise in Current Density Visualization

## Overview
A 3D visualization of a uniform arrangement along the z-axis containing the following electric current distributions:

- In the region of space where $x > 0$ and $0 < y < h$, the spatial distribution with density:
  $$\mathbf{J} = A \left[ \left( 1 - e^{-bx} \right) \hat{x} + b(h - y)e^{-bx}\right] \hat{y}$$

- In the section of the plane $y = 0$ where $x > 0$, the surface distribution with density:
  $$\mathbf{K} = -Ah \left( 1 - e^{-bx} \right) \hat{x}$$

where $A$, $b$, and $h$ are known positive constants. The entire space has magnetic permeability $\mu_0$, while the regions where $x < 0$, $y < 0$, or $y > h$ are non-conductive.

## Installation

To install the necessary dependencies, use [`pipenv`](https://github.com/pypa/pipenv?tab=readme-ov-file#installation). It is recommended to use a virtual environment to manage your dependencies.

Clone the repository.

```bash
git clone https://github.com/orestis42/current_density_visualization.git
```

Navigate to the project directory.
```bash
cd current_density_visualization
```

Install dependencies using pipenv.
```bash
pipenv install
```

## Usage

```bash
pipenv run python current_density_visualization.py
```
