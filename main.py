import pygame
import tkinter as tk
from tkinter import colorchooser
from typing import Tuple
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
root.geometry("700x450")
# Crear la superficie de Pygame
game_surface = pygame.display.set_mode((800,600))

# Global variables
# By default we create a hexagon grid
stage = Hexagon(game_surface)
stage_st = "HEX" # SQU | VOR
L = 10 # Init
COLOR_JUST_BORN = (0,255,0)
COLOR_SURVIVED = (255,0,0)
alive_neighbours_to_be_born = [] # Update
alive_neighbours_to_survive = [] # Update
initial_alive_probability = 0 # Init

## Funciones para crear nuevas instancias del 
# escenario cuando se pulse el botón
def generate_new_square() -> None:
  global stage, stage_st
  stage = Square(game_surface)
  stage_st = "SQU"

def generate_new_hexagon() -> None:
  global stage, stage_st
  stage = Hexagon(game_surface)
  stage_st = "HEX"

def generate_new_Voronoi() -> None:
  global stage, stage_st
  stage = VoronoiGrid(game_surface)
  stage_st = "VOR"

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
def log(message) -> None:
    log_text.insert(tk.END, message + "\n")

log("Welcome to PyCA software!")

#######
# Stage
#######

# Creamos un boton para el escenario stage
button1 = tk.Button(root, text="Square", command=generate_new_square)
button1.grid(row=1, column=1, padx=5, pady=10)

# Creamos un boton para el escenario stage
button2 = tk.Button(root, text="Hexagon", command=generate_new_hexagon)
button2.grid(row=1, column=2,padx=5, pady=10)

# Creamos un boton para el escenario stage
button3 = tk.Button(root, text="Voronoi", command=generate_new_Voronoi)
button3.grid(row=1, column=3,padx=5, pady=10)

#######
# CHANGE COLOR CELLS
#######

def change_color1() -> None:
  color = colorchooser.askcolor()[0]
  # global COLOR_JUST_BORN
  # COLOR_JUST_BORN = color
  stage.COLOR_JUST_BORN = color
  log(f"Hemos cambiado el tipo de celda X con un color{color}")

def change_color2() -> None:
  color = colorchooser.askcolor()[0]
  # global COLOR_SURVIVED
  # COLOR_SURVIVED = color
  stage.COLOR_SURVIVED = color
  log(f"Hemos cambiado el tipo de celda Y con un color{color}")

color1 = tk.Label(root,text="COLOR_JUST_BORN",font=("Helvetica", 10))
color1.grid(row=2,column=0, padx=5, pady=5)

btnc1 = tk.Button(root, text="Change Color", command=change_color1)
btnc1.grid(row=2, column=1)

color2 = tk.Label(root,text="COLOR_SURVIVED",font=("Helvetica", 10))
color2.grid(row=2,column=2)

btnc2 = tk.Button(root, text="Change Color", command=change_color2)
btnc2.grid(row=2, column=3)

#####################
# L system
#####################
changeL = tk.Label(root,text="Select L:",font=("Helvetica", 10))
changeL.grid(row=3,column=0,columnspan=1)

scale = tk.Scale(from_=3, to=200, digits = 3,orient=tk.HORIZONTAL,resolution = 0.01)
scale.grid(row=3,column=1,columnspan=1)

def apply_grid_size() -> None:
  value = scale.get()
  # TODO: AÑADIR LOS COLORES Y RESTO DE PARÁMETROS CUANDO ENTREMOS AQUÍ
  global stage
  if stage_st == "HEX":
    stage = Hexagon(game_surface, L = value)
  elif stage_st == "SQU":
    stage = Square(game_surface, L = value)
  elif stage_st == "VOR":
    stage = VoronoiGrid(game_surface, L = value)
  pygame.display.update()
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

def send_rule() -> None:
  """
  Send rule to the system
  """
  msg = label7.get()
  if is_rule_valid(msg):
    global alive_neighbours_to_be_born
    global alive_neighbours_to_survive
    alive_neighbours_to_be_born , alive_neighbours_to_survive = parser_rule(msg)
    stage.alive_neighbours_to_be_born = alive_neighbours_to_be_born
    stage.alive_neighbours_to_survive = alive_neighbours_to_survive
    # print(alive_neighbours_to_be_born)
    # print(stage.alive_neighbours_to_be_born)
    # print(alive_neighbours_to_survive)
    # print(stage.alive_neighbours_to_survive)

    log(f"The new rule is: {msg}")
  else:
    log(f"The rule {msg} is invalid. Please set a valid rule")
    

def is_rule_valid(rule:str) -> bool:
  """
  Check if rule is valid

  Example:
    is_rule_valid("B3/S23") # True
    is_rule_valid("B99/S45") # False, in B variable there're duplicate elements
    is_rule_valid("B19/S43") # False, in S the numbers aren't ordered
  """
  def is_asc_unique(ls:str) -> bool:
    """
    check if string hasn't any duplicates and the values are sorted ascending
    """
    nums = [int(x) for x in ls]
    # Check if numbers are in ascending order
    for i in range(1,len(nums)):
      if nums[i] < nums[i-1]:
        return False
    # Check if exist duplicates
    if len(nums) != len(set(nums)):
      return False
    return True
  # If the pattern match with a rule
  if re.match(r"^B([0-9]{1,9})/S([0-9]{1,9})$",rule):
    # Split the rule
    b,s = rule.split("/")
    b_cond = b[1:]
    s_cond = s[1:]
    if is_asc_unique(b_cond) and is_asc_unique(s_cond):
      return True
  return False

def parser_rule(rule:str) -> Tuple[list,list]:
  """
  Generate a tuple of list that each list is numbers of neighbours
  """
  b,s = rule.split("/")
  born = [int(x) for x in b if x.isdigit()]
  surv = [int(x) for x in s if x.isdigit()]
  return born,surv
  

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