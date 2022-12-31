import pygame
import tkinter as tk
import time
from square import Square
from Hexagon import Hexagon
# Inicializar Pygame y Tkinter
pygame.init()
root = tk.Tk()
root.title('Settings')
pygame.display.set_caption("PyCA - Display")

# Crear la ventana de Tkinter
root.geometry("200x600")
# Crear la superficie de Pygame
game_surface = pygame.display.set_mode((800,600))


# Crear el Stage
# TODO Realizarlo en una variable global
stage = Square(game_surface)

## Funciones para crear nuevas instancias del 
# escenario cuando se pulse el botón
def generate_new_square():
  global stage
  stage = Square(game_surface)
  
def generate_new_hexagon():
  global stage
  stage = Hexagon(game_surface)

# Creamos un boton para el escenario stage
button1 = tk.Button(root, text="Square Stage", command=generate_new_square)
button1.pack()

# Creamos un boton para el escenario stage
button2 = tk.Button(root, text="Hexagon Stage", command=generate_new_hexagon)
button2.pack()

# Bucle principal del programa
while True:
  # Actualizar el Stage (Cuadrado, Hexagonal, Voronoi)
  stage.handle_events()

  # Si el programa sigue funcionando
  if stage.running:
    stage.update()
    pygame.display.update()

  time.sleep(0.001)
  root.update()