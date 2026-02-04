import pygame
from .block_field import BlockField
from . import draw_score
from . import movement
from . import game_state
from . import background
import os

from game import Game

MOVE_PIECE_EVENT = pygame.USEREVENT + 1

class Tetris(Game):
    def __init__(self, screen) -> None:
        super().__init__(screen)
        self.tetris_dir = os.path.dirname(os.path.abspath(__file__))
        # text setup
        font_path = os.path.join(self.tetris_dir, "assets", "nintendo-nes-font.ttf")
        self.font = pygame.font.Font(font_path, 32)
        self.HSfont = pygame.font.Font(font_path, 15)
        self.font40 = pygame.font.Font(font_path, 40)
        self.font25 = pygame.font.Font(font_path, 25)
        self.font20 = pygame.font.Font(font_path, 20)
        self.font15 = pygame.font.Font(font_path, 15)
        self.font12 = pygame.font.Font(font_path, 12)
        self.font9 = pygame.font.Font(font_path, 9)
        # initialise the timer for the piece movement
        game_state.make_timer()
        #make a new high score file if it doesnt exist yet
        if not os.path.exists("HighScore.txt"):
            with open("HighScore.txt", 'w') as file:
                file.write("0\n0\n0\n0\n0\n0\n0\n0\n0\n0")
        game_state.game_continues = True
        self.playfield = BlockField()
        self.playing_music = False
        self.key_map_flipped = {v: k for k, v in self.key_map.items()}

    def handle_events(self, event):
        if event.type == MOVE_PIECE_EVENT and game_state.game_continues:
            self.playfield.move_piece("down")
        super().handle_events(event)

    def update(self, dt):
        if self.playing_music == False:
            pygame.mixer.music.load(os.path.join(self.tetris_dir, "assets", "sounds", "1 - Music 1.mp3"))
            pygame.mixer.music.play(-1)
            self.playing_music = True

        movement.movement(self.playfield, self.key_map_flipped, self.pressed, self.just_pressed)
        self.scores = self.playfield.leaderboard
        self.highScores = ""
        for score in self.scores:
            self.highScores += str(score) + "\n"
        if game_state.game_continues:
            pass
        else:
            game_state.timer.set_start_speed()
            if self.just_pressed["a"]:   
                game_state.game_continues = True
                self.playfield.grid = self.playfield.defaultgrid.copy()   
                self.playfield.score = 0  
            elif self.just_pressed["b"]:
                self.next_state = "MENU"
                game_state.game_continues = True
                self.playfield.grid = self.playfield.defaultgrid.copy()   
                self.playfield.score = 0 
                pygame.mixer.music.stop()
                self.playing_music = False
        
    def draw(self):
        if game_state.game_continues:
            background.draw_game_active(self.screen)

            self.playfield.draw(self.screen, 472, 104)

            score_text_introduction = self.font25.render("SCORE", True, "white")
            self.screen.blit(score_text_introduction, (936, 196))

            score_text = self.font25.render(str(self.playfield.score), True, "white")
            text_rect = score_text.get_rect(center=(1059, 285))
            self.screen.blit(score_text, (text_rect))

            HStext = self.font12.render(" HIGH\nSCORES:\n\n" + self.highScores, True, "white")
            self.screen.blit(HStext, (206, 186))

            # draw next piece
            draw_score.draw_array(
                self.playfield.tetromino_generator.next_piece.shape,
                self.screen,
                (916, 420),
            )
        else: # when gamestate.game_continues is false
            background.draw_game_over(self.screen)

            game_over = self.font20.render(" GAME OVER!", True, "white")
            text_rect = game_over.get_rect(center=(self.screen.get_width() / 2, 120))
            self.screen.blit(game_over, (text_rect))

            game_over = self.font20.render("RETRY: A MENU: B", True, "white")
            text_rect = game_over.get_rect(center=(self.screen.get_width() / 2, 170))
            self.screen.blit(game_over, (text_rect))

            reached_score_introduction = self.font12.render("REACHED SCORE:", True, "white")
            text_rect = reached_score_introduction.get_rect(
                center=(self.screen.get_width() / 2, 335)
            )
            self.screen.blit(reached_score_introduction, (text_rect))

            reached_score = self.font20.render(str(self.playfield.score), True, "white")
            text_rect = reached_score.get_rect(center=(self.screen.get_width() / 2, 380))
            self.screen.blit(reached_score, (text_rect))

            scores = self.playfield.leaderboard
            highScores = ""
            for score in scores[:5]:
                highScores += str(score) + "\n   "
            
            HStext = self.font15.render("HIGH SCORES:\n\n   " + highScores, True, "white")
            text_rect = HStext.get_rect(center=(self.screen.get_width() / 2, 710))
            self.screen.blit(HStext, (text_rect))

