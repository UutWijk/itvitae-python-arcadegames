import pygame
import os
from player import Player

pygame.init()


class Score:
    def __init__(self, player: Player, highscore):
        self.player = player
        self.highscore = highscore
        self._score = 0

        if os.name == "posix":
            self.path = os.path.join("..", "assets", "font.ttf")
        elif os.name == "nt":
            self.path = os.path.join("assets", "font.ttf")

        self.font = pygame.font.Font(self.path, size=50)

    def update(self, dt: float):
        # dt isn't used, but is added for compatibility with other classes that use an update function

        self._score = self.player.get_score()

        self.surface = self.font.render(str(self._score), antialias=True, color="black")
        current_high = self.highscore.get_highscore()
        self.highscore_surface = self.font.render(
            f"High Score: {current_high}", antialias=True, color="white"
        )
    def draw(self, screen: pygame.Surface):
        screen.blit(self.surface, (50, 50))
        screen.blit(self.highscore_surface, (50, 110))

    def reset(self):
        self._score = 0
        self.player._score = 0