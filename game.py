
import pygame
from state import State


class Game(State):
    def __init__(self, screen) -> None:
        super().__init__(screen)


    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_state = "MENU" # Signal to go back
   

    def update(self, dt) -> None:
        pass

    def draw(self) -> None:
        pass