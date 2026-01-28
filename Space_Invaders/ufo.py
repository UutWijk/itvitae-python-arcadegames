import pygame
from GameObject import GameObject
from constants import *
from assets import ufo_sprite



class Ufo(GameObject):

    def __init__(self):

        self.image = pygame.image.load(ufo_sprite)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH + 200, 50))
        self.direction = 0
        

    def update(self, delta):
        timer = pygame.time.get_ticks()

        if 9900 < timer <= 10100:
            self.direction = -1

        if -105 < self.rect.x <= -95:
            self.direction = 1

        if SCREEN_WIDTH + 95 < self.rect.x <= SCREEN_WIDTH + 105:
            self.direction = -1

        self.rect.move_ip(200 * self.direction * delta, 0)

    def draw(self, surface: pygame.Surface):

        image_rect = self.image.get_rect(center=(self.rect.x, self.rect.y))
        surface.blit(self.image, image_rect)

