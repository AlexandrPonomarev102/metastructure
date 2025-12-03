import numpy as np

class ImpedanceMatrixBuilder:
    def __init__(self, num_rings, R, L, C, omega):
        self.N = num_rings
        self.R = R
        self.L = L
        self.C = C
        self.omega = omega

class MutualInductanceCalculator:
    def __init__(self, ring_radius, strip_width):
        self.r0 = ring_radius
        self.w = strip_width

    def mutual_inductance(self,):
        """
        Расчет взаимной индуктивности между двумя кольцами.

        Parameters:
        pos_n, pos_m : трехмерные координаты центров колец
        orientation_n, orientation_m : нормали колец (векторы)

        Returns:
        float : значение взаимной индуктивности M[n, m]
        """
        pass


class ExternalFluxCalculator:
    def __init__(self, positions, orientations):
        self.positions = positions
        self.orientations = orientations

    def compute_external_flux(self, B_field):
        """
        Parameters:
        B_field : ndarray (N, 3) - вектор магнитного поля в точках позиций колец

        Returns:
        ndarray (N,) - вектор внешних потоков Phi_ext
        """
        # Проекция магнитного поля на нормали колец
        flux = np.array([np.dot(B, n) for B, n in zip(B_field, self.orientations)])
        r0 = 1
        area = np.pi * r0 ** 2
        return flux * area

    def build_impedance_matrix(self, mutual_inductances):
        """
        Параметры:
        mutual_inductances : ndarray (N, N) взаимные индуктивности

        Returns:
        ndarray (N, N) матрица импедансов Z
        """
        Z = np.zeros((self.N, self.N), dtype=complex)
        Z0 = self.R + 1j * self.omega * self.L + 1 / (1j * self.omega * self.C)
        np.fill_diagonal(Z, Z0)

        for i in range(self.N):
            for j in range(self.N):
                if i != j:
                    Z[i, j] = 1j * self.omega * mutual_inductances[i, j]

        return Z

class Solver:
    def __init__(self, method='direct'):
        self.method = method #
        
    def solve(self, Z, V):
        pass

