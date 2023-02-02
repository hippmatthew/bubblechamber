from math import pow as m_pow
from math import sqrt, cos
import time

from particle import Particle
from path import Trajectory
from linear_algebra import get_angle
from constants import *

def analyze(parent_traj, particle_1, particle_2, exp_vals):
    theta_1 = get_angle(parent_traj.direction, particle_1.path.init_direction)
    p_1 = particle_1.momentum * cos(theta_1)

    theta_2 = get_angle(parent_traj.direction, particle_2.path.init_direction)
    p_2 = particle_2.momentum * cos(theta_2)

    P = p_1 + p_2
    E = particle_1.energy + particle_2.energy
    m = sqrt(m_pow(E, 2) - m_pow(P, 2))
    
    v = P / sqrt(m_pow(m, 2) + m_pow(P, 2))
    tau = parent_traj.length / (v * LIGHT_SPEED)
    
    m_err = abs(m - exp_vals[0])
    m_rel_err = m_err / exp_vals[0]

    tau_err = abs(tau - exp_vals[1])
    tau_rel_err = tau_err / exp_vals[1]

    print(f'p:\t\t{P} MeV/c')
    print(f'v:\t\t{v} c')
    print(f'E:\t\t{E} MeV')
    
    print(f'\nm:\t\t{m} MeV/c^2')
    print(f'm_err:\t\t{m_err} MeV/c^2')
    print(f'm_rel_err:\t{m_rel_err}')
    
    print(f'\ntau:\t\t{tau} ps')
    print(f'tau_err:\t{tau_err} ps')
    print(f'tau_rel_err:\t{tau_rel_err}')

T_0 = time.perf_counter()

# Kaon analysis
t_0 = time.perf_counter()

K0_trajectory = Trajectory('./img/K0_start_end_pos.png')
K0_pi_minus = Particle('./img/K0_pimin.png', PION_MASS)
pi_plus = Particle('./img/K0_piplus.png', PION_MASS)

print('--- Kaon Analysis ---')
analyze(K0_trajectory, K0_pi_minus, pi_plus, [KAON_MASS, KAON_LIFETIME])

t_1 = time.perf_counter()
delta_t = t_1 - t_0
print(f'\nK0 delta_t: {delta_t} s')

# Lambda analysis
t_0 = time.perf_counter()

L0_trajectory = Trajectory('./img/L0_start_end_pos.png')
proton = Particle('./img/L0_prot.png', PROTON_MASS)
L0_pi_minus = Particle('./img/L0_pimin.png', PION_MASS)

print('\n--- Lambda Analysis ---')
analyze(L0_trajectory, L0_pi_minus, proton, [LAMBDA_MASS, LAMBDA_LIFETIME])

t_1 = time.perf_counter()
delta_t = t_1 - t_0
print(f'\nL0 delta_t: {delta_t} s')

T_1 = time.perf_counter()
delta_T = T_1 - T_0
print(f'\nprogram run time: {delta_T} s')