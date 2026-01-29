import os
import pygame

class Sound:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        current_dir = os.path.dirname(__file__)
        self.snake_collide_sound = pygame.mixer.Sound(os.path.join(current_dir, "assets", "sounds", "snake_collide.mp3"))
        self.win_one_round_sound = pygame.mixer.Sound(os.path.join(current_dir, "assets", "sounds", "win_one_round.mp3"))
        self.win_best_of_three_sound = pygame.mixer.Sound(os.path.join(current_dir, "assets", "sounds", "win_best_of_three.mp3"))

    def collide(self):
        self.snake_collide_sound.set_volume(0.4)
        self.snake_collide_sound.play()
        
    
    def winround(self):
        self.win_one_round_sound.set_volume(0.2)
        self.win_one_round_sound.play()
        
    
    def wingame(self):
        self.win_best_of_three_sound.set_volume(0.3)
        self.win_best_of_three_sound.play()
        