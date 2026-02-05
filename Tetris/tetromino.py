import pygame
from pygame.locals import QUIT, Rect

class Tetromino():
    def __init__(self, block) -> None:
        self.shape = [[]]
        self.block = block
        self.size = 3

    def check_for_rotate(self, keys_just_pressed) -> bool:
        """
        this function checks if the player is rotating the current piece, and returns the new shape after rotation if the player did in fact rotate
        """
        rotate_clockwise = keys_just_pressed["a"]
        rotate_counterclockwise = keys_just_pressed["b"]
        newshape = []

        if rotate_clockwise:
            newshape = list(zip(*self.shape[::-1]))
            newshape = list(zip(*newshape[::-1]))
            newshape = list(zip(*newshape[::-1]))
            return newshape
        if rotate_counterclockwise:
            newshape = list(zip(*self.shape[::-1]))
            return newshape
        else:
            return False

        
            
class LinePiece(Tetromino):
    def __init__(self, block):
        super().__init__(block)
        self.shape = [
            ["", "", "", ""],
            [self.block, self.block, self.block, self.block],
            ["", "", "", ""],
            ["", "", "", ""]
            ]
        self.size = 4

class SquarePiece(Tetromino):
    def __init__(self, block):
        super().__init__(block)
        self.shape = [
            [self.block, self.block],
            [self.block, self.block]
        ]
        self.size = 2

class TPiece(Tetromino):
    def __init__(self, block):
        super().__init__(block)
        self.shape = [
            ["", "", ""],
            [self.block, self.block, self.block],
            ["", self.block, ""]
        ]

class SPiece(Tetromino):
    def __init__(self, block):
        super().__init__(block)
        self.shape = [
            ["", "", ""],
            ["", self.block, self.block],
            [self.block, self.block, ""]
        ]

class ZPiece(Tetromino):
    def __init__(self, block):
        super().__init__(block)
        self.shape = [
            ["", "", ""],
            [self.block, self.block, ""],
            ["", self.block, self.block]
        ]
class JPiece(Tetromino):
    def __init__(self, block):
        super().__init__(block)
        self.shape = [
            ["", "", ""],
            [self.block, self.block, self.block],
            ["", "", self.block]
        ]

class LPiece(Tetromino):
    def __init__(self, block):
        super().__init__(block)
        self.shape = [
            ["", "", ""],
            ["", "", self.block],
            [self.block, self.block, self.block]
        ]
