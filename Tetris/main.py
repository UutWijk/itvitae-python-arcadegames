import pygame
pygame.mixer.init()
from pygame import Color
import ctypes
import os
import game_state



# Initialize pygame and sound mixer
pygame.init()


playfield : BlockField = None

import movement
ctypes.windll.user32.SetProcessDPIAware()

import draw_score
from block_field import BlockField



# Constants
FPS = 60

# Screen information

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960

# Display setup
DISPLAY_SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background = pygame.image.load(os.path.join('assets', 'textures', 'background.png'))
background = pygame.transform.scale(background, (1280, 960))
#background = pygame.transform.scale_by(background, 4)

# text setup
font = pygame.font.Font('assets/nintendo-nes-font.ttf', 20)
HSfont = pygame.font.Font('assets/nintendo-nes-font.ttf', 13)
linesfont = pygame.font.Font('assets/nintendo-nes-font.ttf', 17)

# timer_setup
clock = pygame.time.Clock()
delta = 0

#starts the timer for the movement.py. We can change the speed in the movement.py file

game_state.make_timer()

playfield = BlockField()
playfield.calculate_game_speed()

def main():
    pygame.mixer.music.load("assets/sounds/1 - Music 1.mp3")
    pygame.mixer.music.play()
    global delta
    game_continues = True
    if not os.path.exists("HighScore.txt"):
        with open("HighScore.txt", 'w') as file:
            file.write("0\n0\n0\n0\n0\n0\n0\n0\n0\n0") 

    

    while True:
        # clear screen
        DISPLAY_SURFACE.fill('grey')
        DISPLAY_SURFACE.blit(background)
        game_continues = movement.movement(playfield, game_continues)
        scores = playfield.leaderboard
        highScores = ""
        for score in scores:
            highScores += (str(score) + "\n")

        game_surface = pygame.Surface((330, 660))
        playfield.draw(game_surface)
        game_surface = pygame.transform.scale(game_surface, (405, 694))
        DISPLAY_SURFACE.blit(game_surface, (475, 167))


        score_text = font.render(f"SCORE\n\n{str(playfield.score)}", True, 'white')
        HStext = HSfont.render("HIGH SCORES\n\n" + highScores, True, 'white')
        
        if game_continues:
            lines_text = linesfont.render(str(playfield.lines), True, 'white')
            level_text = linesfont.render(str(playfield.level), True, 'white')
            # print(str(playfield.score))
        else:
            game_over_text = HSfont.render("GAME OVER!\nRETRY: Z OR X", True, 'white', bgcolor='black')
            DISPLAY_SURFACE.blit(game_over_text, (500, 350))
            game_state.timer.set_start_speed()

        DISPLAY_SURFACE.blit(score_text, (980, 91))
        DISPLAY_SURFACE.blit(lines_text, (760, 69))
        DISPLAY_SURFACE.blit(level_text, (1040, 686))
        DISPLAY_SURFACE.blit(HStext, (95, 284))

        draw_score.draw_array(playfield.tetromino_generator.next_piece.shape, DISPLAY_SURFACE, (955,407))

        # Display and tick
        pygame.display.update()
        delta = clock.tick(FPS) / 1000.0 
        game_state.timer.speed




if __name__ == "__main__":
    main()