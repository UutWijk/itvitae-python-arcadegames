import pygame
from pygame.sprite import Sprite, Group
from menu import MainMenu
from Asteroids.asteroids.asteroids import Asteroids
from Frogger.Frogger.scripts.main import Frogger
from Blockade.blockade.blockade import Blockade
# from Pong.pong.src.pong import Pong
import os
import sys

# from pong.src.pong import Pong

pygame.init()

FPS = 60
clock = pygame.time.Clock()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
DISPLAY_SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("ASTEROIDS")


states = {
    "Asteroids": Asteroids(DISPLAY_SCREEN),
    "Frogger": Frogger(DISPLAY_SCREEN),
    "Blockade": Blockade(DISPLAY_SCREEN),
    # "Pong": Pong(DISPLAY_SCREEN),
}
games = states.keys()
states["MENU"] = MainMenu(DISPLAY_SCREEN, games)
current_state_key = "MENU"


while True:  
    dt = clock.tick(FPS)/1000 # Gets time since last frame
    current_state = states[current_state_key]
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        current_state.handle_events(event)

    # State Switching Logic
    if current_state.next_state:
        # Reset the current state's signal before switching
        new_key = current_state.next_state
        current_state.next_state = None 
        current_state_key = new_key

    current_state.update(dt)
    current_state.draw()
    current_state.reset_just_pressed()
    pygame.display.flip()
