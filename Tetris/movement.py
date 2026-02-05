import pygame
import os
import sys
from pygame.locals import QUIT
import numpy as np
from . import game_state

tetris_dir = os.path.dirname(os.path.abspath(__file__))

MOVE_PIECE_EVENT = pygame.USEREVENT + 1
move_sound = pygame.mixer.Sound(os.path.join(tetris_dir, "assets", "sounds", "move.mp3"))
rotate_sound = pygame.mixer.Sound(os.path.join(tetris_dir, "assets", "sounds", "rotate.mp3"))




def test_rotation(playfield, newshape) -> bool:
    """
    this function checks if a rotated version of a tetromino would not overlap with other blocks or go past the edges of the screen
    """
    position = playfield.piece_position
    for r in range(len(newshape)):
        for c in range(len(newshape[r])):
            if(newshape[r][c] and (playfield.grid[position[0] + r][position[1] + c] or position[0] + r > 19 or position[1] + c < 0 or position[1] + c > 9)):
                return False
    return True   



def movement(playfield, keys, keys_pressed, keys_just_pressed):
    """
    this function handles the movement of tetrominos
    """
    newshape = playfield.current_piece.check_for_rotate(keys_just_pressed)
    if(newshape):
        can_rotate = test_rotation(playfield, newshape)
        if(can_rotate):
            playfield.current_piece.shape = newshape
            rotate_sound.play()            

    if game_state.game_continues:
    #key press handling
        if keys_just_pressed["left"]:
            playfield.move_piece("left")
            move_sound.play()
            game_state.left_timer = 12

        if keys_pressed["left"]:  

            if game_state.left_timer == 0:
                playfield.move_piece("left")
                game_state.left_timer = 5
            else:
                game_state.left_timer -= 1

        if keys_just_pressed["right"]:
            playfield.move_piece("right")
            move_sound.play()
            game_state.right_timer = 12

        if keys_pressed["right"]:


            if game_state.right_timer == 0:
                playfield.move_piece("right")
                game_state.right_timer = 5
            else:
                game_state.right_timer -= 1    

        original_time_speed = game_state.timer.speed
        if keys_just_pressed["down"]:
            pygame.time.set_timer(MOVE_PIECE_EVENT, int(30))
        if pygame.key.get_just_released()[keys["down"]]:
            pygame.time.set_timer(MOVE_PIECE_EVENT, int(original_time_speed)) # seconds passed since last frame
          