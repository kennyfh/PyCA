"""
Clase padre donde se van a crear los 3 escenarios: Cuadrático, Hexagonal y Voronoi
"""
COLOR_BLACK = (10, 10, 10)
COLOR_WHITE = (255, 255, 255)
COLOR_RED=(255,0,0)
COLOR_GREEN=(0,255,0)
COLOR_BLUE=(0,0,255)

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

# Length of the size of the regular hexagon. It would be ideal
# to make "cell size" an abstract parameter in every dird (square and voronoi too).
# In square and hexagonal grids, it refers to the side length, but in voronoi it could
# be proportionate to the inverse of the number of cells (which indicates qualitative
# size)
L = 14

# Toggle between empty and random initial state
initial_alive_probability = 0.0

class Stage:
    def __init__(self, surface, L = 10, COLOR_JUST_BORN = (255,255,255), COLOR_SURVIVED = (255,255,255),alive_neighbours_to_be_born = [3],alive_neighbours_to_survive = [2,3], initial_alive_probability = 0, delay = 0.001):
        self.surface = surface
        self.L = L
        self.COLOR_JUST_BORN = COLOR_JUST_BORN
        self.COLOR_SURVIVED = COLOR_SURVIVED
        self.alive_neighbours_to_be_born = alive_neighbours_to_be_born
        self.alive_neighbours_to_survive = alive_neighbours_to_survive
        self.initial_alive_probability = initial_alive_probability
        self.delay = delay

    def update(self):
        pass

    def handle_events(self):
        pass

    def run(self):
        pass
