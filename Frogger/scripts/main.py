import pygame
import sys
from player import Player
from level import Level
from score import Score
from gameover import GameOver
from highscore import HighScore
from next_level import NextLevel
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
from lives_counter import LivesCounter


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
lives_counter = LivesCounter(player)

nextlevel = NextLevel()


game_over = GameOver(player, highscore)

level = Level(player, game_over, highscore, nextlevel)


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
        if keys[pygame.K_ESCAPE] and level.game_over:
            # self.next_state = "MENU"
            pass

        level.update(dt)
        player.update(dt)
        score.update(dt)
        game_over.update(dt)
        nextlevel.update(dt)

        level.draw(screen)
        player.draw(screen)
        score.draw(screen)
        lives_counter.draw(screen)
        game_over.draw(screen)
        nextlevel.draw(screen)

        pygame.display.update()
        dt = clock.tick(FPS) / 1000  # delta time


if __name__ == "__main__":
    main()
