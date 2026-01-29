
import pygame
from state import State


class Game(State):
    def __init__(self, screen) -> None:
        super().__init__(screen)