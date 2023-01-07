#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Module: Hexagon
# Created By  : TEODORO JIMÉNEZ LEPE
#               KENNY JESÚS FLORES HUAMÁN
# version ='1.0'
# ---------------------------------------------------------------------------
# This file contains a class to generate Hexagon Grid
# ---------------------------------------------------------------------------

# IMPORTS
# Standard library imports
import time
import os 

# Third-party imports
import pygame
import numpy as np
from typing import List, Tuple

# Own local imports
from stage import Stage
Lx = 800
Ly = 600

COLOR_BLACK = (10, 10, 10)
COLOR_WHITE = (255, 255, 255)
COLOR_GRID = (40, 40, 40)

# Start pygame
pygame.init()

# Class for the hexagonal stage:


class Hexagon(Stage):
    """
    A class for generating and visualizing a cellular automata stage in the form of a hexagonal grid.

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
                 L: int = 5,
                 COLOR_JUST_BORN: Tuple[int, int, int] = (0, 255, 0),
                 COLOR_SURVIVED: Tuple[int, int, int] = (255, 0, 0),
                 alive_neighbours_to_be_born: List[int] = [2],
                 alive_neighbours_to_survive: List[int] = [3, 4],
                 initial_alive_probability: float = 0) -> None:
        # Set the surface to draw the stage on
        super().__init__(surface, L, COLOR_JUST_BORN, COLOR_SURVIVED,
                         alive_neighbours_to_be_born, alive_neighbours_to_survive, initial_alive_probability)

        # Set the background color
        self.surface.fill(COLOR_GRID)
        
        # Set the size of the stage
        self.size = surface.get_size()

        # Calculations to adapt grid to the screen according to Lx, Ly and L:
        effective_width = np.sqrt(3)*self.L + 3
        effective_height = self.L + 2
        nx = np.floor(Lx/effective_width-1/2).astype(int)
        ny = np.floor((2/3)*(Ly/effective_height - 0.5)).astype(int)
        if ny % 2 != 0:
            ny = ny - 1

        # Set the size of the grid
        self.grid_size = (nx, ny)

        # Toggle between all dead and random initial state
        self.initial_alive_probability = initial_alive_probability  # 0 to 1

        # Color to fill the hexagon (changes after every step)
        self.color = np.ndarray((nx, ny), dtype=object)

        # Storage rectangular hitbox for every hexagon.
        self.RectHitbox = np.ndarray((nx, ny), dtype=object)

        # Create and display initial state grid
        self.grid = np.zeros((nx, ny))
        self.hexagon_vertices = np.ndarray((nx, ny), dtype=object)
        for col, row in np.ndindex(self.grid.shape):
            # Get vertices of every hexagon before running
            self.hexagon_vertices[col, row] = self.calculate_hexagon_vertices(
                col, row, self.L)
            if np.random.rand() < initial_alive_probability:  # Threshold for initial alive state
                self.grid[col, row] = 1  # Tag alive cells with 1
                self.color[col, row] = COLOR_WHITE  # Color them white
            else:
                self.grid[col, row] = 0  # Tag dead cells with 0
                self.color[col, row] = COLOR_BLACK  # Color them white
            # Display on hexagons on screen ans storage their rectangular hitbox:
            self.RectHitbox[col, row] = pygame.draw.polygon(
                self.surface, self.color[col, row], self.hexagon_vertices[col, row])
        # Update screen:
        pygame.display.update()

        # Set the running flag to False
        self.running = False
        
        # Set the recording flag to False
        self.recording = False
        
        # Processing window caption:
        self.change_caption()
        
        # Attribute to communicate with main log
        self.log_state = 0
        
        # Message for global log
        self.message = None
    def log(self, message):
        self.message = message
        self.log_state = self.log_state + 1
        
    def screenshot(self) -> None:
        # Save screen in a folder 
        if self.recording == True:
            newpath = "saved_images\\" + "hexagon" + self.rule.replace('/','_')
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            pygame.image.save(self.surface, "saved_images/"+ "hexagon" + self.rule.replace('/','_') +"/"+str(pygame.time.get_ticks())+".png")
        
        
    # Calculate the coordinates of the hexagon corresponding to (col,row) coordinates.
    # Takes the length of the side of the hexagons and the position of the (0,0) one as
    # parameters.
    def calculate_hexagon_vertices(self, col: int, row: int, side_length: int) -> List[Tuple[int, int]]:
        """
            Calculate the coordinates of the hexagon corresponding to (col,row) coordinates.
            Takes the length of the side of the hexagons and the position of the (0,0) one as parameters.

            Args:
                col : int
                    Column index of the hexagon.
                row : int
                    Row index of the hexagon.
                side_length : float
                    Length of the side of the hexagon.

            Returns:
                vertices : List of tuples containing the coordinates of the vertices of the hexagon in the form (x, y).
        """

        # Coordinates for the top-left hexagon north-west vertex
        grid_topleft = np.array([3, self.L/2])

        width_hex = side_length*np.sqrt(3)  # Width of an hexagon

        # Space between hexagon in order to acquire grid appearance:
        step_x = width_hex + 3
        step_y = side_length*1.5 + 3

        # Vertices coordinates:
        vertex = np.empty((6), dtype=object)
        vertex[0] = grid_topleft + np.array([step_x*col, step_y*row])
        vertex[1] = grid_topleft + \
            np.array([step_x*col, step_y*row+side_length])
        vertex[2] = grid_topleft + \
            np.array([step_x*col+0.5*np.sqrt(3)*side_length,
                     step_y*row+1.5*side_length])
        vertex[3] = grid_topleft + \
            np.array([step_x*col+np.sqrt(3)*side_length, step_y*row+side_length])
        vertex[4] = grid_topleft + \
            np.array([step_x*col+np.sqrt(3)*side_length, step_y*row])
        vertex[5] = grid_topleft + \
            np.array([step_x*col+0.5*np.sqrt(3)*side_length,
                     step_y*row-0.5*side_length])

        # There is an offset between even row hexagons and odd row hexagons:
        if row % 2 == 1:
            for i in range(len(vertex)):
                vertex[i] = vertex[i] + np.array([step_x/2, 0])

        # Output array of vertices as a list of tuples:
        vertices = []
        for i in range(6):
            vertices.append(tuple(vertex[i]))
        return vertices

    # Function to calculate the number of alive neighbours
    def alive_hexagon(self, cell: np.ndarray, x: int, y: int) -> int:
        """Calculate the number of alive neighbours for a cell in a hexagonal grid.

        Args:
            cell (np.ndarray): The current state of the grid.
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.

        Returns:
            int: The number of alive neighbours.
        """
        # Set periodic boundary conditions (toroidal shape)
        x_pre = (x-1) % cell.shape[0]
        x_post = (x+1) % cell.shape[0]
        y_pre = (y-1) % cell.shape[1]
        y_post = (y+1) % cell.shape[1]

        # In order to storage this information in a matrix (nx, ny),
        # we need to distinguish between odd and even rows. This is due to
        # the horizontal offset between them.
        if y % 2 == 0:
            alive_neighbours = cell[x_pre, y] + cell[x_post, y]   \
                + cell[x_pre, y_pre] + cell[x, y_pre] \
                + cell[x_pre, y_post] + cell[x, y_post] #+ cell[x,y]
        else:
            alive_neighbours = cell[x_pre, y] + cell[x_post, y]   \
                + cell[x, y_pre] + cell[x_post, y_pre] \
                + cell[x, y_post] + cell[x_post, y_post] #+ cell[x,y]

        return int(alive_neighbours)
    
    def change_caption(self) -> None: 
        # Processing window caption:
        birth_string = [str(x) for x in self.alive_neighbours_to_be_born]
        survival_string = [str(x) for x in self.alive_neighbours_to_survive]
        self.rule = 'B'+"".join(birth_string)+'S'+"".join(survival_string)
        if self.recording:
            caption = 'B'+"".join(birth_string)+'/S'+"".join(survival_string)+" "+'in hexagonal grid (RECORDING SCREEN)' 
        else:
            caption = 'B'+"".join(birth_string)+'/S'+"".join(survival_string)+" "+'in hexagonal grid' 
            
        pygame.display.set_caption(caption)

    # Update state of the cellular automata and the screen
    def update(self) -> None:
        # Processing window caption:
        self.change_caption()
        
        # Initially asume every cell is dead (0)
        updated_cells = np.zeros((self.grid.shape[0], self.grid.shape[1]))

        for col, row in np.ndindex(self.grid.shape):
            # Calculate the number of alive neighbours for every cell
            alive_neighbours = self.alive_hexagon(self.grid, col, row)

            if self.grid[col, row] == 1:
                # Check if the conditions for birth are met.
                # Updated grid and color are changed accordingly.
                if alive_neighbours in self.alive_neighbours_to_survive:
                    updated_cells[col, row] = 1
                    self.color[col, row] = self.COLOR_SURVIVED
                else:
                    self.color[col, row] = COLOR_BLACK
                # Check if the conditions for survival are met.
                # Updated grid and color are changed accordingly.
            else:
                if alive_neighbours in self.alive_neighbours_to_be_born:
                    updated_cells[col, row] = 1
                    self.color[col, row] = self.COLOR_JUST_BORN
                else:
                    self.color[col, row] = COLOR_BLACK
                # Note that self.COLOR_SURVIVED and self.COLOR_JUST_BORN both mean "alive",
                # but specify the previous state of the cell (alive and dead
                # respectively).

            # Draw updated hexagons
            pygame.draw.polygon(
                self.surface, self.color[col, row], self.hexagon_vertices[col, row])
        
        # Save screen in a folder 
<<<<<<< HEAD
        self.screenshot()
=======
        if self.recording:
            newpath = "saved_images\\" + "hexagon" + self.rule.replace('/','_')
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            pygame.image.save(self.surface, "saved_images/"+ "hexagon" + self.rule.replace('/','_') +"/"+str(pygame.time.get_ticks())+".png")
>>>>>>> 01c8d60bac1f4f0a462874a09914cecae4aacc4a
        
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
            elif event.type == pygame.KEYDOWN:  # Check if any key gets pressed down
                if event.key == pygame.K_SPACE:  # Check if spacebar gets pressed down
                    self.running = not self.running  # Pause and resume button
                elif event.key == pygame.K_RIGHT:  # Check if right arrow gets pressed down
                    # This key allows single step update in order to
                    # watch evolution in detail:
                    self.running = False
                    self.update()
                elif event.key == pygame.K_DOWN:  # Check if down arrow gets pressed down
                    self.running = False
                    for col, row in np.ndindex(self.grid.shape):
                        self.grid[col, row] = 0  # Kill every cell
                        self.color[col, row] = COLOR_BLACK
                        pygame.draw.polygon(
                            self.surface, self.color[col, row], self.hexagon_vertices[col, row])
                    pygame.display.update()
                elif event.key == pygame.K_s: # Check if s key gets pressed down
                    self.recording = not self.recording
                    self.change_caption()
                    if self.recording:
                        self.screenshot()
                    
            if pygame.mouse.get_pressed()[0]:  # True if left-click
                pos = pygame.mouse.get_pos()  # Get mouse pointer position
                for col, row in np.ndindex(self.grid_size):
                    # Check if user has clicked on any hexagon hitbox:
                    if self.RectHitbox[col, row].collidepoint(pos):
                        self.grid[col, row] = 1  # Cell becomes alive
                        self.color[col, row] = COLOR_WHITE  # Thus, gets white
                        # Draw new hexagon:
                        pygame.draw.polygon(self.surface, self.color[col, row], self.hexagon_vertices[col, row])
                        # Show it on screen:
                        pygame.display.update()
            elif pygame.mouse.get_pressed()[2]:  # True if right-click
                pos = pygame.mouse.get_pos()  # Get mouse pointer position
                for col, row in np.ndindex(self.grid_size):
                    # Check if user has clicked on any hexagon hitbox:
                    if self.RectHitbox[col, row].collidepoint(pos):
                        self.grid[col, row] = 0  # Cell is killed
                        self.color[col, row] = COLOR_BLACK  # Thus, gets black
                        # Draw new hexagon:
                        pygame.draw.polygon(self.surface, self.color[col, row], self.hexagon_vertices[col, row])
                        # Show it on screen:
                        pygame.display.update()
            # Analogous action that prints number of alive neighbours on terminal.
            # This is mainly implemented for troubleshooting.
            # Central mouse button (mouse wheel)
            elif pygame.mouse.get_pressed()[1]:
                pos = pygame.mouse.get_pos()
                for col, row in np.ndindex(self.grid_size):
                    if self.RectHitbox[col, row].collidepoint(pos):
                        if self.grid[col, row] == 1:
                            state = 'alive'
                        else:
                            state = 'dead'
                        self.log('This cell {} is'.format((col, row))+ ' ' + state +'. Alive neighbours: {}'.format(
                            self.alive_hexagon(self.grid, col, row)))

    def run(self) -> None:
        # Main loop
        while True:
            self.handle_events()
            #self.surface.fill(COLOR_GRID)
            if self.running:
                time.sleep(0.01)
                self.update()

## Check this script independetly: (do not uncomment if running main.py)
# window = pygame.display.set_mode((800, 600))
# stage = Hexagon(window, L = 5.5)
# stage.run()
