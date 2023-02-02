from math import pow as m_pow
from math import sqrt

from path import Path
from constants import *

class Particle:
    def __init__(self, img_path, mass):
        self.path = Path(img_path)          # Information about the particle's path
        self.mass = mass                    # Particle mass in MeV/c^2
        self.momentum = 0                   # Particle momentum in MeV/c
        self.energy = 0                     # Particle energy in MeV

        R = self.path.curvature_radius
        self.momentum = LIGHT_SPEED * R * B_FIELD * m_pow(10, 3)
        
        p = self.momentum
        m = self.mass
        self.energy = sqrt(m_pow(p, 2) + m_pow(m, 2))
