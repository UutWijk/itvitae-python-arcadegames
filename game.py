
import pygame
from state import State


class Game(State):
    def __init__(self, screen, multiplayer = False) -> None:
        super().__init__(screen, multiplayer)