import pygame
from pygame.key import ScancodeWrapper


pygame.init()


class Input_Handling:
    def get_input(
        self,
    ) -> ScancodeWrapper:  # get_just_pressed() returns a ScancodeWrapper
        keys = pygame.key.get_just_pressed()
        return keys
