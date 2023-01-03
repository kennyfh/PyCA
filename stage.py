#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Module: Stage
# Created By  : TEODORO JIMÉNEZ LEPE
#               KENNY JESÚS FLORES HUAMÁN
# version ='1.0'
# ---------------------------------------------------------------------------
# Parent class where the 3 scenarios will be created: Quadratic, Hexagonal and Voronoi
# ---------------------------------------------------------------------------

COLOR_BLACK = (10, 10, 10)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)

COLOR_GRID = (40, 40, 40)

# EVANGELION_GREEN = (10,144,98)
# EVANGELION_PURPLE = (157,68,199)

################################################################################################################################################
# Parameters that should be controled by the user through tkinter interface:
################################################################################################################################################

# Customize birth and survival colors!
COLOR_JUST_BORN = COLOR_GREEN
COLOR_SURVIVED = COLOR_RED

# Create your own rules based on number of neighbours!
alive_neighbours_to_be_born = [2]
alive_neighbours_to_survive = [2]

# B1S- makes cool patterns
# B-S123456 too
# B2S2 has some blinkers and is similar to B2S23 square grid in proportion to neighbourhood
# Check B2S345 and others B2S-
# Look for reference of previous works (some rules show gliders)


# These are supposedly constant values: (screen dimensions)
Lx = 800
Ly = 600


class Stage:
    """
    A base class for generating and visualizing cellular automata stages.

    Args:
        surface (pygame.Surface): The surface on which the stage will be drawn.
        L (int, optional): The size of the cells in the stage. Default is 10.
        COLOR_JUST_BORN (Tuple[int, int, int], optional): The color of cells that are born in a given step. Default is (255, 255, 255).
        COLOR_SURVIVED (Tuple[int, int, int], optional): The color of cells that survive to the next step. Default is (255, 255, 255).
        alive_neighbours_to_be_born (List[int], optional): A list of the number of alive neighbors required for a cell to be born. Default is [3].
        alive_neighbours_to_survive (List[int], optional): A list of the number of alive neighbors required for a cell to survive. Default is [2, 3].
        initial_alive_probability (float, optional): The probability that a cell will be initially alive. Default is 0.
    """

    def __init__(self, surface, L=10, COLOR_JUST_BORN=(255, 255, 255), COLOR_SURVIVED=(255, 255, 255), alive_neighbours_to_be_born=[3], alive_neighbours_to_survive=[2, 3], initial_alive_probability=0):
        self.surface = surface
        self.L = L
        self.COLOR_JUST_BORN = COLOR_JUST_BORN
        self.COLOR_SURVIVED = COLOR_SURVIVED
        self.alive_neighbours_to_be_born = alive_neighbours_to_be_born
        self.alive_neighbours_to_survive = alive_neighbours_to_survive
        self.initial_alive_probability = initial_alive_probability

    def update(self):
        pass

    def handle_events(self):
        pass

    def run(self):
        pass
