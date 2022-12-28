import pygame
import numpy as np
from scipy.spatial import Voronoi

# Set the width and height of the window
width, height = 640, 480

# Generate a set of random points
num_points = 100
points = np.zeros([num_points, 2], np.uint16)
points[:, 0] = np.random.randint(0, width, size=num_points)
points[:, 1] = np.random.randint(0, height, size=num_points)

# Create a Voronoi object
vor = Voronoi(points)

# Initialize Pygame and create a window
pygame.init()
screen = pygame.display.set_mode((width, height))

# Keep track of the polygons and their positions
polygons = []
for region in vor.regions:
    if not -1 in region:
        polygon = [vor.vertices[i] for i in region]
        polygons.append((polygon, (0, 0)))

# Draw the Voronoi diagram
for polygon, pos in polygons:
    pygame.draw.polygon(screen, (255, 255, 255), polygon, 1)

# Display the window and run the game loop
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check for clicks within the bounding box of each poly
            mouse_pos = pygame.mouse.get_pos()
            for polygon, pos in polygons:
                # Calculate the bounding box of the polygon
                min_x, min_y = np.min(polygon, axis=0)
                max_x, max_y = np.max(polygon, axis=0)
                rect = pygame.Rect(pos, (max_x - min_x, max_y - min_y))

                # Check if the mouse position is within the bounding box
                if rect.collidepoint(mouse_pos):
                    # The mouse position is within the bounding box of the polygon
                    # Do something here, such as printing a message or changing the color of the polygon
                    print("Clicked on polygon!")

pygame.quit()




