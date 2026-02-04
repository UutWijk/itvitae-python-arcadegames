import pygame
from GameObject import GameObject
from assets import bunker_sprite
from constants import *

pygame.init()

class Bunker(GameObject):

    #create bunkers
    def __init__(self, bunker_position_x: float, bunker_position_y: float):
        self.original_image = pygame.image.load(bunker_sprite).convert_alpha()
        self.original_image = pygame.transform.scale_by(self.original_image, GAME_SCALE)

        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(left=bunker_position_x, top=bunker_position_y)

        self.lives = 5
        self.dead = False
        self.flash_timer = 0

    #bunkers are static, they don't need to be checked every frame.
    def update(self, delta):
        if self.flash_timer > 0:
            self.flash_timer -= delta
            if self.flash_timer <= 0:
                self.image = self.original_image
        pass
    
    #draw bunkers
    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

    def destruction(self, lives: int):
        self.lives = lives
        self.image = self.original_image.copy()
        self.image.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_ADD)

        self.flash_timer = 0.1
        if self.lives <= 0:
            self.dead = True

def spawn_bunkers() -> list[Bunker]:
    y = 500 * GAME_SCALE
    return [Bunker(110 * GAME_SCALE, y),
            Bunker(330 * GAME_SCALE, y),
            Bunker(550 * GAME_SCALE, y),
            Bunker(770 * GAME_SCALE, y)]