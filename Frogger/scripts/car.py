import pygame
import os
import random
from pygame import Rect, Color
from constants import TILE_SIZE


class Car:
    def __init__(self, x: int, y: int, driving_rightwards: bool, speed: float):
        if os.name == "posix":
            self.path = os.path.join("..", "assets", "Car.png")
            self.path2 = os.path.join("..", "assets", "Car2.png")
        elif os.name == "nt":
            self.path = os.path.join("assets", "Car.png")
            self.path2 = os.path.join("assets", "Car2.png")
        else:
            print("Error with asset loading, please report")
            sys.exit()
        if random.randint(0, 1) == 0:
            self.sprite = pygame.image.load(self.path2)
        else:
            self.sprite = pygame.image.load(self.path)
        if driving_rightwards:
            self.sprite = pygame.transform.flip(self.sprite, True, False)
        self.hitbox = Rect(x, y, TILE_SIZE * 2, TILE_SIZE)
        self.driving_rightwards = driving_rightwards
        self.speed = speed

    def update(self, dt: float):
        movement = int(self.speed * dt)
        if not self.driving_rightwards:
            movement *= -1
        self.hitbox.x += movement

    def draw(self, surface: pygame.Surface):
        surface.blit(self.sprite, self.hitbox)