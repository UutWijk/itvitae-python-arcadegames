import random
import pygame
import math
from pygame.sprite import Sprite, Group


class Bullet(Sprite):

    # Attributes die we nodig hebben zijn positie en de hoek. 
    def __init__(self, x, y, angle, lifetime=1, speed=1000, kills=True):

        # Initialiseer de parent Sprite class. 
        super().__init__()
        # Surface maken, vullen met een kleur, Rect maken van de Surface
        self.image = pygame.Surface((4, 4))
        self.image.fill(("#ffffff")) # Classic witte bullet
        self.rect = self.image.get_rect(center=(x, y)) # midden van Rect gekoppeld aan x en y coördinaten
        self.mask = pygame.mask.from_surface(self.image)
        # Bewegingseigenschappen met behulp van Vectors. 
        # Pygame-CE's Vector2 zouden hiervoor perfect moeten zijn volgens Gemini.
        self.pos = pygame.Vector2(x, y)
        self.speed = speed # Dit later nog aanpassen naar resolutie. 
        # Maak een vector gebaseerd op de hoek van het schip 
        self.velocity = pygame.Vector2(0, -self.speed).rotate(-angle) # We gaan ervan uit dat 0 graden UP is; kunnen we wijzigen

        self.lifetime = lifetime
        self.kills = kills

    def update(self, dt):
        # Verplaatst de position vector. 
        self.pos += self.velocity * dt
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
        # Update de actuele REect positie. 
        self.rect.center = self.pos





