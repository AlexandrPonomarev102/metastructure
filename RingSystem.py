import numpy as np
from Ring import Ring

class RingSystem:
    def __init__(self):
        self.rings = []
        self.orientations = np.array([])
        self.positions = np.array([])
        self.currents = None #токи

    def add_ring(self, position, orientation, R, L, C, omega):
        ring = Ring(position, orientation, R, L, C, omega)
        self.orientations = np.append(self.orientations, orientation)
        self.positions = np.append(self.positions, position)

        self.rings.append(ring)
        
    def get_rings(self):
        return self.rings
        
    def get_positions(self):
        return self.positions        
    def get_orientations(self):
        return self.orientations    


    def visualize(self):
        pass

    #сделать функцию чето типа гетфилдс
