import os
import pygame

tetris_dir = os.path.dirname(os.path.abspath(__file__))

active_score = pygame.image.load(os.path.join(tetris_dir, 'assets','Background','active_score.png'))
background_empty = pygame.image.load(os.path.join(tetris_dir, 'assets','Background','background_empty.png'))
blockfield = pygame.image.load(os.path.join(tetris_dir, 'assets','Background','blockfield.png'))
game_over_score = pygame.image.load(os.path.join(tetris_dir, 'assets','Background','game_over_score.png'))
game_over = pygame.image.load(os.path.join(tetris_dir, 'assets','Background','game_over.png'))
next_piece = pygame.image.load(os.path.join(tetris_dir, 'assets','Background','next_piece.png'))
score_list = pygame.image.load(os.path.join(tetris_dir, 'assets','Background','score_list.png'))
reached_score = pygame.image.load(os.path.join(tetris_dir, 'assets','Background','reached_score.png'))
 

def draw_game_active(DISPLAY_SURFACE):
    DISPLAY_SURFACE.blit(background_empty, (0, 0))
    DISPLAY_SURFACE.blit(next_piece, (890, 394))
    DISPLAY_SURFACE.blit(score_list, (170, 140))
    DISPLAY_SURFACE.blit(active_score, (890, 140))
    DISPLAY_SURFACE.blit(blockfield, (446, 78))
    

def draw_game_over(DISPLAY_SURFACE):
    DISPLAY_SURFACE.blit(background_empty, (0,0))
    DISPLAY_SURFACE.blit(game_over, (248,40))
    DISPLAY_SURFACE.blit(game_over_score, (393,466))
    DISPLAY_SURFACE.blit(reached_score, (391, 279))