#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Module: Voronoi
# Created By  : TEODORO JIMÉNEZ LEPE
#               KENNY JESÚS FLORES HUAMÁN
# version ='1.0'
# ---------------------------------------------------------------------------
# This file contains a class to generate Voronoi Grid
# ---------------------------------------------------------------------------

# IMPORTS
# Standard library imports
import time
import os 

# Third-party imports
import pygame
import numpy as np
from scipy.spatial import Voronoi
from typing import List, Tuple

# Own local imports
from stage import Stage
from pixel_perfect_polygon_hitbox import ordered_vertices, is_in_polygon

Lx = 800
Ly = 600

N = 5

COLOR_BLACK = (10, 10, 10)
COLOR_WHITE = (255, 255, 255)
COLOR_LOAD = (106,13,173)
COLOR_GRID = (60,60,60)


# Start pygame
pygame.init()

# Class for the voronoi stage:


class VoronoiGrid(Stage):
    """Initialize the voronoi stage with the given surface and parameters.

    Args:
        surface (pygame.Surface): The surface on which the stage will be drawn.
        L (int, optional): The size of the cells in the stage. Default is 10.
        COLOR_JUST_BORN (Tuple[int, int, int], optional): The color of cells that are born in a given step. Default is (0, 255, 0).
        COLOR_SURVIVED (Tuple[int, int, int], optional): The color of cells that survive to the next step. Default is (255, 0, 0).
        alive_neighbours_to_be_born (List[int], optional): A list of the number of alive neighbors required for a cell to be born. Default is [3].
        alive_neighbours_to_survive (List[int], optional): A list of the number of alive neighbors required for a cell to survive. Default is [2, 3].
        initial_alive_probability (float, optional): The probability that a cell will be initially alive. Default is 0.
    """

    def __init__(self,
                 surface: pygame.Surface,
                 L: int = 6,
                 COLOR_JUST_BORN: Tuple[int, int, int] = (0, 255, 0),
                 COLOR_SURVIVED: Tuple[int, int, int] = (255, 0, 0),
                 alive_neighbours_to_be_born: List[int] = [1,2,3,4,5,6,7,8,9],
                 alive_neighbours_to_survive: List[int] = [1,2,3,4,5,6,7,8,9],
                 initial_alive_probability: int = 0.0) -> None:
        
        # Set the loading flag to True in order to make initial calculations without event handling issues
        self.loading = True
        
        # Set the surface to draw the stage on
        super().__init__(surface, L, COLOR_JUST_BORN, COLOR_SURVIVED,
                         alive_neighbours_to_be_born, alive_neighbours_to_survive, initial_alive_probability)
        
        # Processing window caption:
        birth_string = [str(x) for x in self.alive_neighbours_to_be_born]
        survival_string = [str(x) for x in self.alive_neighbours_to_survive]
        self.rule = 'B'+"".join(birth_string)+'/S'+"".join(survival_string)
        caption = self.rule + 'in Voronoi grid'
        pygame.display.set_caption(caption) 
        
        # Set the size of the grid
        number_of_seeds = np.floor((Lx*Ly/self.L**2)).astype(int)
        points = np.zeros([number_of_seeds, 2])
        points[:, 0] = np.random.randint(0, Lx, size=number_of_seeds)
        points[:, 1] = np.random.randint(0, Ly, size=number_of_seeds)
        
        # Set the background color
        self.surface.fill(COLOR_GRID)
        # Set the title of the window 
        pygame.display.update()
        # Create a font object
        font = pygame.font.Font(None, 36)        
        # Render the text
        text = font.render('LOADING ' + "%0.0e" % number_of_seeds + \
                           ' VORONOI REGIONS ...', 1, (255, 255, 255))        
        # Get the size of the text
        text_rect = text.get_rect()        
        # Set the position of the text
        text_rect.center = (Lx // 2, Ly // 2)
        # Draw the text on the screen
        self.surface.blit(text, text_rect)
        # Update the display
        pygame.display.update()
        
        # Set the size of the stage
        self.size = surface.get_size()

        self.number_of_regions = 0
        vor = Voronoi(points)
        for region in vor.regions:
            if not -1 in region:
                if len([vor.vertices[vertex] for vertex in region]) > 2:
                    self.number_of_regions = self.number_of_regions + 1
        self.grid_size = self.number_of_regions

        # Storage rectangular hitbox for every hexagon.
        self.RectHitbox = np.ndarray((self.number_of_regions), dtype=object)

        # Set the background color
        self.surface.fill(COLOR_GRID)

        # Labels for voronoi vertices of each voronoi region
        self.voronoi_vertices_labels = np.ndarray(
            (self.number_of_regions), dtype=object)

        # Vertices for voronoi regions
        self.voronoi_vertices = np.ndarray(
            (self.number_of_regions), dtype=object)
        cell = 0
        scipy_label = 0
        for region in vor.regions:
            if not -1 in region:
                vertices = [vor.vertices[vertex] for vertex in region]
                if len(vertices) > 2:
                    self.voronoi_vertices_labels[cell] = region
                    for i in range(len(vertices)):
                        vertices[i] = tuple(vertices[i])
                    self.voronoi_vertices[cell] = ordered_vertices(vertices)
                    cell = cell + 1
            scipy_label = scipy_label + 1

        # Update screen:
        # pygame.display.flip()

        # Toggle between all dead and random initial state
        self.initial_alive_probability = initial_alive_probability  # 0 to 1

        # Color to fill the hexagon (changes after every step)
        self.color = np.ndarray((self.number_of_regions), dtype=object)

        # Create and display initial state grid
        self.grid = np.zeros(self.number_of_regions)
        
        # Establish square 100x100 pixels^2 sections to classify voronoi regions.
        # This will make it easier to determine neighbourhood relationship.
        
        # Every voronoi region belongs to one or more sections (48 total) of the grid:
        self.grid_section = np.ndarray((self.number_of_regions), dtype=object)
        
        # Every section contains a certain number of voronoi regions
        self.section_cells = np.ndarray(int(Lx*Ly/N**2), dtype=object)
        
        for cell in range(self.number_of_regions): 
            self.grid_section[cell] = []
        
        for section in range(int(Lx*Ly/N**2)): 
            self.section_cells[section] = []
        
        for cell in range(self.number_of_regions):
            
            if np.random.rand() < self.initial_alive_probability:  # Threshold for initial alive state
                self.grid[cell] = 1  # Tag alive cells with 1
                self.color[cell] = COLOR_WHITE  # Color them white
            else:
                self.grid[cell] = 0  # Tag dead cells with 0
                self.color[cell] = COLOR_BLACK  # Color them white
            # Display on hexagons on screen ans storage their rectangular hitbox:
            self.RectHitbox[cell] = pygame.draw.polygon(
                self.surface, self.color[cell], self.voronoi_vertices[cell])
            pygame.draw.polygon(self.surface, COLOR_GRID,
                                self.voronoi_vertices[cell], 1)
            if cell % 10 == 0:
                pygame.display.update()
                
            for vertex in self.voronoi_vertices[cell]:
                x_section = vertex[0]//N
                if x_section > (Lx/N)-1:
                    x_section = (Lx/N)-1
                if x_section < 0:
                    x_section = 0   
                y_section = vertex[1]//N
                if y_section > (Ly/N)-1:
                    y_section = (Ly/N)-1
                if y_section < 0:
                    y_section = 0
                index_section = int(y_section*(Lx/N) + x_section)
                if index_section not in self.grid_section[cell]:
                    self.grid_section[cell].append(index_section)
                    self.section_cells[index_section].append(cell)
        pygame.display.update()
        
        self.neighbours = np.ndarray((self.number_of_regions), dtype=object)
        for cell in range(self.number_of_regions):
            self.neighbours[cell] = []
        for cell in range(self.number_of_regions):
            for section in self.grid_section[cell]:
                for other_cell in self.section_cells[section]:
                    for vertex_label in self.voronoi_vertices_labels[cell]:
                        if vertex_label in self.voronoi_vertices_labels[other_cell] and \
                                other_cell not in self.neighbours[cell] and \
                                cell not in self.neighbours[other_cell] and other_cell != cell:
                            self.neighbours[cell].append(other_cell)
                            self.neighbours[other_cell].append(cell)
                            

        # Set the running flag to False
        self.running = False
        
        # Set the recording flag to False
        self.recording = False
        
        # Set the loading flag to false 
        self.loading = False
        
        self.change_caption()

    # Function to calculate the number of alive neighbours
    def alive_voronoi(self, cell: int) -> int:
        """
        Calculate the number of alive neighbours for a given cell.

        Args:
            cell (int): Index of the cell in the grid.

        Returns:
            int: Number of alive neighbours.
        """
        alive_neighbours = 0
        for neighbour in self.neighbours[cell]:
            alive_neighbours = alive_neighbours + self.grid[neighbour]
        return alive_neighbours

    def change_caption(self) -> None:
        # Processing window caption:
        birth_string = [str(x) for x in self.alive_neighbours_to_be_born]
        survival_string = [str(x) for x in self.alive_neighbours_to_survive]
        self.rule = 'B'+"".join(birth_string)+'S'+"".join(survival_string)
        if self.recording:
            caption = 'B'+"".join(birth_string)+'/S'+"".join(survival_string)+' ' + 'in Voronoi grid (RECORDING SCREEN)' 
        else:
            caption = 'B'+"".join(birth_string)+'/S'+"".join(survival_string)+' ' + 'in Voronoi grid' 
        pygame.display.set_caption(caption) 
    
    def update(self) -> None:
        """
         Update state of the cellular automata and the screen
        """
        # Processing window caption:
        self.change_caption()
        
        # Initially asume every cell is dead (0)
        updated_cells = np.zeros(self.number_of_regions)

        for cell in range(self.number_of_regions):
            # Calculate the number of alive neighbours for every cell
            alive_neighbours = self.alive_voronoi(cell)

            if self.grid[cell] == 1:
                # Check if the conditions for birth are met.
                # Updated grid and color are changed accordingly.
                if alive_neighbours in self.alive_neighbours_to_survive:
                    updated_cells[cell] = 1
                    self.color[cell] = self.COLOR_SURVIVED
                else:
                    self.color[cell] = COLOR_BLACK
                # Check if the conditions for survival are met.
                # Updated grid and color are changed accordingly.
            else:
                if alive_neighbours in self.alive_neighbours_to_be_born:
                    updated_cells[cell] = 1
                    self.color[cell] = self.COLOR_JUST_BORN
                else:
                    self.color[cell] = COLOR_BLACK
                # Note that COLOR_SURVIVED and COLOR_JUST_BORN both mean "alive",
                # but specify the previous state of the cell (alive and dead
                # respectively).

            # Draw updated hexagons
            pygame.draw.polygon(
                self.surface, self.color[cell], self.voronoi_vertices[cell])
            pygame.draw.polygon(self.surface, COLOR_GRID,
                                self.voronoi_vertices[cell], 1)
        # Save screen in a folder 
        if self.recording == True:
            newpath = "saved_images\\" + "Voronoi" + self.rule.replace('/','_')
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            pygame.image.save(self.surface, "saved_images/"+ "Voronoi" + self.rule.replace('/','_') +"/"+str(pygame.time.get_ticks())+".png")

        # Show updates on screen
        pygame.display.update()
        # Storage updated grid state in main grid
        self.grid = updated_cells

    # Handle pygame events: mainly user instructions
    def handle_events(self) -> None:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN and not self.loading:  # Check if any key gets pressed down
                if event.key == pygame.K_SPACE:  # Check if spacebar gets pressed down
                    self.running = not self.running  # Pause and resume button
                elif event.key == pygame.K_RIGHT:  # Check if right arrow gets pressed down
                    # This key allows single step update in order to
                    # watch evolution in detail:
                    self.running = False
                    self.update()
                    pygame.display.update()
                elif event.key == pygame.K_DOWN:  # Check if down arrow gets pressed down
                    self.running = False
                    for cell in range(self.number_of_regions):
                        self.grid[cell] = 0  # Kill every cell
                        self.color[cell] = COLOR_BLACK
                        pygame.draw.polygon(
                            self.surface, self.color[cell], self.voronoi_vertices[cell])
                    self.update()
                elif event.key == pygame.K_s: # Check if s key gets pressed down
                    self.recording = not self.recording
                    self.change_caption()

            if pygame.mouse.get_pressed()[0]:  # True if left-click
                pos = pygame.mouse.get_pos()  # Get mouse pointer position
                for cell in range(self.number_of_regions):
                    # Check if user has clicked on any hexagon hitbox:
                    if self.RectHitbox[cell].collidepoint(pos):
                        if is_in_polygon(pos, self.voronoi_vertices[cell]):
                            self.grid[cell] = 1  # Cell becomes alive
                            self.color[cell] = COLOR_WHITE  # Thus, gets white
                            # Draw new hexagon:
                            pygame.draw.polygon(
                                self.surface, self.color[cell], self.voronoi_vertices[cell])
                            pygame.draw.polygon(
                                self.surface, COLOR_GRID, self.voronoi_vertices[cell], 1)
                            # Show it on screen:
                            pygame.display.update()
            elif pygame.mouse.get_pressed()[2]:  # True if right-click
                pos = pygame.mouse.get_pos()  # Get mouse pointer position
                for cell in range(self.number_of_regions):
                    # Check if user has clicked on any hexagon hitbox:
                    if self.RectHitbox[cell].collidepoint(pos):
                        if is_in_polygon(pos, self.voronoi_vertices[cell]):
                            self.grid[cell] = 0  # Cell is killed
                            self.color[cell] = COLOR_BLACK  # Thus, gets black
                            # Draw new hexagon:
                            pygame.draw.polygon(
                                self.surface, self.color[cell], self.voronoi_vertices[cell])
                            pygame.draw.polygon(
                                self.surface, COLOR_GRID, self.voronoi_vertices[cell], 1)
                            # Show it on screen:
                            pygame.display.update()
            # Analogous action that prints number of alive neighbours on terminal.
            # This is mainly implemented for troubleshooting.
            # Central mouse button (mouse wheel)
            elif pygame.mouse.get_pressed()[1]:
                pos = pygame.mouse.get_pos()
                for cell in np.ndindex(self.grid_size):
                    if self.RectHitbox[cell].collidepoint(pos):
                        if is_in_polygon(pos, self.voronoi_vertices[cell]):
                            if self.grid[cell] == 1:
                                print('This cell {} is alive'.format(cell))
                            else:
                                print('This cell {} is dead'.format(cell))
                            print('Alive neighbours: {}'.format(self.alive_voronoi(cell)))
                            
    def run(self) -> None:
        # Main loop
        while True:
            self.handle_events()
            # self.surface.fill(COLOR_GRID)
            if self.running:
                # time.sleep(self.delay)
                self.update()

# # Check this script independetly: (do not uncomment if running main.py)
# window = pygame.display.set_mode((800, 600))
# stage = VoronoiGrid(window)
# stage.run()
