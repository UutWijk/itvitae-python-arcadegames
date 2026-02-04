import pygame
import sys
from .player import Player
from .level import Level
from .score import Score
from .gameover import GameOver
from .highscore import HighScore
from game import Game
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE


# pygame.init()
FPS = 60
# SCREENX = 1280
# SCREENY = 960
SCREEN_RES = pygame.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT)  # Screen resolution
# screen = pygame.display.set_mode(SCREEN_RES)
pygame.display.set_caption("Frogger")
clock = pygame.time.Clock()

class Frogger(Game):
        
    def __init__(self, screen):
        super().__init__(screen)
        self.player = Player(
            pygame.Vector2(SCREEN_WIDTH / 2 - TILE_SIZE / 2, SCREEN_HEIGHT - TILE_SIZE)
        )  # location is defined in a not-so-neat manner, subject to change. Player starts out in the bottom-middle of the screen.
        self.highscore = HighScore()
        self.score = Score(self.player, self.highscore)

        self.game_over = GameOver(self.player, self.highscore)
        self.level = Level(self.player, self.game_over, self.highscore)


    def update(self, dt):
        


        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_SPACE] and self.level.game_over:
            self.level.restart()
            self.score.reset()

        self.level.update(dt)
        self.player.update()
        self.score.update(dt)
        self.game_over.update(dt)

    def draw(self):
        self.level.draw(self.screen)
        self.player.draw(self.screen)
        self.score.draw(self.screen)
        self.game_over.draw(self.screen)



