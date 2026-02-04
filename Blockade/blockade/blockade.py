import pygame
import os
import sys
from .player import Player
from .sound import Sound
from game import Game

# Pygame init stuff
pygame.init()

FPS = 60
clock = pygame.time.Clock()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960

#setup for the grid
CELL_SIZE = 32
COLUMNS = 21
ROWS = 21

GRID_WIDTH = COLUMNS * CELL_SIZE
GRID_HEIGHT = ROWS * CELL_SIZE

OFFSET_X = (SCREEN_WIDTH - GRID_WIDTH) // 2
OFFSET_Y = (SCREEN_HEIGHT - GRID_HEIGHT) // 2

class Blockade(Game):
    def __init__(self, screen) -> None:
        super().__init__(screen, True)
        current_dir = os.path.dirname(__file__)
        # Font for the game
        self.FONT = pygame.font.Font(os.path.join(current_dir, "assets/RetroGaming.ttf"), 40)
        self.FONT_two = pygame.font.Font(os.path.join(current_dir, "assets/RetroGaming.ttf"), 60)
        self.FONT_tiny = pygame.font.Font(os.path.join(current_dir, "assets/RetroGaming.ttf"), 20)
        # Some game states for pausing after a win etc.
        self.game_active = True
        self.waiting_to_start = True

        # The string that will get edited for whoever wins a match
        self.winner_message = ""
        # Screen setup and application window text
        self.DISPLAY_SCREEN = screen


        # Player controls setup
        p1_controls = {"up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d}
        p2_controls = {"up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT}

        # Player setup
        self.player_1 = Player(3,3,"#0099ff", False, (1,0))
        self.player_2 = Player(17,17,"#ff6600", True,(-1,0))

        #sound setup
        self.game_sounds = Sound()
        # This is for the player movement so they dont constantly move. the 400 is time in MS, the higher the number the longer the delay.
        self.MOVE_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.MOVE_EVENT, 400)

        self.timer = 0

        # Scores setup
        self.p1_score = 0
        self.p2_score = 0
        self.winning_score = 3

        self.game_timer = 0 
        self.reset_timer = 2 # Time in seconds before the game resets after a win

        # By calling these here, the players start moving at the same time on the first round
        self.player_1.reset()
        self.player_2.reset()

    # Draws a grid with a for loop, adjust the numbers in draw.rect for a diffrent colour
    def draw_grid(self):
        
        for x in range(COLUMNS):
            for y in range(ROWS):
                rect = pygame.Rect(
                    OFFSET_X + x * CELL_SIZE,
                    OFFSET_Y + y * CELL_SIZE,
                    CELL_SIZE,
                    CELL_SIZE
                )
                pygame.draw.rect(self.DISPLAY_SCREEN, "#3C3C3C", rect, 1)

    # Draws a border with a for loop, adjust the numbers in the draw.rect for a diffrent colour
    def draw_border(self):
        for x in range(COLUMNS):
            for y in range(ROWS):
                if x == 0 or x == COLUMNS - 1 or y == 0 or y == ROWS - 1:
                    rect = pygame.Rect(
                        OFFSET_X + x * CELL_SIZE,
                        OFFSET_Y + y * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE
                    )
                    pygame.draw.rect(self.DISPLAY_SCREEN, "#cfcfcf", rect)


# Main game loop
    def update(self, dt):
        pressed = self.pressed
        self.timer += dt
        self.DISPLAY_SCREEN.fill("#19191919")
         
        match_over = self.p1_score >= self.winning_score or self.p2_score >= self.winning_score
        if match_over and pressed["a"]:
            self.p1_score = 0
            self.p2_score = 0
            self.player_1.reset()
            self.player_2.reset()
            self.game_active = True
            self.waiting_to_start = True
            self.winner_message = ""

        # When any player presses a key, the round will start (and both players will start moving in their default direction)
        if self.waiting_to_start == True and any(pressed.values()):
            self.waiting_to_start = False

        if self.just_pressed["b"]:
            self.next_state = "MENU"

        # Handles player input
        if self.game_active and not self.waiting_to_start:
            self.player_1.player_input(pressed)
            self.player_2.player_input(pressed)

        # Handles player movement, they move at an interval thats specified earlier in the code (the pygame.time.set_timer)
            if self.timer > 0.400:
                self.player_1.move()
                self.player_2.move()
                self.timer = 0

                # Checks player collision
                p1_hit = self.player_1.check_collision(COLUMNS, ROWS, self.player_2.trail)
                p2_hit = self.player_2.check_collision(COLUMNS, ROWS, self.player_1.trail)
                # Win/lose conditions
                if p1_hit or p2_hit:
                    if p1_hit and p2_hit:
                        self.winner_message = "TIE"
                        Sound.collide(self.game_sounds)

                    elif p1_hit:
                        self.p2_score += 1
                        self.winner_message = "Player 2 won the round!"
                        if not self.p2_score >= self.winning_score:
                            Sound.winround(self.game_sounds)

                    elif p2_hit:
                        self.p1_score += 1
                        self.winner_message = "Player 1 won the round!"
                        if not self.p1_score >= self.winning_score:
                            Sound.winround(self.game_sounds)

                    if self.p1_score >= self.winning_score:
                        self.winner_message = "        Game Over!\n       Player 1 WIN\n   Press 'A' To Reset."
                        Sound.wingame(self.game_sounds)
                    if self.p2_score >= self.winning_score:
                        self.winner_message = "        Game Over!\n       Player 2 WIN\n   Press 'A' To Reset."      
                        Sound.wingame(self.game_sounds)          

                    # Turns the game inactive and puts up a timer so it doesnt instantly reset               
                    self.game_active = False
                    

        # When a player hasnt won yet, resets the board so they players can play again
        if not self.game_active:
            if self.game_timer > self.reset_timer:
                self.game_timer = 0
                if self.p1_score < self.winning_score and self.p2_score < self.winning_score:
                    self.player_1.reset()
                    self.player_2.reset()
                    self.game_active = True
                    self.winner_message = ""
                    self.waiting_to_start = True
            else:
                self.game_timer += dt


        # Draws the grid and the border of the play field
        self.draw_grid()
        self.draw_border()

        # Draws the players
        self.player_1.draw(self.DISPLAY_SCREEN, OFFSET_X, OFFSET_Y, CELL_SIZE)
        self.player_2.draw(self.DISPLAY_SCREEN, OFFSET_X, OFFSET_Y, CELL_SIZE)

        # Winner message:
        if not self.game_active:
            text_surface = self.FONT.render(self.winner_message, True, "#FFFDF7")
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.DISPLAY_SCREEN.blit(text_surface, text_rect)
        # Start message:
        if self.waiting_to_start and self.game_active:
            start_surface = self.FONT.render("PRESS ANY BUTTON\n        TO START", True, "#FFFDF7")
            start_rect = start_surface.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.DISPLAY_SCREEN.blit(start_surface,start_rect)

        # Score display:
        score_surface_p1 = self.FONT.render(f"P1: {self.p1_score}", True, "#FFFDF7")
        score_surface_p2 = self.FONT.render(f"P2: {self.p2_score}", True, "#FFFDF7")
        self.DISPLAY_SCREEN.blit(score_surface_p1, (SCREEN_WIDTH // 2 - 500, 225))
        self.DISPLAY_SCREEN.blit(score_surface_p2, (SCREEN_WIDTH //2 + 380, 225))

        game_title_message = self.FONT_two.render("B L O C K A D E", True, "#FFFDF7")
        return_to_menu_message = self.FONT_tiny.render("Press 'B' to return to menu", True, "#FFFDF7")
        self.DISPLAY_SCREEN.blit(game_title_message,(SCREEN_WIDTH // 2 -275, 65))
        self.DISPLAY_SCREEN.blit(return_to_menu_message, (SCREEN_WIDTH // 2 - 235, SCREEN_HEIGHT - 40))
