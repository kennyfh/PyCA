import pygame
import random
from scipy.spatial import Voronoi

# Set the width and height of the window
width, height = 640, 480

# Generate a set of random points
num_points = 1000
points = [(random.randint(0, width), random.randint(0, height)) for _ in range(num_points)]# Create a Voronoi object
vor = Voronoi(points)

# Initialize Pygame and create a window
pygame.init()
screen = pygame.display.set_mode((width, height))

# Draw the Voronoi diagram
for region in vor.regions:
    if not -1 in region:
        polygon = [vor.vertices[i] for i in region]
        print(polygon)
        pygame.draw.polygon(screen, (0, 0, 0), polygon, 1)

# Display the window and run the game loop
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
pygame.quit()
