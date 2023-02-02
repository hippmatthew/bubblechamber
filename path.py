import cv2
import numpy as np
from math import pow as m_pow

from linear_algebra import *
from constants import *


# Path gives us the complete info about the path a particle takes
class Path:
    def __init__(self, img_path):
        self.__img_path = img_path                                              # Directory of the corresponding path's png
        
        self.__start_pos = [0, 0]                                               # Starting position of the path in [y, x] due to how opencv reads images
        self.__second_pos = [0, 0]                                              # Second position in the curve. Used to define the initial direction. Same convention as above
        self.__end_pos = [0, 0]                                                 # Ending position of the path. Same convention as above

        self.arc_length = 0                                                     # Pixel distance of the path                                   

        self.__set_start_pos()
        self.__set_endpos_and_get_arc_length()
        
        self.init_direction = get_vector(self.__start_pos, self.__second_pos)   # Initial direction of the particle. Used to get the angle with the parent particle trajectory
        self.base_direction = get_vector(self.__start_pos, self.__end_pos)      # Direction from the stating position to the ending position. Used to find sagita

        self.__find_saggita()
        
        L = self.arc_length
        s = self.saggita
        self.curvature_radius = ((m_pow(L, 2) + 4 * m_pow(s, 2)) / (8 * s)) / PX2MM / 1000 * MAG_FACTOR *S_FACTOR # Distance to the center of the circle that the particle traces 

        
    def __set_start_pos(self):
        img = cv2.imread(self.__img_path)

        pos_found = False
        for i in range(0, IMG_WIDTH):
            for j in range(0, IMG_HEIGHT):
                if np.all(img[j, i] == START_POS_COL):
                    self.__start_pos = [j, i]
                    self.arc_length += 1
                    pos_found = True
                    break
            if pos_found: break
                
    def __set_endpos_and_get_arc_length(self):
        img = cv2.imread(self.__img_path)
        
        curr_pos = self.__start_pos
        prev_pos = self.__start_pos

        tracing = True
        while tracing:
            pos_found = False
            for i in range(-1, 2):
                x = curr_pos[1] + i
                
                for j in range(-1, 2):
                    y = curr_pos[0] + j

                    if np.any([y, x] != curr_pos) and np.any([y, x] != prev_pos) and np.all(img[y, x] == READ_COL):
                        prev_pos = curr_pos
                        curr_pos = [y, x]
                        self.arc_length += 1
                    
                        # gets a point that enables us to get an estimate of the initial direction
                        if self.arc_length == 30:
                            self.__second_pos = curr_pos

                        pos_found = True
                
                if pos_found: break
                elif i == 1:
                    self.__end_pos = curr_pos
                    tracing = False

    def __find_saggita(self):
        img = cv2.imread(self.__img_path)
        
        curr_pos = self.__start_pos
        prev_pos = self.__start_pos

        curr_max_distance = 0

        tracing = True
        while tracing:
            pos_found = False
            for i in range(-1, 2):
                x = curr_pos[1] + i
                
                for j in range(-1, 2):
                    y = curr_pos[0] + j

                    if np.any([y, x] != curr_pos) and np.any([y, x] != prev_pos) and np.all(img[y, x] == READ_COL):
                        prev_pos = curr_pos
                        curr_pos = [y, x]

                        pos_vec = get_vector(self.__start_pos, curr_pos)
                        
                        scale_factor = scalar_product(pos_vec, normalize(self.base_direction))
                        neg_proj_vec = [-1 * scale_factor * self.base_direction[0], -1 * scale_factor * self.base_direction[1]]
                    
                        perp_vec = add_vectors(pos_vec, neg_proj_vec)
                        distance = get_magnitude(perp_vec)

                        if distance > curr_max_distance:
                            curr_max_distance = distance

                        pos_found = True
                
                if pos_found: break
                elif i == 1:
                    self.saggita = curr_max_distance
                    tracing = False

class Trajectory:
    def __init__(self, img_path):
        self.__img_path = img_path
        
        self.__start_pos = [0, 0]
        self.__end_pos = [0, 0]

        self.__find_points()

        self.direction = get_vector(self.__start_pos, self.__end_pos, False)
        self.length = get_magnitude(self.direction) / PX2MM * MAG_FACTOR * S_FACTOR
        self.direction = normalize(self.direction)

    def __find_points(self):
        img = cv2.imread(self.__img_path)
        
        pos_found = [False, False]
        for i in range(0, IMG_WIDTH):
            for j in range(0, IMG_HEIGHT):
                if np.all(img[j, i] == START_POS_COL):
                    self.__start_pos = [j, i]
                    pos_found[0] = True
                    break
                elif np.all(img[j,i] == TRAJ_END_POS_COL):
                    self.__end_pos = [j, i]
                    pos_found[1] = True
                    break
            if np.all(pos_found == True): break
    
   
