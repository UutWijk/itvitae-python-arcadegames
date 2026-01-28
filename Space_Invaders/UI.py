import pygame
import os
from constants import *

HIGHSCORE_FILE = os.path.join(os.path.dirname(__file__), "High-Score.txt") # local file that has the high-score

font = pygame.font.SysFont("Verdana", 30)
font_small = pygame.font.SysFont("Verdana", 20)
font_big = pygame.font.SysFont("Verdana", 45)

def game_over_screen(surface: pygame.Surface, current_score): # Gets called in main game
    #surface.fill(WHITE)
    with open(HIGHSCORE_FILE, "r", encoding="utf-8") as f: # Reads high-score file and saves it in a variable
        current_highscore = int(f.readline().strip())

    if current_score > current_highscore: # Checks if there is a new high score and changes text depending on
        current_highscore = current_score
        update_highscore(current_score)
        high_score = font_small.render(f"High-Score: {current_highscore} NEW!", True, WHITE)
    else:
        high_score = font_small.render(f"High-Score: {current_highscore}", True, WHITE)
    
    title = font_big.render("GAME OVER", True, WHITE)
    current_score = font_small.render(f"Your Score: {current_score}", True, WHITE)
    prompt = font_small.render("Press ENTER to Restart or ESC to return to main menu", True, WHITE)

    surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))) # places the text on the screen
    surface.blit(current_score, current_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)))
    surface.blit(high_score, high_score.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10)))
    surface.blit(prompt, prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)))

    pygame.display.update() # one last update, otherwise the game over screen won't appear

def score_tracker(surface: pygame.Surface, current_score): # keeps track and displays the current game's score
        score_text = font.render(f"Score:{current_score}", True, WHITE)

        surface.blit(score_text, score_text.get_rect(topleft=(10, 5)))

def update_highscore(score): 
    with open(HIGHSCORE_FILE, "w", encoding="utf-8") as f:
        f.write(str(score))

def main_menu_screen(surface: pygame.Surface):

    title = font_big.render("SPACE INVADERS", True, WHITE)
    subtitle = font_small.render("use LEFT and RIGHT arrows to move, press SPACE to shoot!", True, WHITE)
    prompt = font_small.render("Press SPACE to start the game", True, WHITE)
    exit_button = font_small.render("press ESC to quit", True, WHITE)

    surface.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)))
    surface.blit(subtitle, subtitle.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
    surface.blit(prompt, prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)))
    surface.blit(exit_button, exit_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200)))

    pygame.display.update()
