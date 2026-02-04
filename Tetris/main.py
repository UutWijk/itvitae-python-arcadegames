import pygame
# Initialize pygame and sound mixer
pygame.init()
pygame.mixer.init()
import draw_score
from block_field import BlockField
import movement
import ctypes
import os
import game_state
import background

ctypes.windll.user32.SetProcessDPIAware()

# Constants
FPS = 60

# Display setup
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
DISPLAY_SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# text setup
font = pygame.font.Font("assets/nintendo-nes-font.ttf", 32)
HSfont = pygame.font.Font("assets/nintendo-nes-font.ttf", 15)
font40 = pygame.font.Font("assets/nintendo-nes-font.ttf", 40)
font25 = pygame.font.Font("assets/nintendo-nes-font.ttf", 25)
font20 = pygame.font.Font("assets/nintendo-nes-font.ttf", 20)
font15 = pygame.font.Font("assets/nintendo-nes-font.ttf", 15)
font12 = pygame.font.Font("assets/nintendo-nes-font.ttf", 12)
font9 = pygame.font.Font("assets/nintendo-nes-font.ttf", 9)


# timer for the game and the piece movement
clock = pygame.time.Clock()
delta = 0
game_state.make_timer()

#make a new high score file if it doesnt exist yet
if not os.path.exists("HighScore.txt"):
    with open("HighScore.txt", 'w') as file:
        file.write("0\n0\n0\n0\n0\n0\n0\n0\n0\n0") 


def main() -> None:
    global delta
    pygame.mixer.music.load("assets/sounds/1 - Music 1.mp3")
    pygame.mixer.music.play(-1)
    game_state.game_continues = True
    playfield = BlockField()


    while True:
        # clear screen
        DISPLAY_SURFACE.fill('grey')
        movement.movement(playfield)
        scores = playfield.leaderboard
        highScores = ""
        for score in scores:
            highScores += str(score) + "\n"

        if game_state.game_continues:
            background.draw_game_active(DISPLAY_SURFACE)

            playfield.draw(DISPLAY_SURFACE, 472, 104)

            score_text_introduction = font25.render("SCORE", True, "white")
            DISPLAY_SURFACE.blit(score_text_introduction, (936, 196))

            score_text = font25.render(str(playfield.score), True, "white")
            text_rect = score_text.get_rect(center=(1059, 285))
            DISPLAY_SURFACE.blit(score_text, (text_rect))

            HStext = font12.render(" HIGH\nSCORES:\n\n" + highScores, True, "white")
            DISPLAY_SURFACE.blit(HStext, (206, 186))

            # draw next piece
            draw_score.draw_array(
                playfield.tetromino_generator.next_piece.shape,
                DISPLAY_SURFACE,
                (916, 420),
            )

        else:
            game_state.timer.set_start_speed()
            background.draw_game_over(DISPLAY_SURFACE)

            game_over = font25.render(" GAME OVER!\nRETRY: Z OR X", True, "white")
            text_rect = game_over.get_rect(center=(SCREEN_WIDTH / 2, 100))
            DISPLAY_SURFACE.blit(game_over, (320, 100))

            reached_score_introduction = font12.render("REACHED SCORE:", True, "white")
            text_rect = reached_score_introduction.get_rect(
                center=(SCREEN_WIDTH / 2, 335)
            )
            DISPLAY_SURFACE.blit(reached_score_introduction, (text_rect))

            reached_score = font20.render(str(playfield.score), True, "white")
            text_rect = reached_score.get_rect(center=(SCREEN_WIDTH / 2, 380))
            DISPLAY_SURFACE.blit(reached_score, (text_rect))

            scores = playfield.leaderboard
            highScores = ""
            for score in scores[:5]:
                highScores += str(score) + "\n   "

            HStext = font15.render("HIGH SCORES:\n\n   " + highScores, True, "white")
            text_rect = HStext.get_rect(center=(SCREEN_WIDTH / 2, 710))
            DISPLAY_SURFACE.blit(HStext, (text_rect))

            game_state.timer.set_start_speed()

        # Display and tick
        pygame.display.update()
        delta = clock.tick(FPS) / 1000.0


if __name__ == "__main__":
    main()
