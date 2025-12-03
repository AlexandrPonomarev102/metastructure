import numpy as np
import RingSystem 


#TODO кольцо, период решетки, эффективные параметры

class Metamaterial:
    def __init__(self, meta_structure_type, structure_params):
        self.structure_params = structure_params        
        self.ring_system = RingSystem()                
        self.currents = None                           
        self.fields = None                             
