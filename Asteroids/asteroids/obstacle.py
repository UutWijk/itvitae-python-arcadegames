import math
import os
import pygame
from pygame.sprite import Sprite, Group
import random

class Obstacle(Sprite):
    
    def __init__(self, x, y, screenwidth, screenheight, stage=1):
        super().__init__()
        SCALE = 0.4
        self.speed = 100

        # set scale and speed based on stage
        match stage:
            case 1:
                SCALE = 0.35
                self.speed = random.randint(50, 150)
            case 2:
                SCALE = 0.2
                self.speed = random.randint(75, 200)
            case 3:
                SCALE = 0.125
                self.speed = random.randint(100, 300)
        self.stage = stage
        self.screenwidth = screenwidth
        self.screenheight = screenheight

        # asset loading
        spritechoice = "sprites/asteroid" + str(random.randint(1,5))
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.image = pygame.image.load(os.path.join(current_dir, spritechoice + ".png")).convert_alpha()
        self.maskimage = pygame.image.load(os.path.join(current_dir, spritechoice + "_mask.png")).convert_alpha()

        # transforming image and mask for in-game size
        w, h = self.image.get_size()
        self.image = pygame.transform.smoothscale(
            self.image,
            (int(w * SCALE), int(h * SCALE)))
        self.maskimage = pygame.transform.smoothscale(
            self.maskimage,
            (int(w * SCALE), int(h * SCALE)))
        rotation = random.randrange(0, 360)
        self.image = pygame.transform.rotate(self.image, rotation)
        self.maskimage = pygame.transform.rotate(self.maskimage, rotation)
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.maskimage)

        # define position and random rotation (so its less obvious there are only 5 sprites)
        self.pos = pygame.Vector2(x, y)
        self.angle = random.randrange(0, 360)

        # had to flip angle and speed for standardization with other game objects
        self.velocity = pygame.Vector2(0, -self.speed).rotate(-self.angle)

    # split into two unless last stage
    def killed(self):
        self.kill()
        if self.stage < 3:            
            return [Obstacle(self.pos.x, self.pos.y, self.screenwidth, self.screenheight, self.stage + 1),
                    Obstacle(self.pos.x, self.pos.y, self.screenwidth, self.screenheight, self.stage + 1)]
            
    def update(self, dt):
        # Move asteroid
        self.pos += self.velocity * dt

        # Use half of the rect's width and height (original image) for wrapping
        half_w = self.rect.width / 2
        half_h = self.rect.height / 2

        # Wrap horizontally
        if self.pos.x < -half_w:
            self.pos.x = self.screenwidth + half_w
        elif self.pos.x > self.screenwidth + half_w:
            self.pos.x = -half_w

        # Wrap vertically
        if self.pos.y < -half_h:
            self.pos.y = self.screenheight + half_h
        elif self.pos.y > self.screenheight + half_h:
            self.pos.y = -half_h

        # Sync rect to position
        self.rect.center = self.pos


    def draw(self,surface):
        surface.blit(self.image, self.rect)
        