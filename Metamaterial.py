import numpy as np
from RingSystem import RingSystem

class Metamaterial:
    """
    Конкретный экземпляр метаматериала.
    Хранит ВСЕ данные: параметры, геометрию, кольца.
    """
    
    def __init__(self, structure_type, **kwargs):
        """
        Args:
            structure_type: объект типа структуры (например, CubicStructure)
            **kwargs: параметры для материала
        """
        self.structure = structure_type
        
        # Параметры материала
        self._init_parameters(kwargs)
        
        # Геометрия
        self.vertices = None
        self.edges = None
        self.faces = None
        
        # Система колец
        self.ring_system = RingSystem()
        
        # Эффективные параметры
        self.effective_permittivity = None
        self.effective_permeability = None
        self.refractive_index = None
        
        # Построение материала
        self._build_material()  # Исправлено с build() на _build_material()
    
    def _init_parameters(self, kwargs):
        """Инициализация параметров как атрибутов"""
        default_params = self.structure.get_default_parameters()
        
        # Объединяем с переданными параметрами
        for key, value in kwargs.items():
            if key in default_params:
                default_params[key] = value
        
        # Проверяем корректность
        self.structure.validate_parameters(**default_params)
        
        # Создаем атрибуты
        for key, value in default_params.items():
            setattr(self, key, value)
        
        # Вычисляемые параметры
        self.omega = 2 * np.pi * self.frequency
    
    def _build_material(self):
        """Построение материала"""
        # Получаем параметры
        params_dict = {}
        default_params = self.structure.get_default_parameters()
        for key in default_params.keys():
            if hasattr(self, key):
                params_dict[key] = getattr(self, key)
        
        # Расчет геометрии
        self.vertices, self.edges, self.faces = self.structure.calculate_geometry(**params_dict)
        
        # Расчет конфигураций колец
        positions, orientations, ring_params_list = self.structure.calculate_ring_configurations(**params_dict)
        
        # Создание колец
        for i in range(len(positions)):
            ring_data = ring_params_list[i]
            self.ring_system.add_ring(
                position=positions[i],
                orientation=orientations[i],
                R=ring_data["R"],
                L=ring_data["L"],
                C=ring_data["C"],
                omega=ring_data["omega"],
                radius=ring_data["radius"],
                strip_width=ring_data["strip_width"]
            )
    
    def get_ring_count(self):
        """Количество колец"""
        return len(self.ring_system.rings)
    
    def get_vertex_count(self):
        """Количество вершин"""
        return len(self.vertices) if self.vertices is not None else 0
    
    def get_edge_count(self):
        """Количество ребер"""
        return len(self.edges) if self.edges is not None else 0
    
    def get_face_count(self):
        """Количество граней"""
        return len(self.faces) if self.faces is not None else 0
    
    def get_size(self):
        """Размер материала"""
        if self.vertices is not None and len(self.vertices) > 0:
            min_coords = np.min(self.vertices, axis=0)
            max_coords = np.max(self.vertices, axis=0)
            return max_coords - min_coords
        return np.array([0, 0, 0])
    
    def get_parameters_info(self):
        """Информация о параметрах"""
        info = "=== ПАРАМЕТРЫ МАТЕРИАЛА ===\n"
        params = self.structure.get_default_parameters()
        for key in params.keys():
            if hasattr(self, key):
                value = getattr(self, key)
                info += f"{key}: {value}\n"
        return info
    
    def get_geometry_info(self):
        """Информация о геометрии"""
        info = "=== ГЕОМЕТРИЯ МАТЕРИАЛА ===\n"
        info += f"Вершины: {self.get_vertex_count()}\n"
        info += f"Ребра: {self.get_edge_count()}\n"
        info += f"Грани: {self.get_face_count()}\n"
        info += f"Кольца: {self.get_ring_count()}\n"
        
        size = self.get_size()
        info += f"Размер: {size[0]:.4f} x {size[1]:.4f} x {size[2]:.4f} м\n"
        
        return info
    
    def add_ring(self, position, orientation, R=None, L=None, C=None, 
                 omega=None, radius=None, strip_width=None):
        """Добавить пользовательское кольцо"""
        R = R or self.resistance
        L = L or self.inductance
        C = C or self.capacitance
        omega = omega or self.omega
        radius = radius or self.ring_radius
        strip_width = strip_width or self.strip_width
        
        self.ring_system.add_ring(
            position=position,
            orientation=orientation,
            R=R,
            L=L,
            C=C,
            omega=omega,
            radius=radius,
            strip_width=strip_width
        )
    
    def remove_ring(self, index):
        """Удалить кольцо"""
        return self.ring_system.remove_ring(index)
    
    def visualize(self):
        """Визуализация"""
        self.ring_system.visualize(
            vertices=self.vertices,
            edges=self.edges
        )
    
    def __repr__(self):
        return f"Metamaterial(rings={self.get_ring_count()}, vertices={self.get_vertex_count()})"