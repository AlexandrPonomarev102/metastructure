import numpy as np
from abc import ABC, abstractmethod

class MetaStructure(ABC):
    """
    Абстрактный класс типа метаструктуры.
    Только расчетные функции, без хранения данных.
    """
    
    @abstractmethod
    def get_default_parameters(self):
        """Получить параметры по умолчанию"""
        pass
    
    @abstractmethod
    def validate_parameters(self, **kwargs):
        """Проверка корректности параметров"""
        pass
    
    @abstractmethod
    def calculate_geometry(self, **kwargs):
        """Расчет геометрии структуры"""
        pass
    
    @abstractmethod
    def calculate_ring_configurations(self, **kwargs):
        """Расчет конфигураций колец"""
        pass


class CubicStructure(MetaStructure):
    """Кубическая периодическая структура"""
    
    def get_default_parameters(self):
        """Возвращает параметры по умолчанию"""
        return {
            "ring_radius": 0.003,
            "strip_width": 0.0005,
            "capacitance": 470e-12,
            "resistance": 1.0,
            "inductance": 1e-9,
            "cube_size": 1.0,
            "unit_size": 0.01,
            "grid_x": 3,
            "grid_y": 3,
            "grid_z": 3,
            "rings_on_edges": True,
            "rings_on_faces": True,
            "rings_on_corners": True,
            "frequency": 1e6,
        }
    
    def validate_parameters(self, **kwargs):
        """Проверка корректности параметров"""
        params = self.get_default_parameters()
        params.update(kwargs)
        
        if params["grid_x"] <= 0 or params["grid_y"] <= 0 or params["grid_z"] <= 0:
            raise ValueError("Размеры решетки должны быть положительными")
        
        if params["cube_size"] <= 0 or params["unit_size"] <= 0:
            raise ValueError("Размеры должны быть положительными")
        
        return True
    
    def calculate_geometry(self, **kwargs):
        """Расчет геометрии кубической структуры"""
        self.validate_parameters(**kwargs)
        
        params = self.get_default_parameters()
        params.update(kwargs)
        
        cube_size = params["cube_size"]
        unit_size = params["unit_size"]
        grid_x = params["grid_x"]
        grid_y = params["grid_y"]
        grid_z = params["grid_z"]
        
        # Генерация вершин
        vertices = []
        for x in range(grid_x + 1):
            for y in range(grid_y + 1):
                for z in range(grid_z + 1):
                    vertex = np.array([
                        x * cube_size * unit_size,
                        y * cube_size * unit_size,
                        z * cube_size * unit_size
                    ])
                    vertices.append(vertex)
        
        vertices = np.array(vertices)
        
        # Генерация ребер
        edges = []
        for x in range(grid_x):
            for y in range(grid_y):
                for z in range(grid_z):
                    base_idx = x * (grid_y + 1) * (grid_z + 1) + y * (grid_z + 1) + z
                    v_indices = [
                        base_idx,
                        base_idx + 1,
                        base_idx + (grid_z + 1),
                        base_idx + (grid_z + 1) + 1,
                        base_idx + (grid_y + 1) * (grid_z + 1),
                        base_idx + (grid_y + 1) * (grid_z + 1) + 1,
                        base_idx + (grid_y + 1) * (grid_z + 1) + (grid_z + 1),
                        base_idx + (grid_y + 1) * (grid_z + 1) + (grid_z + 1) + 1
                    ]
                    
                    # 12 ребер куба
                    cube_edges = [
                        (v_indices[0], v_indices[1]), (v_indices[0], v_indices[2]),
                        (v_indices[1], v_indices[3]), (v_indices[2], v_indices[3]),
                        (v_indices[4], v_indices[5]), (v_indices[4], v_indices[6]),
                        (v_indices[5], v_indices[7]), (v_indices[6], v_indices[7]),
                        (v_indices[0], v_indices[4]), (v_indices[1], v_indices[5]),
                        (v_indices[2], v_indices[6]), (v_indices[3], v_indices[7])
                    ]
                    edges.extend(cube_edges)
        
        # Генерация граней
        faces = []
        for x in range(grid_x):
            for y in range(grid_y):
                for z in range(grid_z):
                    base_idx = x * (grid_y + 1) * (grid_z + 1) + y * (grid_z + 1) + z
                    v_indices = [
                        base_idx,
                        base_idx + 1,
                        base_idx + (grid_z + 1),
                        base_idx + (grid_z + 1) + 1,
                        base_idx + (grid_y + 1) * (grid_z + 1),
                        base_idx + (grid_y + 1) * (grid_z + 1) + 1,
                        base_idx + (grid_y + 1) * (grid_z + 1) + (grid_z + 1),
                        base_idx + (grid_y + 1) * (grid_z + 1) + (grid_z + 1) + 1
                    ]
                    
                    # 6 граней куба
                    cube_faces = [
                        (v_indices[0], v_indices[1], v_indices[3], v_indices[2]),
                        (v_indices[4], v_indices[5], v_indices[7], v_indices[6]),
                        (v_indices[0], v_indices[1], v_indices[5], v_indices[4]),
                        (v_indices[2], v_indices[3], v_indices[7], v_indices[6]),
                        (v_indices[0], v_indices[2], v_indices[6], v_indices[4]),
                        (v_indices[1], v_indices[3], v_indices[7], v_indices[5])
                    ]
                    faces.extend(cube_faces)
        
        return vertices, edges, faces
    
    def calculate_ring_configurations(self, **kwargs):
        """Расчет конфигураций колец для кубической структуры"""
        self.validate_parameters(**kwargs)
        
        params = self.get_default_parameters()
        params.update(kwargs)
        
        cube_size = params["cube_size"]
        unit_size = params["unit_size"]
        grid_x = params["grid_x"]
        grid_y = params["grid_y"]
        grid_z = params["grid_z"]
        
        ring_radius = params["ring_radius"]
        strip_width = params["strip_width"]
        capacitance = params["capacitance"]
        resistance = params["resistance"]
        inductance = params["inductance"]
        frequency = params["frequency"]
        omega = 2 * np.pi * frequency
        
        rings_on_faces = params["rings_on_faces"]
        rings_on_edges = params["rings_on_edges"]
        rings_on_corners = params["rings_on_corners"]
        
        positions = []
        orientations = []
        ring_params_list = []
        
        # Кольца на гранях (все 3 плоскости)
        if rings_on_faces:
            # 1. Кольца на гранях, перпендикулярных оси X (плоскость YZ)
            for x in range(grid_x + 1):
                for y in range(grid_y):
                    for z in range(grid_z):
                        center = np.array([
                            x * cube_size * unit_size,
                            (y + 0.5) * cube_size * unit_size,
                            (z + 0.5) * cube_size * unit_size
                        ])
                        # Нормаль к грани (направлена вдоль оси X)
                        orientation = np.array([1, 0, 0]) if x < grid_x else np.array([-1, 0, 0])
                        positions.append(center)
                        orientations.append(orientation)
                        ring_params_list.append({
                            "R": resistance,
                            "L": inductance,
                            "C": capacitance,
                            "omega": omega,
                            "radius": ring_radius,
                            "strip_width": strip_width
                        })
            
            # 2. Кольца на гранях, перпендикулярных оси Y (плоскость XZ)
            for x in range(grid_x):
                for y in range(grid_y + 1):
                    for z in range(grid_z):
                        center = np.array([
                            (x + 0.5) * cube_size * unit_size,
                            y * cube_size * unit_size,
                            (z + 0.5) * cube_size * unit_size
                        ])
                        # Нормаль к грани (направлена вдоль оси Y)
                        orientation = np.array([0, 1, 0]) if y < grid_y else np.array([0, -1, 0])
                        positions.append(center)
                        orientations.append(orientation)
                        ring_params_list.append({
                            "R": resistance,
                            "L": inductance,
                            "C": capacitance,
                            "omega": omega,
                            "radius": ring_radius,
                            "strip_width": strip_width
                        })
            
            # 3. Кольца на гранях, перпендикулярных оси Z (плоскость XY)
            for x in range(grid_x):
                for y in range(grid_y):
                    for z in range(grid_z + 1):
                        center = np.array([
                            (x + 0.5) * cube_size * unit_size,
                            (y + 0.5) * cube_size * unit_size,
                            z * cube_size * unit_size
                        ])
                        # Нормаль к грани (направлена вдоль оси Z)
                        orientation = np.array([0, 0, 1]) if z < grid_z else np.array([0, 0, -1])
                        positions.append(center)
                        orientations.append(orientation)
                        ring_params_list.append({
                            "R": resistance,
                            "L": inductance,
                            "C": capacitance,
                            "omega": omega,
                            "radius": ring_radius,
                            "strip_width": strip_width
                        })
        
        # Кольца на ребрах (все 3 направления)
        if rings_on_edges:
            # 1. Ребра параллельные оси X
            for x in range(grid_x):
                for y in range(grid_y + 1):
                    for z in range(grid_z + 1):
                        center = np.array([
                            (x + 0.5) * cube_size * unit_size,
                            y * cube_size * unit_size,
                            z * cube_size * unit_size
                        ])
                        # Ориентация вдоль оси X
                        orientation = np.array([1, 0, 0])
                        positions.append(center)
                        orientations.append(orientation)
                        ring_params_list.append({
                            "R": resistance,
                            "L": inductance,
                            "C": capacitance,
                            "omega": omega,
                            "radius": ring_radius,
                            "strip_width": strip_width
                        })
            
            # 2. Ребра параллельные оси Y
            for x in range(grid_x + 1):
                for y in range(grid_y):
                    for z in range(grid_z + 1):
                        center = np.array([
                            x * cube_size * unit_size,
                            (y + 0.5) * cube_size * unit_size,
                            z * cube_size * unit_size
                        ])
                        # Ориентация вдоль оси Y
                        orientation = np.array([0, 1, 0])
                        positions.append(center)
                        orientations.append(orientation)
                        ring_params_list.append({
                            "R": resistance,
                            "L": inductance,
                            "C": capacitance,
                            "omega": omega,
                            "radius": ring_radius,
                            "strip_width": strip_width
                        })
            
            # 3. Ребра параллельные оси Z
            for x in range(grid_x + 1):
                for y in range(grid_y + 1):
                    for z in range(grid_z):
                        center = np.array([
                            x * cube_size * unit_size,
                            y * cube_size * unit_size,
                            (z + 0.5) * cube_size * unit_size
                        ])
                        # Ориентация вдоль оси Z
                        orientation = np.array([0, 0, 1])
                        positions.append(center)
                        orientations.append(orientation)
                        ring_params_list.append({
                            "R": resistance,
                            "L": inductance,
                            "C": capacitance,
                            "omega": omega,
                            "radius": ring_radius,
                            "strip_width": strip_width
                        })
        
        # Кольца в углах (пересечениях трех граней)
        if rings_on_corners:
            for x in range(grid_x + 1):
                for y in range(grid_y + 1):
                    for z in range(grid_z + 1):
                        center = np.array([
                            x * cube_size * unit_size,
                            y * cube_size * unit_size,
                            z * cube_size * unit_size
                        ])
                        # Ориентация по диагонали (нормализованная сумма направлений)
                        orientation = np.array([1, 1, 1])
                        orientation = orientation / np.linalg.norm(orientation)
                        positions.append(center)
                        orientations.append(orientation)
                        ring_params_list.append({
                            "R": resistance,
                            "L": inductance,
                            "C": capacitance,
                            "omega": omega,
                            "radius": ring_radius,
                            "strip_width": strip_width
                        })
        
        return np.array(positions), np.array(orientations), ring_params_list