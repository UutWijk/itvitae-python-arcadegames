import os
import pygame
import random
import array

class Sound:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.current_dir = os.path.dirname(os.path.abspath(__file__))

        self.asteroid_break_1_sound = pygame.mixer.Sound(os.path.join(self.current_dir, "sounds/asteroid_break_1.mp3"))
        self.asteroid_break_2_sound = pygame.mixer.Sound(os.path.join(self.current_dir, "sounds/asteroid_break_2.mp3"))
        self.laser_1_sound = pygame.mixer.Sound(os.path.join(self.current_dir, "sounds/laser_1.mp3"))
        self.laser_2_sound = pygame.mixer.Sound(os.path.join(self.current_dir, "sounds/laser_2.mp3"))
        self.ship_impact_sound = pygame.mixer.Sound(os.path.join(self.current_dir, "sounds/ship_impact.mp3"))
        self.ufo_sound = pygame.mixer.Sound(os.path.join(self.current_dir, "sounds/ufo.mp3"))
        self.ufo_sound.set_volume(0.5)

    def laser(self):
        self.laser_2_sound.set_volume(0.5)
        self.laser_2_sound.play()
    
    def asteroid_break(self):
        breaksound = self.asteroid_break_1_sound
        breaksound.set_volume(0.5)
        breaksound.play()
    
    def ship_impact(self):
        self.ship_impact_sound.set_volume(0.5)
        self.ship_impact_sound.play()

    def ufo(self):
        
        self.ufo_sound.play()
    
    def fade_ufo(self, amount):
        self.ufo_sound.set_volume(self.ufo_sound.get_volume()-amount)

