from setuptools import setup, find_packages
from Cython.Build import cythonize
import numpy

setup(
    name='CurrentDensityProject',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    ext_modules=cythonize("src/current_density/current_density.pyx"),
    include_dirs=[numpy.get_include()],
    entry_points={
        'console_scripts': [
            'visualize=current_density.current_density_visualization:visualize_current_densities',
        ],
    },
)

