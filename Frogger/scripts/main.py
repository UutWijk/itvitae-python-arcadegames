import pygame
import sys
import os
from .player import Player
from .level import Level
from .score import Score
from .gameover import GameOver
from .highscore import HighScore
from .next_level import NextLevel
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
from .lives_counter import LivesCounter
from game import Game


class Frogger(Game):
    def __init__(self, screen):
        super().__init__(screen)
        self.FPS = 60
        # SCREENX = 1280
        # SCREENY = 960
        # SCREEN_RES = pygame.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT)  # Screen resolution
        self.screen = screen
        # pygame.display.set_caption("Frogger")
        self.clock = pygame.time.Clock()

        self.player = Player(
            pygame.Vector2(SCREEN_WIDTH / 2 - TILE_SIZE / 2, SCREEN_HEIGHT - TILE_SIZE)
        )  # location is defined in a not-so-neat manner, subject to change. Player starts out in the bottom-middle of the screen.
        self.highscore = HighScore()
        self.score = Score(self.player, self.highscore)
        self.lives_counter = LivesCounter(self.player)

        self.nextlevel = NextLevel()

        self.game_over = GameOver(self.player, self.highscore)

        self.level = Level(self.player, self.game_over, self.highscore, self.nextlevel)

    def update(self, dt):
        # if event.type == pygame.KEYDOWN:
        #    if event.key == pygame.K_SPACE and game_over.game_over:
        #        level.restart()
        #        score.reset()

        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_a] and self.level.game_over:
            self.level.restart()
            self.score.reset()
        if keys[pygame.K_b] and self.level.game_over:
            self.next_state = "MENU"
            pass

        self.level.update(dt)
        self.player.update(dt)
        self.score.update(dt)
        self.game_over.update(dt)
        self.nextlevel.update(dt)

        # dt = self.clock.tick(self.FPS) / 1000  # delta time

    def draw(self):
        self.level.draw(self.screen)
        self.player.draw(self.screen)
        self.score.draw(self.screen)
        self.lives_counter.draw(self.screen)
        self.game_over.draw(self.screen)
        self.nextlevel.draw(self.screen)
