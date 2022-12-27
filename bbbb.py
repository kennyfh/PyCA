import tkinter as tk
import pygame
import sys
import time
from rectangle import Stage

# Initialize Pygame
pygame.init()

# Set the window size
window_size = (800, 600)

# Create the window
screen = pygame.display.set_mode(window_size)

# Set the width of the menu
menu_width = 200

# Create the stage
game_surface = pygame.Surface((window_size[0] - menu_width, window_size[1]))
stage = Stage(game_surface)

# Create the main tkinter window
root = tk.Tk()
root.geometry('200x600')

# Function to create a new instance of the stage when the button is clicked
def create_new_stage():
  global stage
  stage = Stage(game_surface)

# Create a button to create a new stage
button = tk.Button(root, text="Create new stage", command=create_new_stage)
button.pack()

# Main loop
while True:
    # Actualizar y dibujar el Stage
  stage.handle_events()

  if stage.running:
    stage.update()
    pygame.display.update()
  
  # Draw the game surface onto the main screen
  screen.blit(game_surface, (menu_width, 0))
  

  time.sleep(0.001)
  
  # Update tkinter events
  root.update()
