import cv2
import numpy as np
from math import pow as mpow
from linear_algebra import *


# Path gives us the complete info about the path a particle takes
class Path:
    def __init__(self, img_path):
        # Colors in [B, G, R] colorspace due to opencv
        self.__START_POS_COL = [255, 0, 238]
        self.__COL = [0, 0, 255]
        self.__conversion_factor = 8.8388                                   # pixels/mm defined on a per computer basis -- appx. 3000 px / 13.6 in * 0.3 / mm for me
        
        self.__img_path = img_path                                          # Directory of the corresponding path's png
        self.__start_pos = [0, 0]                                           # Starting position of the path in [y, x] due to how opencv reads images
        self.__end_pos = [0, 0]                                             # Ending position of the path. Same convention as above

        self.arc_length = 0                                                 # Pixel distance of the path                                   

        self.__set_start_pos()
        self.__set_endpos_and_get_arc_length()
        self.arc_length = self.arc_length / self.__conversion_factor 
        
        self.trajectory = Trajectory(self.__img_path, self.__COL)           # Initial direction of the vector. Used to get the angle with the parent particle trajectory
        self.base_direction = get_vector(self.__start_pos, self.__end_pos)  # Direction from the stating position to the ending position. Used to find sagita

        self.__find_saggita()
        self.saggita = self.saggita / self.__conversion_factor
        
        L = self.arc_length
        s = self.saggita
        self.curvature_radius = (mpow(L, 2) + 4 * mpow(s, 2)) / (8 * s)       # Distance to the center of the circle that the particle traces 

        
    def __set_start_pos(self, img_width = 580, img_height = 559):
        img = cv2.imread(self.__img_path)

        pos_found = False
        for i in range(0, img_width):
            for j in range(0, img_height):
                if np.all(img[j, i] == self.__START_POS_COL):
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

                    if np.any([y, x] != curr_pos) and np.any([y, x] != prev_pos) and np.all(img[y, x] == self.__COL):
                        prev_pos = curr_pos
                        curr_pos = [y, x]
                        self.arc_length += 1
                    
                        # gets a point that enables us to get an estimate of the initial direction
                        if self.arc_length == 12:
                            self.__tan_pos = curr_pos

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

                    if np.any([y, x] != curr_pos) and np.any([y, x] != prev_pos) and np.all(img[y, x] == self.__COL):
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

# Initial direction of travel of the particle. I have defined this to be a tangent vctor to the curve calculated from the start positon to the 12th pixel's position
class Trajectory:
    def __init__(self, img_path, read_color = [255, 187, 0]):
        self.__START_POS_COL = [255, 0, 238]
        self.__COL = read_color
        
        self.__img_path = img_path
        self.__start_pos = [0, 0]
        self.__end_pos = [0, 0]

        self.__set_start_pos()
        self.__set_end_pos()

        self.direction = get_vector(self.__start_pos, self.__end_pos)
    
    def __set_start_pos(self, img_width = 580, img_height = 559):
        img = cv2.imread(self.__img_path)

        pos_found = False
        for i in range(0, img_width):
            for j in range(0, img_height):
                if np.all(img[j, i] == self.__START_POS_COL):
                    self.__start_pos = [j, i]
                    pos_found = True
                    break
            if pos_found: break

    def __set_end_pos(self):
        img = cv2.imread(self.__img_path)

        curr_pos = self.__start_pos
        prev_pos = self.__start_pos

        count = 1
        tracing = True
        while tracing:
            pos_found = False
            for i in range(-1, 2):
                x = curr_pos[1] + i

                for j in range(-1, 2):
                    y = curr_pos[0] + j
                
                    if np.any([y, x] != curr_pos) and np.any([y, x] != prev_pos) and np.all(img[y, x] == self.__COL):
                        prev_pos = curr_pos
                        curr_pos = [y, x]
                        pos_found = True
                        count += 1
                        break
                
                if pos_found: break
                elif i == 1 or count == 12:
                    self.__end_pos = curr_pos
                    tracing = False
