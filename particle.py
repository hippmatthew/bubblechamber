import numpy as np
from math import pow as mpow
from path import Path

class Particle:
    def __init__(self, img_path, mass):
        __g = 0.036221                      # Magnification factor: 559 px -> mm / 175 mm
        __B = 1.5                           # B-Field magnitude in T (B-Field out of page in all images)
        
        self.path = Path(img_path)          # Information about the particle's path
        self.mass = mass                    # Particle mass in MeV/c^2
        self.momentum = 0                   # Particle momentum in MeV/c
        self.energy = 0                     # Particle energy in MeV

        R = self.path.curvature_radius
        self.momentum = 300 * __g * R / 1000 * __B
        
        p = self.momentum
        m = self.mass
        self.energy = np.sqrt(mpow(p, 2) + mpow(m, 2))

    def __str__(self):
        return f'''mass:\t\t{self.mass} MeV/c^2
momentum:\t{self.momentum} MeV/c
energy:\t\t{self.energy} MeV

--- path info ---
init_dir:\t{self.path.trajectory.direction}
base_dir:\t{self.path.base_direction}
arc_len:\t{self.path.arc_length} mm
saggita:\t{self.path.saggita} mm
curv_rad:\t{self.path.curvature_radius} mm'''
