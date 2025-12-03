import numpy as np
import RingSystem 

class Metamaterial:
    def __init__(self, meta_structure_type, structure_params):
        self.meta_structure_type = meta_structure_type  # Тип метаструктуры 
        self.structure_params = structure_params        
        self.ring_system = RingSystem()                
        self.currents = None                           
        self.fields = None                             
