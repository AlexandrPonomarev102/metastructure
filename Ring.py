import numpy as np
from Solver import MutualInductanceCalculator
from Solver import ImpedanceMatrixBuilder
from Solver import ExternalFluxCalculator
class Ring:
    def __init__(self, position, orientation, R, L, C, omega):
        self.position = position
        self.orientation = orientation
        self.R = R
        self.L = L
        self.C = C
        self.omega = omega
        
    def build_impedance_matrix(self, ring_system):
        positions = ring_system.get_positions()
        orientations = ring_system.get_orientations()
        N = len(positions)
        
        mutual_calc = MutualInductanceCalculator(ring_radius=1, strip_width=1)
        L_matrix = np.zeros((N, N), dtype=float)
        
        for i in range(N):
            for j in range(N):
                if i != j:
                    L_matrix[i, j] = mutual_calc.mutual_inductance(
                        positions[i], orientations[i],
                        positions[j], orientations[j]
                    )
                    
        impedance_builder = ImpedanceMatrixBuilder(N, self.R, self.L, self.C, self.omega)
        return impedance_builder.build_impedance_matrix(L_matrix)
        
    def build_external_flux_vector(self, ring_system, B_field_external):
        positions = ring_system.get_positions()
        orientations = ring_system.get_orientations()
        
        flux_calc = ExternalFluxCalculator(positions, orientations)
        Phi_ext = flux_calc.compute_external_flux(B_field_external)
        return -1j * self.omega * Phi_ext
