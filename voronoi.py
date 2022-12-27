import pygame
import numpy as np
from scipy.spatial import Voronoi
import time
from stage import Stage


"""
VORONOI : https://en.wikipedia.org/wiki/Voronoi_diagram
"""

pygame.init()

class VoronoiGrid(Stage):
    def __init__(self, surface):
        super().__init__(surface)

    def generateDiagram(self):
        points = np.zeros([900, 2], np.uint16)
        ## NOTA: Si esto no funciona , cambiar de orden los valores 800 y 600 entre ellos
    
        # Genera un array de 900 elementos aleatorios entre 0 y 1600
        points[:, 0] = np.random.randint(0, 800, size=900)

        # Genera un array de 900 elementos aleatorios entre 0 y 900
        points[:, 1] = np.random.randint(0, 600, size=900)

        # Devolvemos Voronoi creado
        return Voronoi(points)

    def draw_voronoi(self,pygame_surface):
        # generate voronoi diagram
        vor = self.generateDiagram()

        # draw all the edges
        for indx_pair in vor.ridge_vertices:
            if -1 not in indx_pair:

                start_pos = vor.vertices[indx_pair[0]]
                end_pos = vor.vertices[indx_pair[1]]
                pygame.draw.line(pygame_surface, (0, 0, 0), start_pos, end_pos)


    def update(self):
        return super().update()
    
    def handle_events(self):
        return super().handle_events()

    def run(self):
        # Main loop
        while True:
            self.handle_events()
            self.draw_voronoi(self.surface)
            time.sleep(0.001)
    
window = pygame.display.set_mode((800, 600))
stage = VoronoiGrid(window)
stage.run()