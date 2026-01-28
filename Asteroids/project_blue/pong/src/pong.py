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

# Class definitions of Pong the game
class Pong(Game):
    def __init__(self, screen):
        super().__init__(screen)
        # Pygame and Soundmixer initialization 
        pygame.mixer.init()

        # Display screen and name
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        
        # Clock initialization and game state variable setting
        self.clock = pygame.time.Clock()
        self.game_active = False
        self.singleplayer = False

        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Loading in the scoring sound
        self.opp_score_sound = pygame.mixer.Sound(os.path.join(current_dir, "assets", "sounds", "scoring_sound.mp3"))
        self.opp_score_sound.set_volume(0.2)

        self.winning_sound = pygame.mixer.Sound(os.path.join(current_dir, "assets", "sounds", "winning_sound.mp3"))
        self.winning_sound.set_volume(0.1) 

        # Creating scoreboard
        self.scoreboard = Scoreboard(Constants.SCREEN_WIDTH)

        # Variables for the 'win' State and delay timer
        self.winner_text = ""
        self.winner_time = 0
        self.winner_delay = 3000 # In milliseconds (3 seconds)

        # Creating sound Object
        self.game_theme = Sound() 

        # Creating paddles
        self.player_paddle = Paddle(50, 440, 15, 70, Constants.PLAYER_SPEED, "#0099ff", pygame.K_w, pygame.K_s)

        # Creating ball 
        self.ball_1 = Ball(640, 480, 15, 8)

    
    # Game loop in run method

    def update(self, dt):

        # Variable for all possible keys to press in pygame 
        keys = pygame.key.get_pressed()
        # Event Handling
            
        # Only triggers when in Startscreen and the winner text is not displayed: 
        if not self.game_active and self.winner_text == "":
            if keys[pygame.K_a]:
                Sound.theme1_fadeout(self.game_theme)
                Sound.theme2(self.game_theme)
                self.opponent_paddle = Paddle(1220, 440, 15, 70, Constants.PLAYER_SPEED, "#ff6600", pygame.K_UP, pygame.K_DOWN)
                self.scoreboard.opponent_score = 0
                self.scoreboard.player_score = 0
                self.game_active = True
                self.ball_1.start_timer()
            if keys[pygame.K_b]:
                Sound.theme1_fadeout(self.game_theme)
                Sound.theme2(self.game_theme)
                self.ai_paddle = AIPaddle(1220, 440, 15, 70, Constants.AI_SPEED, "#ff6600")
                self.scoreboard.opponent_score = 0
                self.scoreboard.player_score = 0
                self.game_active = True 
                self.singleplayer = True
                self.ball_1.start_timer()

        # The game play itself 
        if self.game_active: 
            # Drawing screen
            self.screen.fill("#191919")
            # Drawing middle line
            for y in range(0, Constants.SCREEN_HEIGHT, 40): # Draw a dash every 40 pixels
                pygame.draw.rect(self.screen, "#FFFDF7", (Constants.SCREEN_WIDTH // 2 - 2, y, 4, 20))

            # Drawing paddles
            self.player_paddle.draw(self.screen)              
            if self.singleplayer:
                self.ai_paddle.draw(self.screen)
            else:
                self.opponent_paddle.draw(self.screen)
            # Drawing ball    
            self.ball_1.draw(self.screen)
            # Drawing scoreboard
            self.scoreboard.draw(self.screen)

            # Movement of paddles and ball
            self.player_paddle.move(Constants.SCREEN_HEIGHT)
            if self.singleplayer:
                self.ai_paddle.move(self.ball_1)
            else:
                self.opponent_paddle.move(Constants.SCREEN_HEIGHT)
            self.ball_1.move(self.screen_rect)
            
            # Collision implementation (from ball.py)
            self.ball_1.check_collision(self.player_paddle)
            if self.singleplayer:
                self.ball_1.check_collision(self.ai_paddle)
            else:
                self.ball_1.check_collision(self.opponent_paddle)

            # Scoring checking (execution in ball.py))
            if self.ball_1.left <= 0:
                self.opp_score_sound.play()
                self.scoreboard.update_score(is_player=False) # Opponent scores
                # Resetting ball after scoring, with pauze
                self.ball_1.reset()
                self.ball_1.start_timer()
            if self.ball_1.right >= Constants.SCREEN_WIDTH:
                self.opp_score_sound.play()
                self.scoreboard.update_score(is_player=True) # Player scores
                # resetting ball after scoring, with pauze
                self.ball_1.reset()      
                self.ball_1.start_timer()    

            # Winning condition met -> display winner message and go back to start screen
            if self.scoreboard.player_score >= 10: 
                self.winner_text = "BLUE WINS!"
                Sound.theme2_stop(self.game_theme)
                self.winning_sound.play()
                self.game_active = False
                self.winner_time = pygame.time.get_ticks() 
            elif self.scoreboard.opponent_score >= 10:
                self.winner_text = "ORANGE WINS!"
                Sound.theme2_stop(self.game_theme)
                self.winning_sound.play()
                self.game_active = False
                self.winner_time = pygame.time.get_ticks() 
        
        
        else:
            current_time = pygame.time.get_ticks() # Setting timer variable for winner message 

            # Winner message logic
            if self.winner_text != "":
                self.screen.fill("#191919")
                if self.scoreboard.player_score >= 10:
                    win_surf = self.scoreboard.font.render(self.winner_text, True, "#0099ff")
                    win_rect = win_surf.get_rect(center=(Constants.SCREEN_WIDTH // 2, Constants.SCREEN_HEIGHT // 2 - 250))
                    self.ball_1.draw(self.screen)
                    self.ball_1.move(self.screen_rect)
                    self.screen.blit(win_surf, win_rect)
                if self.scoreboard.opponent_score >= 10:
                    win_surf = self.scoreboard.font.render(self.winner_text, True, "#ff6600")
                    win_rect = win_surf.get_rect(center=(Constants.SCREEN_WIDTH // 2, Constants.SCREEN_HEIGHT // 2 - 250))
                    self.ball_1.draw(self.screen)
                    self.ball_1.move(self.screen_rect)
                    self.screen.blit(win_surf, win_rect)                      

                if current_time - self.winner_time > self.winner_delay:
                    self.winner_text = ""

            # Start screen logic
            else:  
                # Drawing and creating surfaces and rects for startscreen
                Sound.theme1(self.game_theme)
                self.screen.fill("#191919")
                start_text = "PRESS 'A' TO START MULTIPLAYER"
                singleplayer_text = "PRESS 'B' TO START SINGLEPLAYER"
                title_text = "PONG"

                title_surf = self.scoreboard.font.render(title_text, True, "#0099ff")
                title_rect = title_surf.get_rect(center=(Constants.SCREEN_WIDTH // 2, Constants.SCREEN_HEIGHT // 2 - 300))

                start_surf = self.scoreboard.font_small.render(start_text, True, "#ff6600")
                start_rect = start_surf.get_rect(center=(Constants.SCREEN_WIDTH // 2, Constants.SCREEN_HEIGHT // 2 - 150))

                singleplayer_surf = self.scoreboard.font_small.render(singleplayer_text, True, "#ff6600")
                singleplayer_rect= singleplayer_surf.get_rect(center=(Constants.SCREEN_WIDTH // 2, Constants.SCREEN_HEIGHT // 2 - 50))
                

                # Blitting the Title text and Press SPACE text
                self.screen.blit(title_surf, title_rect)
                self.screen.blit(start_surf, start_rect)
                self.screen.blit(singleplayer_surf, singleplayer_rect)

        
            self.clock.tick(Constants.FPS)

        def draw(self):
            ... # Drawing is handled in the update method
