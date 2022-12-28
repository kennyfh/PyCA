import pygame

pygame.init()

# Set the window size and title
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption('Click on the Polygon')

# Set the polygon points and color
polygon_points = [(100, 100), (150, 50), (200, 100)]
polygon_color = (255, 0, 0)  # Red

# Create a bounding box for the polygon
polygon_rect = pygame.Rect(min(x for x, y in polygon_points), min(y for x, y in polygon_points),
                         max(x for x, y in polygon_points) - min(x for x, y in polygon_points),
                         max(y for x, y in polygon_points) - min(y for x, y in polygon_points))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse position is inside the polygon
            if polygon_rect.collidepoint(event.pos):
                print('Clicked on the polygon!')

    # Draw the polygon
    pygame.draw.polygon(screen, polygon_color, polygon_points)

    # Update the display
    pygame.display.flip()

pygame.quit()
