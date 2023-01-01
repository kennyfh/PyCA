import pygame
import tkinter as tk
from tkinter import colorchooser
import re
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
root.geometry("820x450")
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

def generate_new_Voronoi():
  global stage
  stage = VoronoiGrid(game_surface)

# Generate Header
header_label = tk.Label(root, text="Welcome to PyCA", font=("Helvetica", 18))
header_label.grid(row=0, column=1, columnspan=2, pady=20, padx=20, sticky="nsew")

label1 = tk.Label(root,text="Stage:",font=("Helvetica", 10))
label1.grid(row=1,column=0)

#####
# LOG FUNC
#####

frame = tk.Frame(root)
frame.grid(row=5, column=0, columnspan=4, sticky="we", padx=10, pady=10)

# Create a Text widget to display the log
log_text = tk.Text(frame)
log_text.pack(side=tk.RIGHT)

# Create a Scrollbar widget and link it to the Text widget
scrollbar = tk.Scrollbar(frame, command=log_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
log_text.configure(yscrollcommand=scrollbar.set)

# Function to append a message to the log
def log(message):
    log_text.insert(tk.END, message + "\n")

log("Welcome to PyCA software!")



# Row 1
# Creamos un boton para el escenario stage
button1 = tk.Button(root, text="Square", command=generate_new_square)
button1.grid(row=1, column=1, padx=5, pady=10)

# Creamos un boton para el escenario stage
button2 = tk.Button(root, text="Hexagon", command=generate_new_hexagon)
button2.grid(row=1, column=2,padx=5, pady=10)

# Creamos un boton para el escenario stage
button3 = tk.Button(root, text="Voronoi", command=generate_new_Voronoi)
button3.grid(row=1, column=3,padx=5, pady=10)

# Row 3

def change_color1():
  color = colorchooser.askcolor()
  # TODO: CREAR UNA FORMA DE MODIFICAR EN STAGE EL COLOR DE ALIVE
  print(color)

def change_color2():
  color = colorchooser.askcolor()
  # TODO: CREAR UNA FORMA DE MODIFICAR EN STAGE EL COLOR DE DEAD
  print(color)

def change_color3():
  color = colorchooser.askcolor()
  # TODO: CREAR UNA FORMA DE MODIFICAR EN STAGE EL COLOR DE DEAD
  print(color)  

color1 = tk.Label(root,text="Color1",font=("Helvetica", 10))
color1.grid(row=2,column=0, padx=5, pady=5)

btnc1 = tk.Button(root, text="Change Color", command=change_color1)
btnc1.grid(row=2, column=1)

color2 = tk.Label(root,text="Color2",font=("Helvetica", 10))
color2.grid(row=2,column=2)

btnc2 = tk.Button(root, text="Change Color", command=change_color2)
btnc2.grid(row=2, column=3)

color3 = tk.Label(root,text="Color3",font=("Helvetica", 10))
color3.grid(row=2,column=4)

btnc3 = tk.Button(root, text="Change Color", command=change_color3) 
btnc3.grid(row=2, column=5)


#####################
# L system
#####################
changeL = tk.Label(root,text="Select L:",font=("Helvetica", 10))
changeL.grid(row=3,column=0,columnspan=1)

scale = tk.Scale(from_=3, to=200, digits = 3,orient=tk.HORIZONTAL,resolution = 0.01)
scale.grid(row=3,column=1,columnspan=1)

def apply_grid_size():
  value = scale.get()
  # TODO: podemos programar para que en el log aparezca que hemos cambiado los elementos a 0
  log(f"L size is now: {value} pixels")

btnL = tk.Button(root, text="Apply Size", command=apply_grid_size)
btnL.grid(row=3, column=2)

#######
# RULES 
#######

rules = tk.Label(root,text="Rules",font=("Helvetica", 10))
rules.grid(row=4,column=0)

label7 = tk.Entry(root)
label7.grid(row=4,column=1, padx=5, pady=15)

def send_rule():
  """
  Send rule to the system
  """
  msg = label7.get()
  if is_rule_valid(msg):
    # TODO: APLICAR LA REGLA EN NUESTRO STAGE
    log(f"The new rule is: {msg}")
  else:
    log(f"The rule {msg} is invalid. Please set a valid rule")
    

def is_rule_valid(rule:str) -> bool:
  def is_asc_unique(ls:str) -> bool:
    nums = [int(x) for x in ls]
    # Check if numbers are in ascending order
    for i in range(1,len(nums)):
      if nums[i] < nums[i-1]:
        return False
    if len(nums) != len(set(nums)):
      return False
    return True

  if re.match(r"^B([0-9]{1,9})/S([0-9]{1,9})$",rule):
    print("ENTRAAAAAAAAA")
    # Split the rule
    b,s = rule.split("/")
    b_cond = b[1:]
    s_cond = s[1:]
    print(b_cond)
    print(s_cond)
    if is_asc_unique(b_cond) and is_asc_unique(s_cond):
      return True
  return False
  

send_rule = tk.Button(root, text="Set rule", command=send_rule)
send_rule.grid(row=4, column=2)


# Main Loop
while True:
  # Update the Stage (Square, Hexagon, Voronoi)
  stage.handle_events()
  if stage.running:
    stage.update()
    pygame.display.update()
  time.sleep(0.001)
  root.update()