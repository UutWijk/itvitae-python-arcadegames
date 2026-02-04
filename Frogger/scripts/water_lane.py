import os
import pygame
from log import Log
from constants import TILE_SIZE, SCREEN_WIDTH

class WaterLane:
    def __init__(self, y_pos, moving_right, speed, log_count):
        self.y_pos = y_pos
        self.height = TILE_SIZE
        self.speed_x = speed if moving_right else -speed
        # self.water_color = (0, 119, 190)

        script_dir = os.path.dirname(__file__)
        water_path = os.path.join(script_dir, '..', 'assets', 'Water.png')
        self.water_image = pygame.image.load(water_path).convert_alpha()

        self.logs = []
        
        spacing = SCREEN_WIDTH // log_count
        for i in range(log_count):
            x = i * spacing
            log = Log(x, y_pos + 8)
            self.logs.append(log)
    
    def update(self):
        for log in self.logs:
            log.update(self.speed_x)
    
    def draw(self, screen):
        tile_width = self.water_image.get_width()
        for x in range(0, SCREEN_WIDTH, tile_width):
            screen.blit(self.water_image, (x, self.y_pos))
        
        for log in self.logs:
            log.draw(screen)

    def get_log_at_position(self, player_rect): # Check if player is on a log with sufficient overlap.
        MIN_OVERLAP = 25  # Require 20px overlap to count as "on log"
        
        for log in self.logs:
            if player_rect.colliderect(log.rect):
                # Calculate overlap dimensions
                overlap_width = min(player_rect.right, log.rect.right) - max(player_rect.left, log.rect.left)
                overlap_height = min(player_rect.bottom, log.rect.bottom) - max(player_rect.top, log.rect.top)
                
                # Both dimensions must meet minimum overlap
                if overlap_width >= MIN_OVERLAP and overlap_height >= MIN_OVERLAP:
                    return log
        return None