import pygame
from pygame.sprite import Sprite, Group
from menu import MainMenu

# import game classes
from Asteroids.asteroids.asteroids import Asteroids
from Blockade.blockade.blockade import Blockade
from Tetris.tetris import Tetris
from Pong.src.game import Pong
from Frogger.scripts.main import Frogger
from Space_Invaders.space_invaders import SpaceInvaders



import os
import sys

pygame.init()

FPS = 60
clock = pygame.time.Clock()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
DISPLAY_SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Arcade")
icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "menu_assets", "capgemini_logos", "capgemini_logo_spade.png")
icon_image = pygame.image.load(icon_path)
pygame.display.set_icon(icon_image)

# add classes ineriting from Game(State) to game list
states = {
    "Asteroids": Asteroids,
    "Blockade": Blockade,
    "Pong": Pong,
    "Tetris": Tetris,
    "Frogger": Frogger,
    "Space Invaders": SpaceInvaders,
}
games = list(states.keys())
current_state_key = "MENU"
current_state = MainMenu(DISPLAY_SCREEN, games)

# state switching logic
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
    dt = (
        clock.tick(FPS) / 1000
    ) # dt = 0.01666...

    if current_state.next_state:
        change_state(current_state.next_state)

    # event handling
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        current_state.handle_events(event)


    # call update and draw for current state
    current_state.update(dt)
    current_state.draw()
    current_state.reset_just_pressed()
    pygame.display.flip()
