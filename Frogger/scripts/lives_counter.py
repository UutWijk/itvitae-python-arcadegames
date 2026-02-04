import pygame
import os
import sys
from Frogger.scripts.player import Player
from Frogger.scripts.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class LivesCounter:
    def __init__(self, player: Player):
        self.player = player

        # if os.name == "posix":
        #    self.path = os.path.join("..", "assets", "Frog.png")
        # elif os.name == "nt":
        #    self.path = os.path.join("assets", "Frog.png")
        curr_dir = os.path.dirname(__file__)
        self.path = os.path.join(curr_dir, "..", "assets", "Frog.png")

        self.sprite = pygame.transform.scale_by(pygame.image.load(self.path), 0.75)

    def draw(self, screen: pygame.Surface):
        x_pos = SCREEN_WIDTH - self.sprite.width
        lives_icons_offset = 8
        for i in range(self.player.get_lives()):
            screen.blit(self.sprite, (x_pos, 0))
            x_pos -= self.sprite.width + lives_icons_offset
