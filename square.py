import time
import pygame
import numpy as np

from stage import Stage

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
alive_neighbours_to_be_born = [3]
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
L = 50

# Calculations to adapt grid to the screen according to Lx, Ly and L:
effective_width = L
effective_height = L
nx = np.floor(Lx/effective_width).astype(int)
ny = np.floor(Ly/effective_height).astype(int)

# Toggle between empty and random initial state
initial_alive_probability = 0.0
################################################################################################################################################
################################################################################################################################################

# Start pygame
pygame.init()

# Class for the hexagonal stage:
class Square(Stage):
    def __init__(self, surface):
        # Set the surface to draw the stage on
        self.surface = surface
        
        # Set the background color
        self.surface.fill(COLOR_GRID)

        # Set the size of the stage
        self.size = surface.get_size()

        # Set the size of the grid
        self.grid_size = (nx, ny)
        
        # Toggle between all dead and random initial state 
        self.initial_alive_probability = initial_alive_probability # 0 to 1 
        
        # Color to fill the hexagon (changes after every step)
        self.color = np.ndarray((nx, ny), dtype=object)
        
        # Storage rectangular hitbox for every hexagon. 
        self.RectHitbox = np.ndarray((nx, ny), dtype=object)
        
        # Create and display initial state grid
        self.grid = np.zeros((nx, ny))
        for col, row in np.ndindex(self.grid.shape):
            if np.random.rand() < initial_alive_probability: # Threshold for initial alive state
                self.grid[col, row] = 1 # Tag alive cells with 1
                self.color[col, row] = COLOR_WHITE # Color them white
            else:
                self.grid[col, row] = 0 # Tag dead cells with 0
                self.color[col, row] = COLOR_BLACK # Color them white
            # Display on hexagons on screen ans storage their rectangular hitbox: 
                self.RectHitbox[col, row] = pygame.draw.rect(self.surface, self.color[col,row], (col * L, row * L, L - 1, L - 1))
        # Update screen:
        pygame.display.update()

        # Set the running flag to False
        self.running = False
    
    # Function to calculate the number of alive neighbours
    def alive_square(self,cell,x,y):
        # Set periodic boundary conditions (toroidal shape)
        x_pre = (x-1) % cell.shape[0]
        x_post = (x+1) % cell.shape[0]
        y_pre = (y-1) % cell.shape[1]
        y_post = (y+1) % cell.shape[1]
        
        # In order to storage this information in a matrix (nx, ny),
        # we need to distinguish between odd and even rows. This is due to
        # the horizontal offset between them.
 
        alive_neighbours = cell[x_pre,y] + cell[x_post,y]   \
                         + cell[x_pre,y_pre] + cell[x,y_pre] + cell[x_post,y_pre] \
                         + cell[x_pre,y_post] + cell[x,y_post] + cell[x_post,y_post]
                   
                            
        return alive_neighbours
        
    # Update state of the cellular automata and the screen
    def update(self):
        # Initially asume every cell is dead (0)
        updated_cells = np.zeros((self.grid.shape[0], self.grid.shape[1]))

        for col, row in np.ndindex(self.grid.shape):
            # Calculate the number of alive neighbours for every cell
            alive_neighbours = self.alive_square(self.grid, col, row)
                        
            if self.grid[col, row] == 1:
                # Check if the conditions for birth are met. 
                # Updated grid and color are changed accordingly.
                if alive_neighbours in alive_neighbours_to_survive:
                    updated_cells[col, row] = 1
                    self.color[col,row] = COLOR_SURVIVED
                else:
                    self.color[col,row] = COLOR_BLACK
                # Check if the conditions for survival are met. 
                # Updated grid and color are changed accordingly. 
            else:
                if alive_neighbours in alive_neighbours_to_be_born:
                    updated_cells[col, row] = 1
                    self.color[col,row] = COLOR_JUST_BORN
                else:
                    self.color[col,row] = COLOR_BLACK
                # Note that COLOR_SURVIVED and COLOR_JUST_BORN both mean "alive",
                # but specify the previous state of the cell (alive and dead
                # respectively).
                
            # Draw updated hexagons
            pygame.draw.rect(self.surface, self.color[col,row], (col * L, row * L, L - 1, L - 1))
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
            
            if pygame.mouse.get_pressed()[0]: # True if left-click
                pos = pygame.mouse.get_pos() # Get mouse pointer position
                for col, row in np.ndindex(self.grid_size):  
                    # Check if user has clicked on any hexagon hitbox:
                    if self.RectHitbox[col,row].collidepoint(pos):
                        self.grid[col, row] = 1 # Cell becomes alive
                        self.color[col,row] = COLOR_WHITE # Thus, gets white
                        # Draw new hexagon:
                        pygame.draw.rect(self.surface, self.color[col,row], (col * L, row * L, L - 1, L - 1))
                        # Show it on screen:
                        pygame.display.update()
            elif pygame.mouse.get_pressed()[2]: # True if right-click
                pos = pygame.mouse.get_pos() # Get mouse pointer position
                for col, row in np.ndindex(self.grid_size):  
                    # Check if user has clicked on any hexagon hitbox:
                    if self.RectHitbox[col,row].collidepoint(pos):
                        self.grid[col, row] = 0 # Cell is killed
                        self.color[col,row] = COLOR_BLACK # Thus, gets black
                        # Draw new hexagon:
                        pygame.draw.rect(self.surface, self.color[col,row], (col * L, row * L, L - 1, L - 1))
                        # Show it on screen:
                        pygame.display.update()
            # Analogous action that prints number of alive neighbours on terminal.
            # This is mainly implemented for troubleshooting.
            elif pygame.mouse.get_pressed()[1]: # Central mouse button (mouse wheel)
                pos = pygame.mouse.get_pos()
                for col, row in np.ndindex(self.grid_size):  
                    if self.RectHitbox[col,row].collidepoint(pos):
                        if self.grid[col, row] == 1:
                            print('This cell {} is alive'.format((col, row)))
                        else:
                            print('This cell {} is dead'.format((col, row)))
                        print('Alive neighbours: {}'.format(self.alive_square(self.grid,col,row)))
    def run(self):
        # Main loop
        while True:
            self.handle_events()
            #self.surface.fill(COLOR_GRID)
            if self.running:
                self.update()

            time.sleep(0.001)

# Check this script independetly: (do not uncomment if running main.py)
window = pygame.display.set_mode((800, 600))
stage = Square(window)
stage.run()