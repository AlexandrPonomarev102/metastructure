class MetaStructure:
    """
    Тип метаструктуры
    Определяет общие свойства и поведение типа материала
    """
    
    def __init__(self, structure_type, description="", typical_params=None):
        """
        Args:
            structure_type: тип структуры 
            description: описание структуры
            typical_params: типичные параметры для этого типа
        """
        self.structure_type = structure_type
        self.description = description
        self.typical_params = typical_params if typical_params else {}
        
        # Предопределенные типы структур
        self.STRUCTURE_TYPES = {
            "cubic": "Кубическая структура с кольцами на гранях кубов"
        }
        
    def get_structure_info(self):
        """Получить информацию о типе структуры"""
        info = f"Structure type: {self.structure_type}\n"
        info += f"Description: {self.description}\n"
        info += "Typical parameters:\n"
        for key, value in self.typical_params.items():
            info += f"  {key}: {value}\n"
        return info
        #TODO: Добавить атрибутом метаматериал 
    def create_default_params(self):     
        """Создать параметры по умолчанию для этого типа структуры"""
        self.defaults = {         #TODO поменять со словаря в атрибуты 
            "CLR": {
                "ring_radius": 0.0049,  # м
                "strip_width": 0.0022,  # м
                "capacitance": 470e-12,  # Ф
                "lattice_constant": 0.015,  # м
            },
            "SRR": {
                "ring_radius": 0.005,
                "gap_width": 0.001,
                "strip_width": 0.0005,
                "lattice_constant": 0.01,
            },
             "cubic": { 
                "ring_radius": 0.003,        # Радиус кольца (м)
                "strip_width": 0.0005,       # Ширина полоски (м)
                "capacitance": 470e-12,      # Емкость (Ф)
                "resistance": 1.0,           # Сопротивление (Ом)
                "inductance": 1e-9,          # Индуктивность (Гн)
                "cube_size": 1.0,            # Размер куба в условных единицах
                "unit_size": 0.01,           # Размер одной условной единицы (м)
                "num_cubes_x": 1,            # Количество кубов по оси X
                "num_cubes_y": 1,            # Количество кубов по оси Y 
                "num_cubes_z": 1,            # Количество кубов по оси Z
                "frequency": 1e6,            # Частота (Гц)
                "rings_on_edges": True,      # Кольца на ребрах
                "rings_on_faces": True,      # Кольца на гранях
                "rings_on_corners": True     # Кольца в углах (пересечениях граней)
            } 

            
        }
        return self.defaults.get(self.structure_type, {})
        
    def validate_params(self, params):
        """Проверить корректность параметров для этого типа структуры"""
        required = self.get_required_params()
        for param in required:
            if param not in params:
                raise ValueError(f"Отсутствует обязательный параметр: {param}")
        return True
        
    def __repr__(self):
        return f"MetaStructure(type={self.structure_type})"