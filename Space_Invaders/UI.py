import pygame
import os
from Space_Invaders.constants import *
from Space_Invaders.assets import player_sprite

HIGHSCORE_FILE = os.path.join(os.path.dirname(__file__), "High-Score.txt") # path to local file that has the high-score

if not os.path.exists(HIGHSCORE_FILE): # checks if file "High-Score.txt" exists, if not it will make one
    with open(HIGHSCORE_FILE, "w", encoding="utf-8") as f:
        f.write(str(0)) 

# regular font style and sizes
font = pygame.font.SysFont("Verdana", int(30 * GAME_SCALE))
font_small = pygame.font.SysFont("Verdana", int(20 * GAME_SCALE))
font_big = pygame.font.SysFont("Verdana", int(45 * GAME_SCALE))

# custom font styles
retro_font_path = os.path.join(os.path.join(os.path.dirname(__file__), "assets", "fonts", "retro.ttf"))

#custom font sizes
retro_font_small = pygame.font.Font(retro_font_path, int(20 * GAME_SCALE))
retro_font = pygame.font.Font(retro_font_path, int(30 * GAME_SCALE))
retro_font_large = pygame.font.Font(retro_font_path, int(45 * GAME_SCALE))

def game_over_screen(surface: pygame.Surface, current_score): # Gets called in main game
    #surface.fill(WHITE)
    with open(HIGHSCORE_FILE, "r", encoding="utf-8") as f: # Reads high-score file and saves it in a variable
        current_highscore = int(f.readline().strip())

    if current_score > current_highscore: # Checks if there is a new high score and changes text depending on
        current_highscore = current_score
        update_highscore(current_score)
        high_score = retro_font_small.render(f"High-Score : {current_highscore} NEW!", True, WHITE)
    else:
        high_score = retro_font_small.render(f"High-Score : {current_highscore}", True, WHITE)
    
    title = retro_font_large.render("GAME OVER", True, WHITE) # creates the game over text to later be placed
    current_score = retro_font_small.render(f"Your Score : {current_score}", True, WHITE)
    prompt = retro_font_small.render("Press 'A' to Restart or 'B' to return to main menu", True, WHITE)
    background = pygame.Surface([700 * GAME_SCALE, 300 * GAME_SCALE], BLACK)

    surface.blit(background, background.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))       # adds black background to the game over screen
    surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)))           # places the game over text on the screen
    surface.blit(current_score, current_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)))
    surface.blit(high_score, high_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)))
    surface.blit(prompt, prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)))

    pygame.display.update() # one last update, otherwise the game over screen won't appear

def score_tracker(surface: pygame.Surface, current_score): # displays the current game's score and high-score
        score_text = retro_font.render(f"Score : {current_score}", True, WHITE)

        with open(HIGHSCORE_FILE, "r", encoding="utf-8") as f: # reads high-score file and saves it in a variable
            current_highscore = int(f.readline().strip())

        highscore_text = retro_font.render(f"High-Score : {current_highscore}", True, WHITE) # takes that high-score to display it

        surface.blit(score_text, score_text.get_rect(topleft=(10, 5)))
        surface.blit(highscore_text, highscore_text.get_rect(midtop=(SCREEN_WIDTH // 2, 5)))

def level_tracker(surface: pygame.Surface, current_level): # used to display the current level
    level_text = retro_font.render(f"Level : {current_level}", True, WHITE)

    surface.blit(level_text, level_text.get_rect(topright=(SCREEN_WIDTH - 10, 5)))

def display_lives(surface: pygame.Surface, current_lives): # used to display remaining lives
    lives_text = retro_font.render(f"Lives : {current_lives}", True, WHITE)

    surface.blit(lives_text, lives_text.get_rect(bottomleft=(10 * GAME_SCALE, SCREEN_HEIGHT - 5)))

    icon = pygame.image.load(player_sprite) # icons to display remaining lives
    icon = pygame.transform.scale(icon, (40 * GAME_SCALE, 40 * GAME_SCALE))

    if current_lives == 3: # shows amount of icons depending on how many lives remain
        surface.blit(icon, icon.get_rect(bottomleft=(175 * GAME_SCALE, SCREEN_HEIGHT - 7)))
        surface.blit(icon, icon.get_rect(bottomleft=(225 * GAME_SCALE, SCREEN_HEIGHT - 7)))
        surface.blit(icon, icon.get_rect(bottomleft=(275 * GAME_SCALE, SCREEN_HEIGHT - 7)))
    elif current_lives == 2:
        surface.blit(icon, icon.get_rect(bottomleft=(175 * GAME_SCALE, SCREEN_HEIGHT - 7)))
        surface.blit(icon, icon.get_rect(bottomleft=(225 * GAME_SCALE, SCREEN_HEIGHT - 7)))
    elif current_lives == 1:
        surface.blit(icon, icon.get_rect(bottomleft=(175 * GAME_SCALE, SCREEN_HEIGHT - 7)))
        return

def update_highscore(score): # update the high-score file with the new high-score
    with open(HIGHSCORE_FILE, "w", encoding="utf-8") as f:
        f.write(str(score))

#Main Menu UI
def main_menu_screen(surface: pygame.Surface):
    surface.fill(BLACK)

    title = retro_font_large.render("SPACE INVADERS", True, WHITE)
    subtitle = retro_font_small.render("move joystick LEFT or RIGHT to move, press 'A' to shoot!", True, WHITE)     # A = Space, joystick = arrow keys
    prompt = retro_font_small.render("Press 'A' to start the game", True, WHITE)                                    # idem
    exit_button = retro_font_small.render("press 'B' to quit", True, WHITE)                                         # B = Escape key

    surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)))
    surface.blit(subtitle, subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
    surface.blit(prompt, prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)))
    surface.blit(exit_button, exit_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)))

    pygame.display.update()
