"""
Clase padre donde se van a crear los 3 escenarios: Cuadrático, Hexagonal y Voronoi
"""
class Stage:
    def __init__(self, surface):
        self.surface = surface

    def update(self):
        pass

    def handle_events(self):
        pass

    def run(self):
        pass
