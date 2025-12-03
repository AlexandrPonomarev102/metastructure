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
        }
        
    def get_structure_info(self):
        """Получить информацию о типе структуры"""
        info = f"Structure type: {self.structure_type}\n"
        info += f"Description: {self.description}\n"
        info += "Typical parameters:\n"
        for key, value in self.typical_params.items():
            info += f"  {key}: {value}\n"
        return info
        
    def create_default_params(self):
        """Создать параметры по умолчанию для этого типа структуры"""
        defaults = {
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
            }
        }
        return defaults.get(self.structure_type, {})
        
    def validate_params(self, params):
        """Проверить корректность параметров для этого типа структуры"""
        required = self.get_required_params()
        for param in required:
            if param not in params:
                raise ValueError(f"Отсутствует обязательный параметр: {param}")
        return True
        
    def get_required_params(self):
        """Получить список обязательных параметров для этого типа структуры"""
        requirements = {
            "CLR": ["ring_radius", "strip_width", "capacitance", "lattice_constant"],
            "SRR": ["ring_radius", "gap_width", "strip_width", "lattice_constant"],
        }
        return requirements.get(self.structure_type, [])
        
    def __repr__(self):
        return f"MetaStructure(type={self.structure_type})"