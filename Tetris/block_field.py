import os
import pygame
import numpy as np
from typing import TYPE_CHECKING, Any
from .tetromino_generator import TetrominoGenerator
from .tetromino import Tetromino
from . import game_state

tetris_dir = os.path.dirname(os.path.abspath(__file__))

put_piece_down_sound = pygame.mixer.Sound(os.path.join(tetris_dir, "assets", "sounds", "put_piece_down.mp3"))
remove_lines_sound = pygame.mixer.Sound(os.path.join(tetris_dir, "assets", "sounds", "remove_lines.mp3"))
line_clear_4_sound = pygame.mixer.Sound(os.path.join(tetris_dir, "assets", "sounds", "4linesclear.mp3"))

class BlockField():
    """
    this class defines the playing field and where blocks are placed inside of it
    """
    def __init__(self):
        self.defaultgrid = np.array([
    ["", "", "", "", "", "", "", "", "", "", "", "", ""], 
    ["", "", "", "", "", "", "", "", "", "", "", "", ""], 
    ["", "", "", "", "", "", "", "", "", "", "", "", ""], 
    ["", "", "", "", "", "", "", "", "", "", "", "", ""], 
    ["", "", "", "", "", "", "", "", "", "", "", "", ""], 
    ["", "", "", "", "", "", "", "", "", "", "", "", ""], 
    ["", "", "", "", "", "", "", "", "", "", "", "", ""], 
    ["", "", "", "", "", "", "", "", "", "", "", "", ""], 
    ["", "", "", "", "", "", "", "", "", "", "", "", ""], 
    ["", "", "", "", "", "", "", "", "", "", "", "", ""], 
    ["", "", "", "", "", "", "", "", "", "", "", "", ""], 
    ["", "", "", "", "", "", "", "", "", "", "", "", ""], 
    ["", "", "", "", "", "", "", "", "", "", "", "", ""], 
    ["", "", "", "", "", "", "", "", "", "", "", "", ""], 
    ["", "", "", "", "", "", "", "", "", "", "", "", ""], 
    ["", "", "", "", "", "", "", "", "", "", "", "", ""], 
    ["", "", "", "", "", "", "", "", "", "", "", "", ""], 
    ["", "", "", "", "", "", "", "", "", "", "", "", ""], 
    ["", "", "", "", "", "", "", "", "", "", "", "", ""], 
    ["", "", "", "", "", "", "", "", "", "", "", "", ""], 
    ["", "", "", "", "", "", "", "", "", "", "", "", ""], 
    ["", "", "", "", "", "", "", "", "", "", "", "", ""], 
    ["", "", "", "", "", "", "", "", "", "", "", "", ""], 
    #this field is 3 rows lower & wider than you actually see so that empty bits of pieces don't end up out of range. Left side is handled differently
],   dtype='<U2'
)       
        self.grid = self.defaultgrid.copy()
        #generating the field this way makes it easier to empty the field again for a new game
        self.tetromino_generator = TetrominoGenerator()
        self.current_piece: Tetromino = self.tetromino_generator.current_piece
        self.piece_position = [0, 3]
        self.score = 0
        HSfile = open("HighScore.txt")
        self.leaderboard = HSfile.readlines()
        self.sprite_sheet = pygame.image.load(os.path.join(tetris_dir, "assets", "blocks", "sprites.png")).convert_alpha()
        self.calculate_game_speed()
    
    def draw(self, surface, pos_x, pos_y) -> None:
        x = pos_x
        y = pos_y
        pygame.draw.rect(surface, "black", pygame.Rect(x, y, 330, 660))

        playfield = self.get_array()
      
        for r in range(20):
            for c in range(10):
                value_of_piece = playfield[r][c]

                if value_of_piece:
                    letter = value_of_piece[0]
                    number = value_of_piece[1]

                    row = ord(letter) - ord('a')
                    col = int(number) - 1

                    sprite_rect = pygame.Rect(
                        col * 30,
                        row * 30,
                        30,
                        30
                    )

                    img = self.sprite_sheet.subsurface(sprite_rect)
                    
                    surface.blit(img, (x +3 + (c * 33),y + ( r * 33)))

         

    def remove_empty_space(self) ->list[list]: #as drawshape
        """
        removes empty spaces to left of tetromino 
        """
        if self.current_piece == None:
            return
        drawshape = self.current_piece.shape.copy()
        #shave off the left columns of a tetromino in the event that it goes past the left of the screen
        if(self.piece_position[1] < 0):
            # code that would work if shape was a numpy array: self.current_piece.shape = self.current_piece.shape[:,int(abs(self.piece_position[1])):]
            for i in range(len(self.current_piece.shape)):
                drawshape[i] = self.current_piece.shape[i][abs(self.piece_position[1]):]  
        return drawshape                   

    def put_piece_into_grid(self) -> bool:
        """
        this function places a tetromino into the game board after it has landed and player control transfers to the next tetromino
        """
        drawshape = self.remove_empty_space()
        self.grid[self.piece_position[0]:self.piece_position[0]+self.current_piece.size, max(self.piece_position[1], 0):self.piece_position[1]+self.current_piece.size] += drawshape
        put_piece_down_sound.play()
        self.remove_full_rows()
        self.current_piece = self.tetromino_generator.get_new_piece()
        self.piece_position = [0, 3]
        self.check_game_over()

    def remove_full_rows(self) -> None:
        """
        Checks the rows that overlap the piece just puts down.
        If a row is full it shifts the grid above down so the row is removed. 
        Also counts the lines removed and calls the update_score() method
        """
        current_line = self.piece_position[0]
        lines_removed = 0
        
        # for the lines that overlap the piece just put down
        for i in range(self.current_piece.size):
            # check if current line has no empty spots
            if True not in (self.grid[current_line][0:10] == ""):
                # shift the grid above down so the line is removed
                self.grid[1:current_line+1] = self.grid[0:current_line]
                lines_removed += 1
            current_line += 1
        # update the score
        if lines_removed > 0:
            self.update_score(lines_removed)
            if lines_removed == 4:
                line_clear_4_sound.play()
            else:
                remove_lines_sound.play()
    
    def update_score(self, lines_removed) -> None: 
        match lines_removed:
            case 1: score_to_add = 40
            case 2: score_to_add = 100
            case 3: score_to_add = 300
            case 4: score_to_add = 1200
        
        self.score += score_to_add
        self.calculate_game_speed()
        
    def calculate_game_speed(self) -> None:
        speed =  1000 / (1 + 0.000065 * self.score ** 1.18)
        game_state.timer.set_speed(int(speed))

    def get_array(self) -> np.ndarray[Any]:
        """this function returns the a copy of the current grid with the current curent piece put in"""
        new_array = np.array(self.grid)
        drawshape = self.remove_empty_space()    
        #draws piece onto playfield, with max assuring that it will start drawing from the left of the playfield if piece extends beyond this
        new_array[self.piece_position[0]:self.piece_position[0]+self.current_piece.size, max(self.piece_position[1], 0):self.piece_position[1]+self.current_piece.size] += drawshape
        return new_array
    
    def check_game_over(self) -> bool:
        """this function checks if a new place can be placed in the game board, and if not the game ends"""
        piece = self.current_piece.shape
        position = self.piece_position
        for r in range(len(piece)):
            for c in range(len(piece[r])):
                #test if new piece overlaps with existing pieces, and if so signal that the game is over
                if(piece[r][c] and (self.grid[position[0] + r][position[1] + c]) and game_state.game_continues == True):
                    self.add_score()
                    game_state.game_continues = False
       
    
    def add_score(self) -> None:
        """this function adds the player's score to the leaderboard at the end of a game, provided it is high enough"""
        scores = self.leaderboard
        scoreList = []

        for score in range(10):
            scoreList.append(int(scores[score]))  
        #self.score = 6001    <- to test if new scores are added to highscore correctly
        newScore = self.score  
        if self.score > scoreList[9]:
            scoreList.append(newScore)
            scoreList.sort(reverse=True)
            scores = ""
            for score in range(10):
                scores += (str(scoreList[score]) + "\n")
            with open('HighScore.txt', 'w', encoding='utf-8') as file:
                file.writelines(scores)
            scorefile = open("HighScore.txt")
            self.leaderboard = scorefile.readlines()    
             
    def test_below(self) -> bool:
        """this function tests if a piece can move downwards"""

        piece = self.current_piece.shape
        position = self.piece_position
        for r in range(len(piece)):
            for c in range(len(piece[r])):
                if(piece[r][c] and (self.grid[position[0] + r + 1][position[1] + c] or position[0] + r >= 19)):
                #this checks if the piece at a row & column contains a block and the spot 1 row below on the same column in the grid also contains a block
                #or if the piece has reached the bottom    
                    return False
        return True       

    def test_right(self) -> bool:
        """this function texts if a piece can move to the right"""
        piece = self.current_piece.shape
        position = self.piece_position
        for r in range(len(piece)):
            for c in range(len(piece[r])):
                if(piece[r][c] and (self.grid[position[0] + r][position[1] + c + 1] or position[1] + c >= 9)):  
                    return False
        return True   
    
    def test_left(self) -> bool:
        """this function tests if a piece can move to the left"""
        piece = self.current_piece.shape
        position = self.piece_position
        for r in range(len(piece)):
            for c in range(len(piece[r])):
                if(piece[r][c] and (self.grid[position[0] + r][position[1] + c - 1] or position[1] + c <= 0)):  
                    return False
        return True 

    def move_piece(self, direction):
        if direction == "down":
            can_move = self.test_below()
            if can_move:
                self.piece_position[0] += 1
            else:
                self.put_piece_into_grid()



        elif direction == "right":
            can_move = self.test_right()
            if can_move:
                self.piece_position[1] += 1
        elif direction == "left":
            can_move = self.test_left()
            if can_move:
                self.piece_position[1] -= 1
    

