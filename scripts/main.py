#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Module: Main
# Created By  : TEODORO JIMÉNEZ LEPE
#               KENNY JESÚS FLORES HUAMÁN
# version ='1.0'
# ---------------------------------------------------------------------------
# This file contains a Pygame and Tkinter application for generating and visualizing cellular automata.
# ---------------------------------------------------------------------------

# IMPORTS
# Standard library imports
import re
import numpy as np

# Third-party imports
import pygame
import tkinter as tk
from tkinter import colorchooser
from tkinter import messagebox 
from typing import Tuple

# Own local imports
from stages.hexagon import Hexagon
from stages.square import Square
from stages.voronoi import VoronoiGrid


# CODE
# Initialize Tkinter and pygame
pygame.init()
root = tk.Tk()
root.title('Settings')
pygame.display.set_caption("PyCA - Display")

# Create Tkinter screen and Pygame surface
root.geometry("700x450")
game_surface = pygame.display.set_mode((800, 600))

# Global variables
# By default we create a hexagon grid
stage = Hexagon(game_surface)
stage_st = "HEX"  # SQU | VOR
L = 10  # Init
COLOR_JUST_BORN = (0, 255, 0)
COLOR_SURVIVED = (255, 0, 0)
alive_neighbours_to_be_born = []  # Update
alive_neighbours_to_survive = []  # Update
initial_alive_probability = 0  # Init
frame_rate = 30

# Generate a new Stage instance


def generate_new_square() -> None:
    """
      Generates a new Square stage for the cellular automata.
    """
    global stage, stage_st
    scale.set(10)
    stage = Square(game_surface)
    stage_st = "SQU"


def generate_new_hexagon() -> None:
    """
      Generates a new Hexagon stage for the cellular automata.
    """
    global stage, stage_st
    scale.set(5)
    stage = Hexagon(game_surface)
    stage_st = "HEX"


def generate_new_Voronoi() -> None:
    """
      Generates a new Voronoi stage for the cellular automata.
    """
    global stage, stage_st
    scale.set(6)
    stage = VoronoiGrid(game_surface)
    stage_st = "VOR"
    
#################
# Show controls
#################

def show_controls() -> None:
    """
      Show game controls on message box
    """
    messagebox.showinfo('Controls',"LEFT CLICK: Bring selected cell to life \n" + 
                                    "RIGHT CLICK: Kill selected cell \n" +                                     
                                    "MOUSE WHEEL CLICK: Show info about selected cell \n \n" +
                                    "SPACE BAR: Start/stop simulation \n" +
                                    "RIGHT ARROW: Simulate one step \n" + 
                                    "DOWN ARROW: Kill all cells \n \n" + 
                                    "S: Take a screenshot \n"  
                                    "R: Start/stop recording screen")
#################
# Generate Header
#################


header_label = tk.Label(root, text="Welcome to PyCA", font=("Helvetica", 18))
header_label.grid(row=0, column=0, columnspan=5,
                  pady=20, padx=20, sticky="nsew")

label1 = tk.Label(root, text="Generate default new stage:", font=("Helvetica", 10))
label1.grid(row=1, column=0)

#####
# LOG FUNC
#####
frame = tk.Frame(root)
root.rowconfigure(10, weight=1)
frame.grid(row=10, column=0, columnspan=4, rowspan=999, sticky="nsew", padx=10, pady=10)

# Create a Text widget to display the log
log_text = tk.Text(frame)
log_text.pack(side=tk.RIGHT)

# Create a Scrollbar widget and link it to the Text widget
scrollbar = tk.Scrollbar(frame, command=log_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
log_text.configure(yscrollcommand=scrollbar.set)


# Function to append a message to the log
def log(message) -> None:
    """
      Appends a message to the log Text widget.
    """
    log_text.insert(tk.END, message + "\n")
    # Scroll to the end of the widget
    log_text.see(tk.END)
    # Update the widget
    log_text.update()


log("Welcome to PyCA software!")

#######
# Stage
#######

# Creamos un boton para el escenario stage
button1 = tk.Button(root, text="Square", command=generate_new_square, bg = "orange")
button1.grid(row=1, column=1, padx=5, pady=10)

# Creamos un boton para el escenario stage
button2 = tk.Button(root, text="Hexagon", command=generate_new_hexagon, bg = "orange")
button2.grid(row=1, column=2, padx=5, pady=10)

# Creamos un boton para el escenario stage
button3 = tk.Button(root, text="Voronoi", command=generate_new_Voronoi, bg = "orange")
button3.grid(row=1, column=3, padx=5, pady=10)

#######
# Controls
#######
button_controls = tk.Button(root, text="Show controls", command=show_controls, bg = "pink")
button_controls.grid(row=0, column=2,columnspan=3, padx=10, pady=1 )
#######
# CHANGE COLOR CELLS
#######


def change_color1() -> None:
    """
     Opens a color chooser window and updates the
     COLOR_JUST_BORN global variable with the chosen color.
    """
    color = colorchooser.askcolor()[0]
    if color is not None:
        # global COLOR_JUST_BORN
        # COLOR_JUST_BORN = color
        stage.COLOR_JUST_BORN = color
        log(
            f"Newborn cells will be shown in this new color: {color} (RGB)")


def change_color2() -> None:
    """
       Opens a color chooser window and updates the
       COLOR_JUST_SURVIVED global variable with the chosen color.
    """
    color = colorchooser.askcolor()[0]
    if color is not None:
        # global COLOR_SURVIVED
        # COLOR_SURVIVED = color
        stage.COLOR_SURVIVED = color
        log(
            f"Survivor cells will be shown in this new color: {color} (RGB)")


color1 = tk.Label(root, text="Newborn cells color:", font=("Helvetica", 10))
color1.grid(row=2, column=0, padx=5, pady=5)

btnc1 = tk.Button(root, text="Change Color", command=change_color1)
btnc1.grid(row=2, column=1)

color2 = tk.Label(root, text="Survivor cells color:", font=("Helvetica", 10))
color2.grid(row=2, column=2)

btnc2 = tk.Button(root, text="Change Color", command=change_color2)
btnc2.grid(row=2, column=3)

#####################
# Function that applies fps, size, initial_alife_probability
# and rule changes all at once
#####################
def apply_changes() -> None:
    global stage
    global frame_rate
    frame_rate = scale_time.get()
    
    value = scale_alive.get()
    size = scale.get()
    # TODO: AÑADIR LOS COLORES Y RESTO DE PARÁMETROS CUANDO ENTREMOS AQUÍ
    if stage_st == "HEX":
        stage = Hexagon(game_surface, initial_alive_probability=value/100, L=size)
    elif stage_st == "SQU":
        stage = Square(game_surface, initial_alive_probability=value/100, L=size)
    elif stage_st == "VOR":
        stage = VoronoiGrid(game_surface, initial_alive_probability=value/100, L=size)
    
    msg = label7.get()
    if is_rule_valid(msg):
        global alive_neighbours_to_be_born
        global alive_neighbours_to_survive
        alive_neighbours_to_be_born, alive_neighbours_to_survive = parser_rule(msg)
        stage.alive_neighbours_to_be_born = alive_neighbours_to_be_born
        stage.alive_neighbours_to_survive = alive_neighbours_to_survive
    
    stage.change_caption()
    pygame.display.update()
#####################
# L system
#####################

changeL = tk.Label(root, text="Cell size:", font=("Helvetica", 10))
changeL.grid(row=3, column=0, columnspan=1)

scale = tk.Scale(from_=3, to=50, digits=3,
                 orient=tk.HORIZONTAL, resolution=0.001)
scale.grid(row=3, column=1, columnspan=1)
scale.set(5)

btnL = tk.Button(root, text="Set Size", command=apply_changes)
btnL.grid(row=3, column=2)

#######
# RULES
#######

rules = tk.Label(root, text="Create custom rule (B.../S...):", font=("Helvetica", 10))
rules.grid(row=4, column=0)
example_rules = ["B2/S2","B3/S23 (Original Game of Life!)","B23/S (no possible survivors!)", \
                 "B0123456789/S0123456789 (infinite growth and survival!)", "B123/S34","B0/S24" \
                ,"B58/S13","B347/S126","B1/S0 (only isolated cells survive)","B2/S345"]

label7 = tk.Entry(root)
label7.grid(row=4, column=1, padx=5, pady=15)


def send_selected_rule() -> None:
    """
    Send rule to the system
    """
    msg = label7.get()
    if is_rule_valid(msg):
        global alive_neighbours_to_be_born
        global alive_neighbours_to_survive
        alive_neighbours_to_be_born, alive_neighbours_to_survive = parser_rule(
            msg)
        stage.alive_neighbours_to_be_born = alive_neighbours_to_be_born
        stage.alive_neighbours_to_survive = alive_neighbours_to_survive
        # print(alive_neighbours_to_be_born)
        # print(stage.alive_neighbours_to_be_born)
        # print(alive_neighbours_to_survive)
        # print(stage.alive_neighbours_to_survive)

        log(f"The new rule is: {msg}")
    else:
        log(f"The rule {msg} is invalid. Please set a valid rule")
        log("Example of valid rule: " + example_rules[np.random.randint(len(example_rules))])
    stage.change_caption()                                        
    

def is_rule_valid(rule: str) -> bool:
    """
    Check if rule is valid

    Example:
      is_rule_valid("B3/S23") # True
      is_rule_valid("B99/S45") # False, in B variable there're duplicate elements
      is_rule_valid("B19/S43") # False, in S the numbers aren't ordered
    """
    def is_asc_unique(ls: str) -> bool:
        """
        check if string hasn't any duplicates and the values are sorted ascending
        """
        nums = [int(x) for x in ls]
        # Check if numbers are in ascending order
        for i in range(1, len(nums)):
            if nums[i] < nums[i-1]:
                return False
        # Check if exist duplicates
        if len(nums) != len(set(nums)):
            return False
        return True
    # If the pattern match with a rule
    if re.match(r"^B([0-9]{1,10})/S([0-9]{1,10})$", rule) \
        or re.match(r"^B([0-9]{1,10})/S$", rule) or \
        re.match(r"^B/S([0-9]{1,10})$", rule) or rule == "B/S":
        # Split the rule
        b, s = rule.split("/")
        if is_asc_unique(b[1:]) and is_asc_unique(s[1:]):
            return True
        elif (is_asc_unique(b[1:]) and s == "S") or (b=="B" and is_asc_unique(s[1:])) \
            or (rule == "B/S"):
            return True
    return False


def parser_rule(rule: str) -> Tuple[list, list]:
    """
    Generate a tuple of list that each list is numbers of neighbours
    """
    b, s = rule.split("/")
    born = [int(x) for x in b if x.isdigit()]
    surv = [int(x) for x in s if x.isdigit()]
    return born, surv


send_rule = tk.Button(root, text="Set Rule", command=send_selected_rule)
send_rule.grid(row=4, column=2)

########
# Alive probability
########
alive = tk.Label(root, text="Initial alive cells (%):", font=("Helvetica", 10))
alive.grid(row=5, column=0, columnspan=1)

scale_alive = tk.Scale(from_=0, to=100, digits=1,
                       orient=tk.HORIZONTAL, resolution=0.01)
scale_alive.grid(row=5, column=1, columnspan=1)

btnL = tk.Button(root, text="Set %", command=apply_changes)
btnL.grid(row=5, column=2)

########
# TIME
########
time_label = tk.Label(root, text="Frames per second:", font=("Helvetica", 10))
time_label.grid(row=6, column=0, columnspan=1)

scale_time = tk.Scale(from_=5, to=120, digits=3,
                      orient=tk.HORIZONTAL, resolution=0.001)
scale_time.grid(row=6, column=1, columnspan=1)
scale_time.set(15)

def apply_time() -> None:
    global frame_rate
    frame_rate = scale_time.get()

btnL = tk.Button(root, text="Set FPS", command=apply_time)
btnL.grid(row=6, column=2)


def global_handle_events() -> None:
    stage_log_state_A = stage.log_state
    stage.handle_events()
    stage_log_state_B = stage.log_state
    if stage_log_state_A != stage_log_state_B:
        log(stage.message)

###########
# Main Loop
###########

# Create a Clock object to control the frame rate
clock = pygame.time.Clock()

# Close tkinter and pygame simus
def close_windows():
    pygame.display.quit()
    pygame.quit()
    root.destroy()

# Set the close_windows function to be called when the tkinter window is closed
root.protocol("WM_DELETE_WINDOW", close_windows)


while True:
    # Update the Stage (Square, Hexagon, Voronoi)
    global_handle_events()
    if stage.running:
        stage.update()
        # Limit the frame rate to the desired value
        clock.tick(frame_rate)

    # Update the Tkinter interface
    root.update()


