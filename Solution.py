import numpy as np

class Solution:
    """
    Сохранялка данных
    """
    def __init__(self, currents, frequencies=None, parameters=None):
        self.currents = currents
        self.frequencies = frequencies
        self.parameters = parameters
        
    def save(self, filename):
        data = {
            'currents': self.currents,
            'frequencies': self.frequencies,
            'parameters': self.parameters
        }
        np.savez(filename, **data) #??
            
    @classmethod 
    def load(cls, filename):
        data = np.load(filename)
        return cls(
            currents=data['currents'],
            frequencies=data['frequencies'].item() if 'frequencies' in data.files else None,
            parameters=data['parameters'].item() if 'parameters' in data.files else None
        )
