import pygame
import pygame.font
import pygame.event
import sys
import rectangle
import time

# Initialize Pygame
pygame.init()

# Set the window size
window_size = (800, 600)

# Create the window
screen = pygame.display.set_mode(window_size)

# Set the font and size for the menu
font = pygame.font.Font(None, 32)

# Set the width of the menu
menu_width = 200

# Create a function to draw the menu
def draw_menu(options, font, surface):
  # Determine the size of the surface
  surface_size = surface.get_size()
  
  # Create a list to hold the rendered options
  rendered_options = []
  
  # Render each option
  for option in options:
    rendered_options.append(font.render(option, 1, (255, 255, 255)))
  
  # Calculate the position of each option
  x = 10
  y = surface_size[1] / 2
  y_offset = font.size(options[0])[1]
  
  # Draw the options onto the surface
  for option in rendered_options:
    surface.blit(option, (x, y))
    y += y_offset

def draw_game(surface):
  # Set the background color
  surface.fill((0, 0, 0))
  
  # Draw a circle at the center of the screen
  pygame.draw.circle(surface, (255, 255, 255), (surface.get_width() / 2, surface.get_height() / 2), 50)

# Set the options for the menu
options = ['Option 1', 'Option 2', 'Option 3']


game_surface = pygame.Surface((window_size[0] - menu_width, window_size[1]))
# Create the stage
stage = rectangle.Stage(game_surface)

# Main loop
while True:
  # Handle events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
  
  # Draw the menu
  draw_menu(options, font, screen)
  
  # Update and draw the stage
  stage.handle_events()
  
  # Draw the game surface onto the main screen
  screen.blit(game_surface, (menu_width, 0))
  
  # Update the display
  pygame.display.update()
  time.sleep(0.001)