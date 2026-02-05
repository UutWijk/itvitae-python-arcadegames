
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):

    # position and angle set in constructor
    # - kills = False for bullets that only add as "particle effects"
    # - ufo if bullet was shot by ufo (kills player, doesnt affect asteroids)
    # - speed can be adapted for ufo-shot bullets and particle effects
    def __init__(self, x, y, angle, lifetime=1, speed=1000, kills=True, ufo=False):
        super().__init__()

        # bullet is just a small 4x4 square pixel
        self.image = pygame.Surface((4, 4))
        self.image.fill(("#ffffff"))
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        # position variables
        self.pos = pygame.Vector2(x, y)
        self.speed = speed

        # had to flip angle and speed for standardization with other game objects
        self.velocity = pygame.Vector2(0, -self.speed).rotate(-angle)

        # set other constructor values
        self.lifetime = lifetime
        self.kills = kills
        self.ufo = ufo

    def update(self, dt):
        self.pos += self.velocity * dt
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
        self.rect.center = self.pos





