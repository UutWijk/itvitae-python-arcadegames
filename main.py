import pygame
from pygame.sprite import Sprite, Group
from menu import MainMenu
from Asteroids.asteroids.asteroids import Asteroids
from Blockade.blockade.blockade import Blockade
from Tetris.tetris import Tetris
from Pong.src.game import Pong
# voeg hier de import toe van de game class die van Game(State) erft

import os
import sys

pygame.init()

FPS = 60
clock = pygame.time.Clock()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
DISPLAY_SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Arcade")


# voeg de geimporteerde class toe aan deze dictionary
states = {
    "Asteroids": Asteroids,
    "Blockade": Blockade,
    "Pong": Pong,
    "Tetris": Tetris,
}
games = states.keys()
current_state_key = "MENU"
current_state = MainMenu(DISPLAY_SCREEN, games)

def change_state(key):
    global current_state, current_state_key
    current_state.next_state = None
    if key in states:
        current_state = states[key](DISPLAY_SCREEN)
        current_state_key = key
        pygame.display.set_caption(type(states[key]).__name__)
    elif key == "MENU":
        current_state = MainMenu(DISPLAY_SCREEN, games)
        current_state_key = "MENU"
        pygame.display.set_caption("Select a game...")


while True:  
    dt = clock.tick(FPS)/1000 # dt is ongeveer 16.67 milliseconden (1/60 van een seconde)

    # logica voor het wisselen van state
    if current_state.next_state:
        change_state(current_state.next_state)

    # deze loop draait dus op 60FPS (houd hier rekening mee als je gameloop op een andere tick rate draait)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        current_state.handle_events(event)

    # update en draw aanroepen voor de huidige state
    current_state.update(dt)
    current_state.draw()
    current_state.reset_just_pressed()
    pygame.display.flip()
