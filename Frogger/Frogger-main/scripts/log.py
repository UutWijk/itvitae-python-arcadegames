import pygame
import os
from constants import SCREEN_WIDTH

class Log:
    def __init__(self, x, y):
        # Load log image
        script_dir = os.path.dirname(__file__)
        log_path = os.path.join(script_dir, '..', 'assets', 'LogWater.png')
        self.image = pygame.image.load(log_path).convert_alpha()
        
        # Scale to 3 tiles wide (192px) and keep original height (or set to 48)
        self.image = pygame.transform.scale(self.image, (192, 48))
        
        self.rect = self.image.get_rect(topleft=(x, y))
        
    def update(self, speed_x):
        self.rect.x += speed_x
        
        # Wrap around screen
        if speed_x > 0:
            if self.rect.left > SCREEN_WIDTH:
                self.rect.right = 0
        else:
            if self.rect.right < 0:
                self.rect.left = SCREEN_WIDTH
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)