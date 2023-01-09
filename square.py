#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Module: Square
# Created By  : TEODORO JIMÉNEZ LEPE
#               KENNY JESÚS FLORES HUAMÁN
# version ='1.0'
# ---------------------------------------------------------------------------
# This file contains a class to generate Square Grid
# ---------------------------------------------------------------------------

# IMPORTS
# Standard library imports
import time
import os

# Third-party imports
import pygame
import numpy as np
from typing import List, Tuple
import imageio

# Own local imports
from stage import Stage

Lx = 800
Ly = 600

COLOR_BLACK = (10, 10, 10)
COLOR_WHITE = (255, 255, 255)
COLOR_GRID = (40, 40, 40)

# Start pygame
pygame.init()


class Square(Stage):
    """
    A class for generating and visualizing a cellular automata stage in the form of a square grid.

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
                 L: int = 10,
                 COLOR_JUST_BORN: Tuple[int, int, int] = (0, 255, 0),
                 COLOR_SURVIVED: Tuple[int, int, int] = (255, 0, 0),
                 alive_neighbours_to_be_born: List[int] = [3],
                 alive_neighbours_to_survive: List[int] = [2, 3],
                 initial_alive_probability: float = 0.0) -> None:

        # Set the surface to draw the stage on
        super().__init__(surface, L, COLOR_JUST_BORN, COLOR_SURVIVED,
                         alive_neighbours_to_be_born, alive_neighbours_to_survive, initial_alive_probability)

        # Set the background color
        self.surface.fill(COLOR_GRID)

        # Set the size of the stage
        self.size = surface.get_size()

        # Calculations to adapt grid to the screen according to Lx, Ly and L:
        effective_width = self.L
        effective_height = self.L
        nx = np.floor(Lx/effective_width).astype(int)
        ny = np.floor(Ly/effective_height).astype(int)

        # Set the size of the grid
        self.grid_size = (nx, ny)

        # Toggle between all dead and random initial state
        self.initial_alive_probability = self.initial_alive_probability  # 0 to 1

        # Color to fill the hexagon (changes after every step)
        self.color = np.ndarray((nx, ny), dtype=object)

        # Storage rectangular hitbox for every hexagon.
        self.RectHitbox = np.ndarray((nx, ny), dtype=object)

        # Stage Name
        self.stage_name = "Square"

        # Create and display initial state grid
        self.grid = np.zeros((nx, ny))
        for col, row in np.ndindex(self.grid.shape):
            if np.random.rand() < self.initial_alive_probability:  # Threshold for initial alive state
                self.grid[col, row] = 1  # Tag alive cells with 1
                self.color[col, row] = COLOR_WHITE  # Color them white
            else:
                self.grid[col, row] = 0  # Tag dead cells with 0
                self.color[col, row] = COLOR_BLACK  # Color them white
            # Display on hexagons on screen ans storage their rectangular hitbox:
            self.RectHitbox[col, row] = pygame.draw.rect(
                self.surface, self.color[col, row], (col * self.L, row * self.L, self.L - 1, self.L - 1))
        # Update screen:
        pygame.display.update()
        self.change_caption()

    # Function to calculate the number of alive neighbours
    def alive_square(self, cell: np.ndarray, x: int, y: int) -> int:
        """Calculate the number of alive neighbours for a cell in a square grid.

        Args:
            cell (np.ndarray): 2D array representing the current state of the grid.
            x (int): X coordinate of the cell being checked.
            y (int): Y coordinate of the cell being checked.

        Returns:
            int: Number of alive neighbours for the cell.
        """
        # Set periodic boundary conditions (toroidal shape)
        x_pre = (x-1) % cell.shape[0]
        x_post = (x+1) % cell.shape[0]
        y_pre = (y-1) % cell.shape[1]
        y_post = (y+1) % cell.shape[1]

        # In order to storage this information in a matrix (nx, ny),
        # we need to distinguish between odd and even rows. This is due to
        # the horizontal offset between them.

        alive_neighbours = cell[x_pre, y] + cell[x_post, y]   \
            + cell[x_pre, y_pre] + cell[x, y_pre] + cell[x_post, y_pre] \
            + cell[x_pre, y_post] + cell[x, y_post] + cell[x_post, y_post]

        return int(alive_neighbours)

    # Update state of the cellular automata and the screen
    def update(self) -> None:

        # Processing window caption:
        self.change_caption()

        # Initially asume every cell is dead (0)
        updated_cells = np.zeros((self.grid.shape[0], self.grid.shape[1]))

        for col, row in np.ndindex(self.grid.shape):
            # Calculate the number of alive neighbours for every cell
            alive_neighbours = self.alive_square(self.grid, col, row)

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
            pygame.draw.rect(
                self.surface, self.color[col, row], (col * self.L, row * self.L, self.L - 1, self.L - 1))

        # Save screen in a folder
        # self.screenshot()

        # Save frame to generate record
        self.record()

        # Show updates on screen
        pygame.display.update()
        # Storage updated grid state in main grid
        self.grid = updated_cells

    # Special key events
    def key_down(self) -> None:
        for col, row in np.ndindex(self.grid.shape):
            self.grid[col, row] = 0  # Kill every cell
            self.color[col, row] = COLOR_BLACK
            pygame.draw.rect(
                self.surface, self.color[col, row], (col * self.L, row * self.L, self.L - 1, self.L - 1))

    def left_click(self) -> None:
        pos = pygame.mouse.get_pos()  # Get mouse pointer position
        for col, row in np.ndindex(self.grid_size):
            # Check if user has clicked on any hexagon hitbox:
            if self.RectHitbox[col, row].collidepoint(pos):
                self.grid[col, row] = 1  # Cell becomes alive
                self.color[col, row] = COLOR_WHITE  # Thus, gets white
                # Draw new hexagon:
                pygame.draw.rect(
                    self.surface, self.color[col, row], (col * self.L, row * self.L, self.L - 1, self.L - 1))
                # Show it on screen:
                pygame.display.update()

    def right_click(self) -> None:
        pos = pygame.mouse.get_pos()  # Get mouse pointer position
        for col, row in np.ndindex(self.grid_size):
            # Check if user has clicked on any hexagon hitbox:
            if self.RectHitbox[col, row].collidepoint(pos):
                self.grid[col, row] = 0  # Cell is killed
                self.color[col, row] = COLOR_BLACK  # Thus, gets black
                # Draw new hexagon:
                pygame.draw.rect(
                    self.surface, self.color[col, row], (col * self.L, row * self.L, self.L - 1, self.L - 1))
                # Show it on screen:
                pygame.display.update()

    def mouse_wheel(self) -> None:
        pos = pygame.mouse.get_pos()
        for col, row in np.ndindex(self.grid_size):
            if self.RectHitbox[col, row].collidepoint(pos):
                if self.grid[col, row] == 1:
                    state = 'alive'
                else:
                    state = 'dead'
                self.log('This cell {} is'.format((col, row))+ ' ' + state +'. Alive neighbours: {}'.format(
                    self.alive_square(self.grid, col, row)))


# Check this script independetly: (do not uncomment if running main.py)
# window = pygame.display.set_mode((800, 600))
# stage = Square(window)
# stage.run()
