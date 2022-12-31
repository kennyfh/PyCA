import pygame
import tkinter as tk
from tkinter import colorchooser
import time
from square import Square
from Hexagon import Hexagon
from voronoi import VoronoiGrid
# Inicializar Pygame y Tkinter
pygame.init()
root = tk.Tk()
root.title('Settings')
pygame.display.set_caption("PyCA - Display")

# Crear la ventana de Tkinter
root.geometry("650x450")
# Crear la superficie de Pygame
game_surface = pygame.display.set_mode((800,600))


# Configure the window to allow the widgets to resize with the window

root.rowconfigure(9, weight=1)

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

def generate_new_Voronoi():
  global stage
  stage = VoronoiGrid(game_surface)

# Fila 0
label1 = tk.Label(root,text="Stage:")
label1.grid(row=0,column=0)

# Fila 1
# Creamos un boton para el escenario stage
button1 = tk.Button(root, text="Square", command=generate_new_square)
button1.grid(row=1, column=1, padx=5, pady=10)

# Creamos un boton para el escenario stage
button2 = tk.Button(root, text="Hexagon", command=generate_new_hexagon)
button2.grid(row=1, column=2,padx=5, pady=10)

# Creamos un boton para el escenario stage
button3 = tk.Button(root, text="Voronoi", command=generate_new_Voronoi)
button3.grid(row=1, column=3,padx=5, pady=10)

# Fila 2
label2 = tk.Label(root,text="Choose colors:")
label2.grid(row=2,column=0) # ,columnspan=1

# Fila 3

def change_color_alive():
  color = colorchooser.askcolor()
  # TODO: CREAR UNA FORMA DE MODIFICAR EN STAGE EL COLOR DE ALIVE
  print(color)

def change_color_dead():
  color = colorchooser.askcolor()
  # TODO: CREAR UNA FORMA DE MODIFICAR EN STAGE EL COLOR DE DEAD
  print(color)

label3 = tk.Label(root,text="Alive:")
label3.grid(row=3,column=0)

button4 = tk.Button(root, text="Color1", command=change_color_alive) # 
button4.grid(row=3, column=1,padx=5, pady=10)

label4 = tk.Label(root,text="Dead:")
label4.grid(row=3,column=2)

button5 = tk.Button(root, text="Color2", command=change_color_dead) # 
button5.grid(row=3, column=3,padx=5, pady=10)

# Fila 4
label5 = tk.Label(root,text="Select L:")
label5.grid(row=4,column=0,columnspan=1)

# Fila 5
# Create the volume bar
volume = tk.Scale(from_=0.55, to=5.75, digits = 3,orient=tk.HORIZONTAL,resolution = 0.01) # , label = "Select L:"
volume.grid(row=5,column=1,columnspan=1)

# Fila 6
label6 = tk.Label(root,text="Rules")
label6.grid(row=6,column=0,columnspan=1)

# Fila 7
label7 = tk.Entry(root)
label7.grid(row=7,column=1,columnspan=1)

def send_message():
  msg = label7.get()
  print(msg)

button6 = tk.Button(root, text="Set rule", command=send_message) # , command=change_color_dead
button6.grid(row=7, column=2)

# Fila 8
label8 = tk.Label(root,text="Log")
label8.grid(row=8,column=1,columnspan=1)

# Fila 9
# Create a frame to hold the Text widget and the Scrollbar widget
frame = tk.Frame(root)
frame.grid(row=9, column=0, columnspan=4, sticky="we")

# Create a Text widget to display the log
log_text = tk.Text(frame)
log_text.pack(side=tk.LEFT)

# Create a Scrollbar widget and link it to the Text widget
scrollbar = tk.Scrollbar(frame, command=log_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
log_text.configure(yscrollcommand=scrollbar.set)

# Function to append a message to the log
def log(message):
    log_text.insert(tk.END, message + "\n")

log("This is a test message.")

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