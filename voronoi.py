import time
import pygame
import numpy as np
from scipy.spatial import Voronoi
from pixel_perfect_polygon_hitbox import ordered_vertices, is_in_polygon

from stage import Stage

COLOR_BLACK = (10, 10, 10)
COLOR_WHITE = (255, 255, 255)
COLOR_RED=(255,0,0)
COLOR_GREEN=(0,255,0)
COLOR_BLUE=(0,0,255)

COLOR_GRID = (40, 40, 40)
COLOR_BACKGROUND = (126, 126, 126)

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
alive_neighbours_to_survive = [2,3]

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
L = 10
number_of_seeds = np.floor(Lx*Ly/L**2).astype(int) 
# number_of_seeds= 700
# print('Number of seeds to generate Voronoi diagram: {}'.format(number_of_seeds))

# Toggle between empty and random initial state
initial_alive_probability = 0.0
################################################################################################################################################
################################################################################################################################################

# Start pygame
pygame.init()

# Class for the hexagonal stage:
class VoronoiGrid(Stage):
    def __init__(self, surface):
        # Set the surface to draw the stage on
        self.surface = surface

        # Set the size of the stage
        self.size = surface.get_size()
        
        # Set the size of the grid
        points = np.zeros([number_of_seeds, 2])
        points[:, 0] = np.random.randint(0, Lx, size = number_of_seeds)
        points[:, 1] = np.random.randint(0, Ly, size = number_of_seeds)
        
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
        self.voronoi_vertices_labels = np.ndarray((self.number_of_regions), dtype=object)

        # Vertices for voronoi regions 
        self.voronoi_vertices = np.ndarray((self.number_of_regions), dtype=object)
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
                    self.RectHitbox[cell] = pygame.draw.polygon(self.surface, COLOR_GRID, self.voronoi_vertices[cell], 2)
                    cell = cell + 1
            scipy_label = scipy_label + 1
            
        
        self.average_number_of_vertices = np.average([len(vertex) for vertex in self.voronoi_vertices])
        print(self.average_number_of_vertices)
        # Update screen:
        pygame.display.update()
         
        # Toggle between all dead and random initial state 
        self.initial_alive_probability = initial_alive_probability # 0 to 1 
        
        # Color to fill the hexagon (changes after every step)
        self.color = np.ndarray((self.number_of_regions), dtype=object)
                 
        # Neighbours for voronoi regions 
        self.neighbours = np.ndarray((self.number_of_regions), dtype=object)
        for cell in range(self.number_of_regions):
            self.neighbours[cell] = []
        for cell in range(self.number_of_regions):
            for vertex_label in self.voronoi_vertices_labels[cell]:
                for other_cell in range(self.number_of_regions):
                    if vertex_label in self.voronoi_vertices_labels[other_cell] and other_cell not in self.neighbours[cell] and other_cell != cell:
                        self.neighbours[cell].append(other_cell)
        
        # Create and display initial state grid
        self.grid = np.zeros(self.number_of_regions)
        for cell in range(self.number_of_regions):
            if np.random.rand() < initial_alive_probability: # Threshold for initial alive state
                self.grid[cell] = 1 # Tag alive cells with 1
                self.color[cell] = COLOR_WHITE # Color them white
            else:
                self.grid[cell] = 0 # Tag dead cells with 0
                self.color[cell] = COLOR_BLACK # Color them white
            # Display on hexagons on screen ans storage their rectangular hitbox: 
            pygame.draw.polygon(self.surface, self.color[cell], self.voronoi_vertices[cell])
            pygame.draw.polygon(self.surface, COLOR_GRID, self.voronoi_vertices[cell], 2)
        # Update screen:
        pygame.display.update()

        # Set the running flag to False
        self.running = False    
            
    # Function to calculate the number of alive neighbours
    def alive_voronoi(self,cell):
        alive_neighbours = 0
        for neighbour in self.neighbours[cell]:
            alive_neighbours = alive_neighbours + self.grid[neighbour]
        return alive_neighbours
        
    # Update state of the cellular automata and the screen
    def update(self):
        # Initially asume every cell is dead (0)
        updated_cells = np.zeros(self.number_of_regions)

        for cell in range(self.number_of_regions):
            # Calculate the number of alive neighbours for every cell
            alive_neighbours = self.alive_voronoi(cell)
                        
            if self.grid[cell] == 1:
                # Check if the conditions for birth are met. 
                # Updated grid and color are changed accordingly.
                if alive_neighbours in alive_neighbours_to_survive:
                    updated_cells[cell] = 1
                    self.color[cell] = COLOR_SURVIVED
                else:
                    self.color[cell] = COLOR_BLACK
                # Check if the conditions for survival are met. 
                # Updated grid and color are changed accordingly. 
            else:
                if alive_neighbours in alive_neighbours_to_be_born:
                    updated_cells[cell] = 1
                    self.color[cell] = COLOR_JUST_BORN
                else:
                    self.color[cell] = COLOR_BLACK
                # Note that COLOR_SURVIVED and COLOR_JUST_BORN both mean "alive",
                # but specify the previous state of the cell (alive and dead
                # respectively).
                
            # Draw updated hexagons
            pygame.draw.polygon(self.surface, self.color[cell], self.voronoi_vertices[cell])
            pygame.draw.polygon(self.surface, COLOR_GRID, self.voronoi_vertices[cell], 2)
        # Show updates on screen
        pygame.display.update()
        # Storage updated grid state in main grid
        self.grid = updated_cells

    # Handle pygame events: mainly user instructions
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN: # Check if any key gets pressed down
                if event.key == pygame.K_SPACE: # Check if spacebar gets pressed down
                    self.running = not self.running # Pause and resume button
                elif event.key == pygame.K_RIGHT: # Check if right arrow gets pressed down
                    # This key allows single step update in order to
                    # watch evolution in detail:
                    self.running = False
                    self.update()
                    pygame.display.update() 
                elif event.key == pygame.K_DOWN: # Check if down arrow gets pressed down
                    self.running = False
                    for cell in range(self.number_of_regions):
                        self.grid[cell] = 0 # Kill every cell
                        self.color[cell] = COLOR_BLACK
                        pygame.draw.polygon(self.surface, self.color[cell], self.voronoi_vertices[cell])
                    self.update()
                    pygame.display.update()
            
            if pygame.mouse.get_pressed()[0]: # True if left-click
                pos = pygame.mouse.get_pos() # Get mouse pointer position
                for cell in range(self.number_of_regions):  
                    # Check if user has clicked on any hexagon hitbox:
                    if self.RectHitbox[cell].collidepoint(pos):
                        if is_in_polygon(pos, self.voronoi_vertices[cell]):
                            self.grid[cell] = 1 # Cell becomes alive
                            self.color[cell] = COLOR_WHITE # Thus, gets white
                            # Draw new hexagon:
                            pygame.draw.polygon(self.surface, self.color[cell], self.voronoi_vertices[cell])
                            pygame.draw.polygon(self.surface, COLOR_GRID, self.voronoi_vertices[cell], 2)
                            # Show it on screen:
                            pygame.display.update()
            elif pygame.mouse.get_pressed()[2]: # True if right-click
                pos = pygame.mouse.get_pos() # Get mouse pointer position
                for cell in range(self.number_of_regions):  
                    # Check if user has clicked on any hexagon hitbox:
                    if self.RectHitbox[cell].collidepoint(pos):
                        if is_in_polygon(pos, self.voronoi_vertices[cell]):
                            self.grid[cell] = 0 # Cell is killed
                            self.color[cell] = COLOR_BLACK # Thus, gets black
                            # Draw new hexagon:
                            pygame.draw.polygon(self.surface, self.color[cell], self.voronoi_vertices[cell])
                            pygame.draw.polygon(self.surface, COLOR_GRID, self.voronoi_vertices[cell], 2)
                            # Show it on screen:
                            pygame.display.update()
            # Analogous action that prints number of alive neighbours on terminal.
            # This is mainly implemented for troubleshooting.
            elif pygame.mouse.get_pressed()[1]: # Central mouse button (mouse wheel)
                pos = pygame.mouse.get_pos()
                for cell in np.ndindex(self.grid_size):  
                    if self.RectHitbox[cell].collidepoint(pos):
                        if is_in_polygon(pos, self.voronoi_vertices[cell]):
                            if self.grid[cell] == 1:
                                print('This cell {} is alive'.format(cell))
                            else:
                                print('This cell {} is dead'.format(cell))
                            print('Vertices labels: {}'.format(self.voronoi_vertices_labels[cell]))
                            print('Neighbours: {}'.format(self.neighbours[cell]))
                            print('Alive neighbours: {}'.format(self.alive_voronoi(cell)))
    def run(self):
        # Main loop
        while True:
            self.handle_events()
            #self.surface.fill(COLOR_GRID)
            if self.running:
                # time.sleep(self.delay)
                time.sleep(0.1)
                self.update()            

# Check this script independetly: (do not uncomment if running main.py)
# window = pygame.display.set_mode((800, 600))
# stage = VoronoiGrid(window)
# stage.run()

