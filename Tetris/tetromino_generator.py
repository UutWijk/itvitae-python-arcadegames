from tetromino import *
import random
import game_state

class TetrominoGenerator():
    def __init__(self):
        self.tetromino_options = [LinePiece, SquarePiece, TPiece, SPiece, ZPiece, JPiece, LPiece]
        self.color_options = [
                            "a1","a2","a3","a4",
                            "b1","b2","b3","b4",
                            "c1","c2","c3","c4",
                            "d1","d2","d3","d4",
                            "e1","e2","e3","e4",
                            "f1","f2","f3","f4",
                            "g1","g2","g3","g4",
                            "h1","h2","h3","h4",
                            "i1","i2","i3","i4",
                            "j1","j2","j3","j4",
                            "k1","k2","k3","k4",
                            "l1","l2","l3","l4",
                            "m1","m2","m3","m4",
                            "n1","n2","n3","n4",
                            "o1","o2","o3","o4",
                            "p1","p2","p3","p4",
                            "q1","q2","q3","q4",
                            "r1","r2","r3","r4"
                            ]
        self.current_piece: Tetromino = LinePiece("a1")
        self.next_piece: Tetromino = None
        self.get_new_piece()
        self.get_new_piece()
      
                
    
    def get_new_piece(self):
        self.current_piece = self.next_piece

        # pick random piece while ensuring there are no duplicates
        new_piece = random.choice(self.tetromino_options)
        while new_piece == type(self.current_piece):
            new_piece = random.choice(self.tetromino_options)


        new_color = random.choice(self.color_options)
        while new_piece == type(self.current_piece):
            new_color = random.choice(self.color_options)
        
        self.next_piece = new_piece(new_color)

        game_state.timer.update_speed()

        return self.current_piece