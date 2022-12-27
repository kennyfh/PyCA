import time
import pygame
import numpy as np
from stage import Stage

COLOR_BG = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_DIE_NEXT = (170, 170, 170)
COLOR_ALIVE_NEXT = (255, 255, 255)

pygame.init()
pygame.display.set_caption("conway's game of life")


class Square(Stage):
    def __init__(self, surface):
        # Set the surface to draw the stage on
        self.surface = surface
        
        # Set the background color
        self.surface.fill(COLOR_GRID)

        # Set the size of the stage
        self.size = surface.get_size()

        # Set the size of the grid
        self.grid_size = (60, 80)

        # Create the grid
        self.grid = np.zeros((self.grid_size[0], self.grid_size[1]))
        
        # Update the screen
        self.update()
        pygame.display.update()

        # Set the running flag to False
        self.running = False
        
    def update(self):
        updated_cells = np.zeros((self.grid.shape[0], self.grid.shape[1]))

        for row, col in np.ndindex(self.grid.shape):
            alive = np.sum(self.grid[row-1:row+2, col-1:col+2]) - self.grid[row, col]
            color = COLOR_BG if self.grid[row, col] == 0 else COLOR_ALIVE_NEXT

            if self.grid[row, col] == 1:
                if alive < 2 or alive > 3:
                    color = COLOR_DIE_NEXT
                elif 2 <= alive <= 3:
                    updated_cells[row, col] = 1
                    color = COLOR_ALIVE_NEXT
            else:
                if alive == 3:
                    updated_cells[row, col] = 1
                    color = COLOR_ALIVE_NEXT

            pygame.draw.rect(self.surface, color, (col * 10, row * 10, 10 - 1, 10 - 1))

        self.grid = updated_cells
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.running = not self.running
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // 10, pos[0] // 10
                self.grid[row, col] = 1 # - self.grid[row, col]  # Toggle between 0 and 1
                # color = COLOR_BG if self.grid[row, col] == 0 else COLOR_ALIVE_NEXT
                color = COLOR_ALIVE_NEXT
                pygame.draw.rect(self.surface, color, (col * 10, row * 10, 10 - 1, 10 - 1))
                pygame.display.update()
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = pos[1] // 10, pos[0] // 10
                self.grid[row, col] = 0 # - self.grid[row, col]  # Toggle between 0 and 1
                # color = COLOR_BG if self.grid[row, col] == 0 else COLOR_ALIVE_NEXT
                color = COLOR_BG
                pygame.draw.rect(self.surface, color, (col * 10, row * 10, 10 - 1, 10 - 1))
                pygame.display.update()
        if self.running:
                self.update()
                pygame.display.update()

    def run(self):
        # Main loop
        while True:
            self.handle_events()
            #self.surface.fill(COLOR_GRID)
            if self.running:
                self.update()
                pygame.display.update()

            time.sleep(0.001)

# Prueba de que funciona correctamente
#window = pygame.display.set_mode((800, 600))
#stage = Square(window)
#stage.run()