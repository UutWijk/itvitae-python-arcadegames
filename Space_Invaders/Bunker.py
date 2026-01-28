import pygame
from GameObject import GameObject
from assets import bunker_sprite
from constants import *

pygame.init()

class Bunker(GameObject):

    def __init__(self, bunker_position_x: float, bunker_position_y: float):
        self.image = pygame.image.load(bunker_sprite)
        self.rect = self.image.get_rect(left=bunker_position_x, top=bunker_position_y)

    def update(self, delta):
        pass

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

