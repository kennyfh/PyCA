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
        self.surface = surface
        self.generateGrid()
        self.running= False
        pygame.display.update()

    def generateGrid(self):
        width,height = self.surface.get_size()
        num_points = 900
        points = np.zeros([num_points, 2], np.uint16)
        ## NOTA: Si esto no funciona , cambiar de orden los valores 800 y 600 entre ellos
        # Genera un array de 900 elementos aleatorios entre 0 y width
        points[:, 0] = np.random.randint(0, width, size=num_points)
        # Genera un array de 900 elementos aleatorios entre 0 y height
        points[:, 1] = np.random.randint(0, height, size=num_points)

        vor = Voronoi(points)
        for region in vor.regions:
            if not -1 in region:
                polygon = [vor.vertices[i] for i in region]
                if len(polygon) > 0:
                    pygame.draw.polygon(self.surface, (255, 255, 255), polygon, 1)

        


    def update(self):
        return super().update()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        if self.running:
                self.update()
                pygame.display.update()

    def run(self):
        # Main loop
        while True:
            self.handle_events()
            #self.surface.fill(COLOR_GRID)
            
            pygame.display.update()

            time.sleep(0.001)
    
#window = pygame.display.set_mode((800, 600))
#stage = VoronoiGrid(window)
#stage.generateGrid()
#stage.run()