import pygame
import sys
import os
from .paddle import Paddle
from .ai_paddle import AIPaddle
from .ball import Ball 
from .scoreboard import Scoreboard
from .sound import Sound
from .constants import Constants
from game import Game

# Class definition of the Pong game itself
class Pong(Game):
    def __init__(self, screen):
        super().__init__(screen, multiplayer=True)
        self.next_state = "MENU"
        # Initialize Pygame engine and audio mixer
        pygame.init() 
        pygame.mixer.init() 

        # Game window attributes 
        self.screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("PONG")
        
        # Timing and State attributes
        self.clock = pygame.time.Clock()
        self.game_active = False
        self.singleplayer = False
        self.selecting_difficulty = False

        # Creating current working directory variable
        cwd = os.path.dirname(os.path.abspath(__file__))
        # Loading in music assets
        self.opp_score_sound = pygame.mixer.Sound(os.path.join(cwd, "assets", "sounds", "scoring_sound.mp3"))
        self.opp_score_sound.set_volume(0.3)
        self.winning_sound = pygame.mixer.Sound(os.path.join(cwd, "assets", "sounds", "winning_sound.mp3"))
        self.winning_sound.set_volume(0.15) 

        # Initializing game Objects
        self.scoreboard = Scoreboard(Constants.SCREEN_WIDTH)
        self.game_theme = Sound() 
        self.player_paddle = Paddle(50, 440, 12, 80, Constants.PLAYER_SPEED, "#0099ff", self.pressed, False)
        self.ball_1 = Ball(640, 480, 15, 8)

        # Variables for the winner display duration
        self.winner_text = ""
        self.winner_time = 0
        self.winner_delay = 3000 

    # method for setting the game up for singleplayer
    def setup_ai(self, level):
        Sound.theme1_fadeout(self.game_theme)
        Sound.theme2(self.game_theme)
        # Creating AI
        self.ai_paddle = AIPaddle(1220, 440, 12, 80, "#ff6600", difficulty=level)
        # setting all correct attribites for game start
        self.scoreboard.opponent_score = 0
        self.scoreboard.player_score = 0
        self.game_active = True 
        self.singleplayer = True
        self.ball_1.start_timer()

    # method for setting the game up for multiplayer
    def setup_multiplayer(self):
        Sound.theme1_fadeout(self.game_theme)
        Sound.theme2(self.game_theme)
        # Creating 2nd player paddle
        self.opponent_paddle = Paddle(1220, 440, 12, 80, Constants.PLAYER_SPEED, "#ff6600", self.pressed, True)
        # setting all correct attribites for game start
        self.scoreboard.opponent_score = 0
        self.scoreboard.player_score = 0
        self.game_active = True
        self.singleplayer = False 
        self.ball_1.start_timer()
    
    # The game loop method
    def update(self, dt):
        

            # Handle Menu Navigation (Press A or B to select options)
            if not self.game_active and self.winner_text == "":
                if not self.selecting_difficulty:
                    if self.just_pressed["a"]:
                        self.setup_multiplayer() 
                    if self.just_pressed["b"]:
                        self.selecting_difficulty = True
                else:
                    if self.just_pressed["a"]:
                        self.setup_ai("easy")
                        self.selecting_difficulty = False
                    if self.just_pressed["b"]:
                        self.setup_ai("hard")
                        self.selecting_difficulty = False

            # Gameplay
            if self.game_active: 
                self.screen.fill("#191919") # clearing screen
                # Drawing thw middle line
                for y in range(0, Constants.SCREEN_HEIGHT, 40):
                    pygame.draw.rect(self.screen, "#FFFDF7", (Constants.SCREEN_WIDTH // 2 - 2, y, 4, 20))

                # Drawing player paddle
                self.player_paddle.draw(self.screen) 

                # Drawing AI paddle (singleplayer) or 2nd player paddle (multiplayer)              
                if self.singleplayer:
                    self.ai_paddle.draw(self.screen)
                    self.ai_paddle.move(self.ball_1)
                    self.ball_1.check_collision(self.ai_paddle)
                else:
                    self.opponent_paddle.draw(self.screen)
                    self.opponent_paddle.move(Constants.SCREEN_HEIGHT)
                    self.ball_1.check_collision(self.opponent_paddle)

                # Drawing ball and scoreboard
                self.ball_1.draw(self.screen)
                self.scoreboard.draw(self.screen)

                # Updating draws
                self.player_paddle.move(Constants.SCREEN_HEIGHT)
                self.ball_1.move(self.screen_rect)
                self.ball_1.check_collision(self.player_paddle)

                # Scoring checking
                if self.ball_1.left <= 0: # Score against Player 1
                    self.opp_score_sound.play()
                    self.scoreboard.update_score(is_player=False)
                    self.ball_1.reset()
                    self.ball_1.start_timer()
                if self.ball_1.right >= Constants.SCREEN_WIDTH: # Score for Player 1
                    self.opp_score_sound.play()
                    self.scoreboard.update_score(is_player=True)
                    self.ball_1.reset()      
                    self.ball_1.start_timer()    

                # Win checking
                if self.scoreboard.player_score >= 10 or self.scoreboard.opponent_score >= 10:
                    self.winner_text = "BLUE WINS!" if self.scoreboard.player_score >= 10 else "ORANGE WINS!"
                    Sound.theme2_stop(self.game_theme)
                    self.winning_sound.play()
                    self.game_active = False
                    self.winner_time = pygame.time.get_ticks() 
            
            # Winner screen and Startscreen
            else:
                current_time = pygame.time.get_ticks() 

                if self.winner_text != "": # Show the "Winner" message for 3 seconds
                    self.screen.fill("#191919")
                    color = "#0099ff" if "BLUE" in self.winner_text else "#ff6600"
                    win_surf = self.scoreboard.font.render(self.winner_text, True, color)
                    win_rect = win_surf.get_rect(center=(Constants.SCREEN_WIDTH // 2, Constants.SCREEN_HEIGHT // 2))
                    self.screen.blit(win_surf, win_rect)

                    if current_time - self.winner_time > self.winner_delay:
                        self.winner_text = "" # Back to main menu

                else:  # Draw Start Menu or Difficulty Menu
                    Sound.theme1(self.game_theme)
                    self.screen.fill("#191919")
                    
                    if not self.selecting_difficulty:
                        title_txt = "PONG"
                        txt_a = "PRESS 'A' FOR MULTIPLAYER"
                        txt_b = "PRESS 'B' FOR SINGLEPLAYER"
                    else:
                        title_txt= "SELECT DIFFICULTY"
                        txt_a = "PRESS 'A' FOR EASY MODE" 
                        txt_b = "PRESS 'B' FOR HARD MODE" 
                    
                    title_surf = self.scoreboard.font.render(title_txt, True, "#0099ff")
                    title_rect = title_surf.get_rect(center=(Constants.SCREEN_WIDTH // 2, Constants.SCREEN_HEIGHT // 2 - 200))

                    a_surf = self.scoreboard.font_small.render(txt_a, True, "#ff6600")
                    a_rect = a_surf.get_rect(center=(Constants.SCREEN_WIDTH // 2, Constants.SCREEN_HEIGHT // 2))

                    b_surf = self.scoreboard.font_small.render(txt_b, True, "#ff6600")
                    b_rect = b_surf.get_rect(center=(Constants.SCREEN_WIDTH // 2, Constants.SCREEN_HEIGHT // 2 + 80))

                    # Blitting texts on screen
                    self.screen.blit(title_surf, title_rect)
                    self.screen.blit(a_surf, a_rect)
                    self.screen.blit(b_surf, b_rect)