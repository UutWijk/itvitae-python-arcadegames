import pygame
import sys
import os

from player import Player
from highscore import HighScore
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class GameOver:
    def __init__(self, player: Player, highscore: HighScore):
        if os.name == "nt":
            self.path_game_over = os.path.join("assets", "Gameover.png")
            self.path_score = os.path.join("assets", "Score.png")
            self.path_press_space = os.path.join("assets", "PressSpace.png")
            self.path_press_a = os.path.join("assets", "PressA.png")
            self.path_font = os.path.join("assets", "fontPixel.ttf")
            self.font = pygame.Font(self.path_font, size=120)
        elif os.name == "posix":
            try:
                self.path_game_over = os.path.join("..", "assets", "Gameover.png")
                self.path_score = os.path.join("..", "assets", "Score.png")
                self.path_press_space = os.path.join("..", "assets", "PressSpace.png")
                self.path_press_a = os.path.join("..", "assets", "PressA.png")
                self.path_font = os.path.join("..", "assets", "fontPixel.ttf")
                self.font = pygame.Font(self.path_font, size=120)
            except FileNotFoundError:
                try:
                    self.path_game_over = os.path.join("assets", "Gameover.png")
                    self.path_score = os.path.join("assets", "Score.png")
                    self.path_press_space = os.path.join("assets", "PressSpace.png")
                    self.path_press_a = os.path.join("assets", "PressA.png")
                    self.path_font = os.path.join("assets", "fontPixel.ttf")
                    self.font = pygame.Font(self.path_font, size=120)
                except FileNotFoundError:
                    print("File Gameover.png could not be loaded. Exiting.")
                    sys.exit()
        self.image_game_over = pygame.image.load(self.path_game_over)
        self.image_score = pygame.image.load(self.path_score)
        self.image_press_space = pygame.image.load(self.path_press_space)
        self.image_press_a = pygame.image.load(self.path_press_a)
        self.rect = self.image_game_over.get_rect()
        self.game_over = False
        self.curtain = 0
        self.curtainRect = pygame.Rect((0, 0), (SCREEN_WIDTH, 0))
        self.timer = 0
        self.player = player
        self.highscore = highscore
        self.n_points = self.player.get_score()

    def set_game_over(self):
        self.game_over = True

    def reset(self):
        self.game_over = False
        self.curtain = 0
        self.timer = 0

    def update(self, dt: float):
        if self.game_over:
            if self.curtain < SCREEN_HEIGHT + 20:
                self.curtain += 1000 * dt

            self.timer += dt

    def draw(self, screen: pygame.Surface):
        self.n_points = self.player.get_score()
        score_surf = self.font.render(str(self.player.get_score()), False, "white")
        hiscore_surf = self.font.render(
            str(self.highscore.get_highscore()), False, "white"
        )
        if self.game_over:
            if self.curtain < SCREEN_HEIGHT + 20:
                self.curtainRect = pygame.Rect((0, 0), (SCREEN_WIDTH, self.curtain))
            pygame.draw.rect(screen, "black", self.curtainRect)
            if self.curtain > SCREEN_HEIGHT:
                screen.blit(self.image_game_over, self.rect)
                if self.timer > 1.5:
                    screen.blit(self.image_score, self.image_score.get_rect())
                    screen.blit(score_surf, (680, 375))
                    screen.blit(hiscore_surf, (680, 525))
                if self.timer > 2 and int(self.timer) < self.timer - 0.4:
                    screen.blit(
                        self.image_press_space, self.image_press_space.get_rect()
                    )
