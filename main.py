from Metastructure import CubicStructure
from Metamaterial import Metamaterial

# Создаем тип структуры
cubic_structure = CubicStructure()

# Создаем конкретный материал
material = Metamaterial(
    structure_type=cubic_structure,
    grid_x=2,
    grid_y=2,
    grid_z=2,
    cube_size=1.0,
    unit_size=0.01,
    ring_radius=0.005,
    frequency=1e9,
    rings_on_faces=True,
    rings_on_edges=False,
    rings_on_corners=False
)

# Выводим информацию
print(material.get_parameters_info())
print(material.get_geometry_info())

print(f"\nВсего колец: {material.get_ring_count()}")

# Визуализируем (если установлен plotly)
material.visualize()

# Выводим информацию
print("=== ИНФОРМАЦИЯ О МАТЕРИАЛЕ ===")
print(material.get_parameters_info())
print(material.get_geometry_info())

# Добавляем пользовательское кольцо
material.add_custom_ring(
    position=[0.05, 0.05, 0.05],
    orientation=[1, 0, 0]
)

print(f"Всего колец после добавления: {material.get_ring_count()}")

# Визуализируем
material.visualize()

# Работа с системой колец напрямую
print("\n=== СТАТИСТИКА СИСТЕМЫ КОЛЕЦ ===")
stats = material.ring_system.get_statistics()
for key, value in stats.items():
    print(f"{key}: {value}")