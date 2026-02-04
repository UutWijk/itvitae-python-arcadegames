import pygame
import os
from player import Player

pygame.init()


class Score:
    def __init__(self, player: Player, highscore):
        self.player = player
        self.highscore = highscore
        self._score = 0
        self._multiplier = player.get_modifier()

        if os.name == "posix":
            self.path = os.path.join("..", "assets", "fontPixel.ttf")
        elif os.name == "nt":
            self.path = os.path.join("assets", "fontPixel.ttf")

        self.font = pygame.font.Font(self.path, size=50)

    def update(self, dt: float):
        # dt isn't used, but is added for compatibility with other classes that use an update function

        self._score = self.player.get_score()

        self._multiplier = self.player.get_modifier()

        self.surface = self.font.render(
            f"Score: {self._score}", antialias=True, color="white"
        )
        current_high = self.highscore.get_highscore()
        self.highscore_surface = self.font.render(
            f"High Score: {current_high}", antialias=True, color="white"
        )

        self.mult_surface = self.font.render(
            f"multiplier: {self._multiplier}", antialias=True, color="white"
        )

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surface, (50, 840))
        screen.blit(
            self.highscore_surface, (1280 - self.highscore_surface.width - 50, 870)
        )
        screen.blit(self.mult_surface, (50, 890))

    def reset(self):
        self._score = 0
        self.player._score = 0
