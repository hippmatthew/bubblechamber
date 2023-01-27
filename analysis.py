import numpy as np
from math import pow as mpow
import time
from particle import Particle
from path import Trajectory
from linear_algebra import get_angle

__EXP_VALUE_K0 = 497.611    # Accepted mass of 0_Kaon in MeV/c^2
__EXP_VALUE_L0 = 000.000    # Accepted mass of 0_Lambda in MeV/c^2

def get_total_momentum(particle_1, particle_2, parent_trajectory):
    theta_1 = get_angle(particle_1.path.trajectory.direction, parent_trajectory.direction)
    p_1 = particle_1.momentum * np.cos(theta_1)

    theta_2 = get_angle(particle_2.path.trajectory.direction, parent_trajectory.direction)
    p_2 = particle_2.momentum * np.cos(theta_2)

    return p_1 + p_2

T_0 = time.perf_counter()

# Kaon analysis
t_0 = time.perf_counter()

K0_trajectory = Trajectory('./img/K0_trajectory.png')
pi_minus = Particle('./img/K0_pimin.png', 139.4)
pi_plus = Particle('./img/K0_piplus.png', 139.4)

K0_momentum = get_total_momentum(pi_minus, pi_plus, K0_trajectory)
K0_energy = pi_plus.energy + pi_minus.energy

K0_mass = np.sqrt(mpow(K0_energy, 2) - mpow(K0_momentum, 2))

K0_err = abs(__EXP_VALUE_K0 - K0_mass)
K0_rel_err = K0_err / __EXP_VALUE_K0

t_1 = time.perf_counter()
delta_t_K0 = t_1 - t_0

# Lambda analysis

T_1 = time.perf_counter()
delta_T = T_1 - T_0

print('\n-------- K0 Analysis --------')
print('--- pi- info ---')
print(pi_minus)
print(f'theta:\t\t{get_angle(pi_minus.path.trajectory.direction, K0_trajectory.direction, False)} deg')

print('\n--- pi+ info')
print(pi_plus)
print(f'theta:\t\t{get_angle(pi_plus.path.trajectory.direction, K0_trajectory.direction, False)} deg')

print('\n--- K0 Info ---')
print(f'Momentum:\t{K0_momentum} MeV/c')
print(f'Energy:\t\t{K0_energy} MeV')
print(f'Mass:\t\t{K0_mass} MeV/c^2')

print('\n----- Error -----')
print(f'K0_err:\t\t{abs(__EXP_VALUE_K0 - K0_mass)}')
print(f'K0_rel_err:\t{K0_rel_err}')

print(f'\nKaon analysis time: {delta_t_K0} s')

print(f'Total program time: {delta_T} s')