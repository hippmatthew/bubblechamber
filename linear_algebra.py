import numpy as np

# Gets the vector from two opencv points ** opencv point := [y, x] **
def get_vector(start_pos, end_pos, normalized = True):
        x = end_pos[1] - start_pos[1]
        y = end_pos[0] - start_pos[0]
        
        mag = get_magnitude([x, y])
        
        return [x / mag, y / mag] if normalized else [x, y]

def get_magnitude(vec):
    return np.sqrt(scalar_product(vec, vec))

def normalize(vec):
    norm = get_magnitude(vec)
    vec[0] /= norm
    vec[1] /= norm
        
    return vec
    
def get_angle(vec_1, vec_2, rad = True):
    vec_1 = normalize(vec_1)
    vec_2 = normalize(vec_2)

    dot = scalar_product(vec_1, vec_2)

    return np.arccos(dot) if rad else np.arccos(dot) * 180 / np.pi

def scalar_product(vec_1, vec_2):
    return vec_1[0]*vec_2[0] + vec_1[1]*vec_2[1]

def add_vectors(vec_1, vec_2):
    x = vec_1[0] + vec_2[0]
    y = vec_1[1] + vec_2[1]

    return [x, y]