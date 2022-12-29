import time
import pygame
import numpy as np

from stage import Stage

COLOR_BG = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_DIE_NEXT = (170, 170, 170)
COLOR_ALIVE_NEXT = (255, 255, 255)
COLOR_GRID_2 = (220, 220, 255)
L=10
grid_topleft=np.array([10,10])

pygame.init()

def ordered_vertices(vertices): #vertices is expected to be a list of tuples
    
    angle = np.zeros([1,len(vertices)])

    center_x = np.average(list(zip(*vertices))[0])
    center_y = np.average(list(zip(*vertices))[1])
    center = np.array([center_x,center_y])
    #unit_reference_vector = np.array([0,1])
    #unit_reference_vector = (np.array(vertices[0]) - center)/np.linalg.norm(center - np.array(vertices[0]))
    k = 0
    for i,j in vertices:
        
        unit_vector_to_center = (np.array([i,j]) - center)/np.linalg.norm(center - np.array([i,j]))
        #print(np.dot(unit_vector_to_center,unit_reference_vector))
        
        #angle[0,k] = np.arccos(np.dot(unit_vector_to_center,unit_reference_vector))
        angle[0,k] = np.arccos(unit_vector_to_center[1])
        
        if i < center[0]:
            angle[0,k] = 2*np.pi - angle[0,k]
        
        k = k + 1
    
    angle = angle*180/np.pi
    # print(angle.tolist()[0])
    # print(vertices)
    # print(center)

    ordered_vertices = [x for _, x in sorted(zip(angle.tolist()[0], vertices), key=lambda pair: pair[0])]
    #Z = [x for _, x in sorted(zip(Y,X))]
    #Z = [x for _, x in sorted(zip(Y, X), key=lambda pair: pair[0])]
    return ordered_vertices #list of tuples

def is_in_polygon(point,ordered_vertices):
    
    positive_cross_products = 0 
    
    for i in range(len(ordered_vertices)):
        if i != len(ordered_vertices) - 1:
            vertex_to_point = np.array(point) - np.array(ordered_vertices[i])
            vertex_to_next_vertex = np.array(ordered_vertices[i+1]) - np.array(ordered_vertices[i])
            
            vertex_to_point = np.insert(vertex_to_point,2,0)
            vertex_to_next_vertex = np.insert(vertex_to_next_vertex,2,0)
            cross_product_z = np.cross(vertex_to_point, vertex_to_next_vertex)[2]
            
            if cross_product_z > 0:
                positive_cross_products = positive_cross_products + 1
                
        else: 
            vertex_to_point = np.array(point) - np.array(ordered_vertices[i])
            vertex_to_next_vertex = np.array(ordered_vertices[0]) - np.array(ordered_vertices[i])
            
            vertex_to_point = np.insert(vertex_to_point,2,0)
            vertex_to_next_vertex = np.insert(vertex_to_next_vertex,2,0)
            cross_product_z = np.cross(vertex_to_point, vertex_to_next_vertex)[2]
            
            if cross_product_z > 0:
                positive_cross_products = positive_cross_products + 1
    #print(positive_cross_products)            
    if positive_cross_products == len(ordered_vertices):
        return True
    else:
        return False

def hexagon_vertices(col,row,side_length,grid_topleft):
    
    width_hex=side_length*np.sqrt(3)
    step_x=width_hex + 3
    step_y=side_length*1.5 + 3 
        
    vertice1 = grid_topleft + np.array([step_x*col,step_y*row])
    vertice2 = grid_topleft + np.array([step_x*col,step_y*row+side_length])
    vertice3 = grid_topleft + np.array([step_x*col+0.5*np.sqrt(3)*side_length,step_y*row+1.5*side_length])
    vertice4 = grid_topleft + np.array([step_x*col+np.sqrt(3)*side_length,step_y*row+side_length])
    vertice5 = grid_topleft + np.array([step_x*col+np.sqrt(3)*side_length,step_y*row])
    vertice6 = grid_topleft + np.array([step_x*col+0.5*np.sqrt(3)*side_length,step_y*row-0.5*side_length])
    
    if row % 2 == 1:
        vertice1 = vertice1 + np.array([step_x/2,0])
        vertice2 = vertice2 + np.array([step_x/2,0])
        vertice3 = vertice3 + np.array([step_x/2,0])
        vertice4 = vertice4 + np.array([step_x/2,0])
        vertice5 = vertice5 + np.array([step_x/2,0])
        vertice6 = vertice6 + np.array([step_x/2,0])
    
    vertices=[tuple(vertice1),tuple(vertice2),tuple(vertice3),tuple(vertice4),tuple(vertice5),tuple(vertice6)]
    return vertices

def alive_hexagon(cell,x,y):
    alive_neighbours = 0
    x_pre = (x-1) % cell.shape[0]
    x_post = (x+1) % cell.shape[0]
    y_pre = (y-1) % cell.shape[1]
    y_post = (y+1) % cell.shape[1]
    
    if y % 2 == 0:
        alive_neighbours = cell[x_pre,y] + cell[x_post,y]   \
                         + cell[x_pre,y_pre] + cell[x,y_pre] \
                         + cell[x_pre,y_post] + cell[x,y_post]
    else:
        alive_neighbours = cell[x_pre,y] + cell[x_post,y]   \
                         + cell[x,y_pre] + cell[x_post,y_pre] \
                         + cell[x,y_post] + cell[x_post,y_post]                     
                        
    return alive_neighbours

class Hexagon(Stage):
    def __init__(self, surface):
        # Set the surface to draw the stage on
        self.surface = surface
        
        # Set the background color
        self.surface.fill(COLOR_GRID)

        # Set the size of the stage
        self.size = surface.get_size()

        # Set the size of the grid
        self.grid_size = (38, 32)

        # Create the grid
        self.grid = np.zeros((self.grid_size[0], self.grid_size[1]))
        
        # Storage ordered vertices
        self.vertices = np.ndarray((self.grid.shape[0],self.grid.shape[1]), dtype=object)
        
        # Storage rectangular hitbox
        self.RectHitbox = np.ndarray((self.grid.shape[0],self.grid.shape[1]), dtype=object)
        
        # Update the screen
        self.update()
        pygame.display.update()

        # Set the running flag to False
        self.running = False

            
    def update(self):
        updated_cells = np.zeros((self.grid.shape[0], self.grid.shape[1]))

        for col, row in np.ndindex(self.grid.shape):
            #alive_neighbours= np.random.randint(6)
            alive_neighbours= alive_hexagon(self.grid,col,row)
            color = COLOR_BG if self.grid[col,row] == 0 else COLOR_ALIVE_NEXT

            if self.grid[col, row] == 1:
                if 2 <= alive_neighbours <= 3:
                    updated_cells[col, row] = 1
                    color = COLOR_ALIVE_NEXT
            else:
                if alive_neighbours == 3:
                    updated_cells[col, row] = 1
                    color = COLOR_ALIVE_NEXT
            
            # pygame.draw.polygon(self.surface, COLOR_GRID_2, hexagon(col,row,L,grid_topleft),width=2)
            self.RectHitbox[col, row] = pygame.draw.polygon(self.surface, color, hexagon_vertices(col,row,L,grid_topleft))
            # self.vertices[col, row] = ordered_vertices(hexagon_vertices(col,row,L,grid_topleft))
        self.grid = updated_cells
        pygame.display.update()
        
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
                for col, row in np.ndindex(self.grid_size):  
                    if self.RectHitbox[col,row].collidepoint(pos):
                        self.grid[col, row] = 1 
                        color = COLOR_ALIVE_NEXT
                        pygame.draw.polygon(self.surface, color, hexagon_vertices(col,row,L,grid_topleft))
                        pygame.display.update()
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                for col, row in np.ndindex(self.grid_size):  
                    if self.RectHitbox[col,row].collidepoint(pos):
                        self.grid[col, row] = 0 
                        color = COLOR_BG
                        pygame.draw.polygon(self.surface, color, hexagon_vertices(col,row,L,grid_topleft))
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
# window = pygame.display.set_mode((800, 600))
# stage = Hexagon(window)
# stage.run()

