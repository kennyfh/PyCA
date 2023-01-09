#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Module: Stage
# Created By  : TEODORO JIMÉNEZ LEPE
#               KENNY JESÚS FLORES HUAMÁN
# version ='1.0'
# ---------------------------------------------------------------------------
# Parent class where the 3 scenarios will be created: Quadratic, Hexagonal and Voronoi
# ---------------------------------------------------------------------------
import time
import pygame
import imageio
import os

COLOR_BLACK = (10, 10, 10)
COLOR_WHITE = (255, 255, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)

COLOR_GRID = (40, 40, 40)

# EVANGELION_GREEN = (10,144,98)
# EVANGELION_PURPLE = (157,68,199)

################################################################################################################################################
# Parameters that should be controled by the user through tkinter interface:
################################################################################################################################################

# Customize birth and survival colors!
COLOR_JUST_BORN = COLOR_GREEN
COLOR_SURVIVED = COLOR_RED

# Create your own rules based on number of neighbours!
alive_neighbours_to_be_born = [2]
alive_neighbours_to_survive = [2]

# B1S- makes cool patterns
# B-S123456 too
# B2S2 shows some blinkers and is similar to B2S23 square grid in proportion to neighbourhood
# Check B2S345 and others B2S-
# Look for reference of previous works (some rules show gliders)


# These are constant values: (screen dimensions)
Lx = 800
Ly = 600


class Stage:
    """
    A base class for generating and visualizing cellular automata stages.

    Args:
        surface (pygame.Surface): The surface on which the stage will be drawn.
        L (int, optional): The size of the cells in the stage. Default is 10.
        COLOR_JUST_BORN (Tuple[int, int, int], optional): The color of cells that are born in a given step. Default is (255, 255, 255).
        COLOR_SURVIVED (Tuple[int, int, int], optional): The color of cells that survive to the next step. Default is (255, 255, 255).
        alive_neighbours_to_be_born (List[int], optional): A list of the number of alive neighbors required for a cell to be born. Default is [3].
        alive_neighbours_to_survive (List[int], optional): A list of the number of alive neighbors required for a cell to survive. Default is [2, 3].
        initial_alive_probability (float, optional): The probability that a cell will be initially alive. Default is 0.
    """

    def __init__(self,
                 surface,
                 L=10,
                 COLOR_JUST_BORN=(255, 255, 255),
                 COLOR_SURVIVED=(255, 255, 255),
                 alive_neighbours_to_be_born=[3],
                 alive_neighbours_to_survive=[2, 3],
                 initial_alive_probability=0) -> None:

        self.surface = surface
        self.L = L
        self.COLOR_JUST_BORN = COLOR_JUST_BORN
        self.COLOR_SURVIVED = COLOR_SURVIVED
        self.alive_neighbours_to_be_born = alive_neighbours_to_be_born
        self.alive_neighbours_to_survive = alive_neighbours_to_survive
        self.initial_alive_probability = initial_alive_probability
        # Generate gifs
        self.writer = None
        self.count_writer = 0
        # Attribute to communicate with main log
        self.log_state = 0
        # Message for global log
        self.message = None
        # Set the running flag to False
        self.running = False
        # Set the recording flag to False
        self.recording = False
        self.stage_name = "Stage"


    def log(self, message) -> None:
        self.message = message
        self.log_state = self.log_state + 1

    def update(self):
        pass

    # Handle pygame events: mainly user instructions
    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:  # Check if any key gets pressed down
                if event.key == pygame.K_SPACE:  # Check if spacebar gets pressed down
                    self.running = not self.running  # Pause and resume button
                elif event.key == pygame.K_RIGHT:  # Check if right arrow gets pressed down
                    # This key allows single step update in order to
                    # watch evolution in detail:
                    self.running = False
                    self.update()
                elif event.key == pygame.K_DOWN:  # Check if down arrow gets pressed down
                    self.running = False
                    # fun1
                    self.key_down()
                    pygame.display.update()
                # elif event.key == pygame.K_s: # Check if s key gets pressed down
                #     self.recording = not self.recording
                #     self.change_caption()
                #     if self.recording:
                #         self.screenshot()
                elif event.key == pygame.K_r:
                    self.recording = not self.recording
                    self.change_caption()
                    if self.recording:
                        self.writer = imageio.get_writer(self.stage_name + self.rule.replace(
                            '/', '_') + "_"+str(pygame.time.get_ticks())+".gif", mode='I', fps=1)
                        self.count_writer = 0
                        self.record()
                    # If get pressed down and the list of images is not empty:
                    elif (not self.recording) and (self.count_writer > 0):
                        self.writer.close()

            if pygame.mouse.get_pressed()[0]:  # True if left-click
                # fun2
                self.left_click()

            elif pygame.mouse.get_pressed()[2]:  # True if right-click
                # fun3
                self.right_click()

            # Analogous action that prints number of alive neighbours on terminal.
            # This is mainly implemented for troubleshooting.
            # Central mouse button (mouse wheel)
            elif pygame.mouse.get_pressed()[1]:
                # fun 4
                self.mouse_wheel()

    # Special key events
    def key_down(self) -> None:
        pass

    def left_click(self) -> None:
        pass

    def right_click(self) -> None:
        pass

    def mouse_wheel(self) -> None:
        pass

    def run(self) -> None:
        # Main loop
        while True:
            self.handle_events()
            if self.running:
                time.sleep(0.01)
                self.update()

    def change_caption(self) -> None:
        # Processing window caption:
        birth_string = [str(x) for x in self.alive_neighbours_to_be_born]
        survival_string = [str(x) for x in self.alive_neighbours_to_survive]
        self.rule = 'B'+"".join(birth_string)+'S'+"".join(survival_string)
        if self.recording:
            caption = 'B'+"".join(birth_string)+'/S'+"".join(survival_string) + \
                ' in ' + self.stage_name + ' grid (RECORDING SCREEN)'
        else:
            caption = 'B'+"".join(birth_string)+'/S' + \
                "".join(survival_string) + ' in ' + self.stage_name + ' grid'
        pygame.display.set_caption(caption)

    def show_controls(self):
        pass

    def screenshot(self) -> None:
        # Save screen in a folder
        if self.recording:
            newpath = os.path.join(
                "saved_images", self.stage_name, self.rule.replace('/', '_'))
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            # pygame.image.save(self.surface, "saved_images/"+ self.stage_name + self.rule.replace('/','_') +"/"+str(pygame.time.get_ticks())+".png")
            path = os.path.join("saved_images",
                                self.stage_name, self.rule.replace('/', '_'),
                                str(pygame.time.get_ticks()), ".png")
            pygame.image.save(self.surface, path)

    def record(self) -> None:
        if self.recording:
            # Save frame
            frame = pygame.surfarray.array3d(pygame.display.get_surface())
            self.writer.append_data(frame)
            self.count_writer += 1
