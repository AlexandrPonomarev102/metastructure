import numpy as np

class RingSystem:
    """
    Система колец. Хранит ВСЕ кольца.
    """
    
    def __init__(self):
        self.rings = []
        self.positions = np.array([]).reshape(0, 3)
        self.orientations = np.array([]).reshape(0, 3)
        self.currents = None
    
    def add_ring(self, position, orientation, R, L, C, omega, radius=0.003, strip_width=0.0005):
        """Добавить кольцо"""
        from Ring import Ring
        ring = Ring(position, orientation, R, L, C, omega, radius, strip_width)
        self.rings.append(ring)
        
        if len(self.positions) == 0:
            self.positions = np.array([position])
            self.orientations = np.array([orientation])
        else:
            self.positions = np.vstack([self.positions, position])
            self.orientations = np.vstack([self.orientations, orientation])
    
    def remove_ring(self, index):
        """Удалить кольцо"""
        if 0 <= index < len(self.rings):
            del self.rings[index]
            self.positions = np.delete(self.positions, index, axis=0)
            self.orientations = np.delete(self.orientations, index, axis=0)
            return True
        return False
    
    def get_positions(self):
        """Получить позиции всех колец"""
        return self.positions
    
    def get_orientations(self):
        """Получить ориентации всех колец"""
        return self.orientations
    
    def visualize(self, vertices=None, edges=None):
        """Визуализация системы колец"""
        try:
            import plotly.graph_objects as go
            
            fig = go.Figure()
            
            # Вершины
            if vertices is not None and len(vertices) > 0:
                fig.add_trace(go.Scatter3d(
                    x=vertices[:, 0],
                    y=vertices[:, 1],
                    z=vertices[:, 2],
                    mode='markers',
                    marker=dict(size=2, color='gray'),
                    name='Вершины'
                ))
            
            # Ребра
            if edges is not None and len(edges) > 0 and vertices is not None:
                for edge in edges[:100]:  # Ограничиваем для производительности
                    v1, v2 = edge
                    if v1 < len(vertices) and v2 < len(vertices):
                        fig.add_trace(go.Scatter3d(
                            x=[vertices[v1][0], vertices[v2][0]],
                            y=[vertices[v1][1], vertices[v2][1]],
                            z=[vertices[v1][2], vertices[v2][2]],
                            mode='lines',
                            line=dict(color='gray', width=1),
                            showlegend=False
                        ))
            
            # Кольца
            for i, ring in enumerate(self.rings[:50]):  # Ограничиваем количество
                center = ring.position
                normal = ring.orientation
                radius = ring.radius
                
                # Два перпендикулярных вектора
                if abs(normal[0]) < 0.9:
                    v1 = np.cross(normal, np.array([1, 0, 0]))
                else:
                    v1 = np.cross(normal, np.array([0, 1, 0]))
                v1 = v1 / np.linalg.norm(v1)
                v2 = np.cross(normal, v1)
                
                # Точки окружности
                theta = np.linspace(0, 2 * np.pi, 20)
                circle_points = []
                for t in theta:
                    point = center + radius * (np.cos(t) * v1 + np.sin(t) * v2)
                    circle_points.append(point)
                circle_points = np.array(circle_points)
                
                fig.add_trace(go.Scatter3d(
                    x=circle_points[:, 0],
                    y=circle_points[:, 1],
                    z=circle_points[:, 2],
                    mode='lines',
                    line=dict(color='blue', width=2),
                    name=f'Кольцо {i}' if i == 0 else None,
                    showlegend=i == 0
                ))
            
            fig.update_layout(
                title=f'Система колец ({len(self.rings)} колец)',
                scene=dict(
                    xaxis_title='X (м)',
                    yaxis_title='Y (м)',
                    zaxis_title='Z (м)'
                )
            )
            
            fig.show()
            
        except ImportError:
            print("Для визуализации установите plotly: pip install plotly")
            print(f"Колец: {len(self.rings)}")
    
    def __repr__(self):
        return f"RingSystem(rings={len(self.rings)})"