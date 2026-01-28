import pygame
import sys
from player import Player
from level import Level
from score import Score
from gameover import GameOver
from highscore import HighScore
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE


pygame.init()
FPS = 60
# SCREENX = 1280
# SCREENY = 960
SCREEN_RES = pygame.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT)  # Screen resolution
screen = pygame.display.set_mode(SCREEN_RES)
pygame.display.set_caption("Frogger")
clock = pygame.time.Clock()

player = Player(
    pygame.Vector2(SCREEN_WIDTH / 2 - TILE_SIZE / 2, SCREEN_HEIGHT - TILE_SIZE)
)  # location is defined in a not-so-neat manner, subject to change. Player starts out in the bottom-middle of the screen.
highscore = HighScore()
score = Score(player, highscore)


game_over = GameOver(player, highscore)

level = Level(player, game_over, highscore)


def main():
    dt = 0.0  # delta time

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

                # if event.type == pygame.KEYDOWN:
                #    if event.key == pygame.K_SPACE and game_over.game_over:
                #        level.restart()
                #        score.reset()

        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_SPACE] and level.game_over:
            level.restart()
            score.reset()

        level.update(dt)
        player.update()
        score.update(dt)
        game_over.update(dt)

        level.draw(screen)
        player.draw(screen)
        score.draw(screen)
        game_over.draw(screen)

        pygame.display.update()
        dt = clock.tick(FPS) / 1000  # delta time


if __name__ == "__main__":
    main()
